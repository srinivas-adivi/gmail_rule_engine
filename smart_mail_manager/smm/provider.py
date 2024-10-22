
import smr.gmail_service
import smr.payload_manager
import smr.rule_executor

import smm.database


class EmailServiceProvider:

    def __init__(self, service: str, config: dict):
        self.service = service
        self.config = config

    def get_email_service(self):
        services = {
            "gmail": smr.gmail_service.GmailService(self.config),
        }
        if not self.service in services:
            raise ValueError(f"Unsupported service: {self.service}")

        return services.get(self.service)

    def get_payload_manager(self):
        services = {
            "gmail": smr.payload_manager.GmailPayloadManager(),
        }
        if not self.service in services:
            raise ValueError(f"Unsupported service: {self.service}")

        return services.get(self.service)

    def get_rule_executor(self):
       service = self.get_email_service()
       return smr.rule_executor.RuleExecutor(service)


class DBProvider:

    @staticmethod
    def get_database(db_type: str, config: dict):
        db_factory = {
            "sqlite": smm.database.SQLiteDatabase(config),
        }
        if not db_type in db_factory:
            raise ValueError(f"Unsupported database type: {db_type}")

        # Get the concrete class
        database = db_factory.get(db_type)
        # construct the connection string
        connection_string = database.get_connection_string(config)
        database.connect(connection_string)
        return database