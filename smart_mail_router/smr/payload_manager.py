from abc import ABC, abstractmethod


class PayloadManager(ABC):

    @abstractmethod
    def api_parser(self, payload):
        pass

    @abstractmethod
    def schema_parser(self, payload):
        pass

class GmailPayloadManager(PayloadManager):

    def api_parser(self, api_data):
        """ Convert API Data to a format suitable for DB operations.

        :param api_data:
        :return:
        """
        payload = api_data.payload
        headers = payload.headers
        sender = next(header.value for header in headers
               if header.name == 'From')
        subject = next(header.value for header in headers
                       if header.name == 'Subject')
        receiver = next(header.value for header in headers
                        if header.name == 'To')
        return {
            'id': api_data.id,
            'From': sender,
            'To': receiver,
            'Subject': subject,
            'snippet': api_data.snippet,
            'internalDate': api_data.internalDate
        }

    def schema_parser(self, gmail_schema):
        """ Convert DB model schema to a format suitable for Gmail API operations

        :param gmail_schema:
        :return:
        """
        internal_date = str(gmail_schema.received_date.timestamp() * 1000)
        return {
            'id': gmail_schema.msg_id,
            'From': gmail_schema.from_email,
            'To': gmail_schema.to_email,
            'Subject': gmail_schema.subject,
            'snippet': gmail_schema.body,
            'internalDate': internal_date
        }
