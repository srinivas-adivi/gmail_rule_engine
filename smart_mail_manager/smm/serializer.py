from abc import ABC, abstractmethod
from datetime import datetime

from smm.data_models import GmailMessageSchema


class EmailSerializer(ABC):

    @abstractmethod
    def to_email_schema(self, payload):
        """Convert payload to DB model"""
        pass

    @abstractmethod
    def to_email_model(self, payload):
        pass

    @abstractmethod
    def from_email_model(self, db_model):
        pass


class GmailSerializer(EmailSerializer):

    def to_email_schema(self, payload):
        """ Converts API Data to a format suitable for DB operations.

        :param payload: after parser of API data.
        :return:
        >>> sample_api_data = {"id": "1", "From": "from_example@gmail.com",
        ... "To": "to_example@gmail.com", "Subject": "Hello World",
        ... "snippet": "This is a test msg.", "internalDate": "1729524475839"}
        """
        internal_date = int(payload.get('internalDate')) / 1000
        received_date = datetime.fromtimestamp(internal_date).isoformat()
        email_data = {
            'msg_id': payload.get('id'),
            'sender': payload.get('From'),
            'receiver': payload.get('To'),
            'subject': payload.get('Subject'),
            'body': payload.get('snippet'),
            'received_date': received_date,
        }

        return email_data

    def to_email_model(self, payload):
        """ Converts payload to db model.

        :param payload:
        :return:
        >>> api_data = {"id": "1", "From": "from_example@gmail.com",
        ... "To": "to_example@gmail.com", "Subject": "Hello World",
        ... "snippet": "This is a test msg.", "internalDate": "1729524475839"}
        >>> sample_payload = { "msg_id": api_data.get("id"),
        ... "sender": api_data.get("From"), "receiver": api_data.get("To"),
        ... "subject": api_data.get("Subject"), "body": api_data.get("snippet"),
        ... "received_date": api_data.get("internalDate")}
        """
        schema = GmailMessageSchema(**payload)
        return schema.model_dump()

    def from_email_model(self, db_model):
        """ Converts db model to gmail schema """
        return GmailMessageSchema(**db_model.__dict__)