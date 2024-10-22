from datetime import datetime
from enum import Enum
from pydantic import (
    BaseModel, Field, FilePath, HttpUrl, EmailStr, model_validator, SecretStr
)
from typing import List, Optional


class GmailMessageSchema(BaseModel):
    msg_id: str = Field(alias='id')
    sender: str = Field(alias='From')
    receiver: str = Field(alias='To')
    subject: str = Field(alias='Subject')
    body: str = Field(alias='snippet')
    received_date: datetime = Field(alias='Date received')

    class Config:
        from_attributes = True
        populate_by_name = True


class GmailHeader(BaseModel):
    name: str
    value: str


class GmailPayload(BaseModel):
    headers: List[GmailHeader]
    body: Optional[dict] = None


class GmailMessage(BaseModel):
    id: str
    snippet: str
    internalDate: str
    payload: GmailPayload


class DbEnum(str, Enum):
    sqlite = 'sqlite'
    mysql = 'mysql'
    postgres = 'postgres'


class ActionEnum(str, Enum):
    mark_as_read = 'Mark as Read'
    mark_as_unread = 'Mark as Unread'
    move_message = 'Move Message'


class Provider(str, Enum):
    google = 'google'


class Service(str, Enum):
    gmail = 'gmail'


class DbConfigParams(BaseModel):
    database: str = Field(description='database name.')
    username: str = Field(description='user name.')
    hostname: str = Field(description='host.')
    port: int = Field(description='port.')
    password: SecretStr = Field(description='password.')


class DbConfig(BaseModel):
    db_type: DbEnum = DbEnum.sqlite
    sqlite: dict = None
    mysql: DbConfigParams = None
    postgres: DbConfigParams = None

    # validator to check dependencies between db_type and its database config
    @model_validator(mode='before')
    def check_db_config(cls, values):
        db_type = values and values.get('db_type') or None

        # Validate db_type and ensure corresponding key is present
        msg = f'For db_type "{db_type}", the "{db_type}" key must be provided\n'
        if db_type == 'sqlite':
            if not values.get('sqlite'):
                raise ValueError(msg)
            if not values.get('sqlite').get('database'):
                msg = (f"For db_type '{db_type}', "
                       f"'database' key must be provided\n")
                raise ValueError(msg)
        elif db_type == 'postgres':
            if not values.get('postgres'):
                raise ValueError(msg)
        elif db_type == 'mysql':
            if not values.get('mysql'):
                raise ValueError(msg)
        else:
            raise ValueError(f'Unsupported db_type: {db_type}')

        return values


class ServiceConfigParams(BaseModel):
    path_to_credentials: str = Field(description='path to gmail API credentials.json')
    path_to_token: str = Field(description='path to gmail API token.json')
    scopes: List[str]


class ServiceConfig(BaseModel):
    service: Service = Service.gmail
    gmail: ServiceConfigParams = None
    outlook: dict = None

    # validator to check dependencies between service and its service config
    @model_validator(mode='before')
    def check_db_config(cls, values):
        service = values.get('service')

        # Validate db_type and ensure corresponding key is present
        msg = f'For service "{service}", the "{service}" key must be provided\n'
        if service == 'gmail':
            if not values.get('gmail'):
                raise ValueError(msg)
        elif service == 'outlook':
            if not values.get('outlook'):
                raise ValueError(msg)
        else:
            raise ValueError(f'Unsupported db_type: {service}')

        return values


class Condition(BaseModel):
    field: str
    predicate: str
    value: str


class Action(BaseModel):
    action: ActionEnum


class Rule(BaseModel):
    conditions: List[Condition]
    predicate: str
    actions: List[Action]


class Rules(BaseModel):
    rules: List[Rule]


class Config(BaseModel):
    db_config: DbConfig
    service_config: ServiceConfig
