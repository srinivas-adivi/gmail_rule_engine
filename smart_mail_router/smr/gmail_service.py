import os
import os.path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import DefaultCredentialsError
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from smr.email_service import EmailService


# If modifying these SCOPES, delete the token.json file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailService(EmailService):

    def __init__(self, config):
        self.config = config
        self.service = self.get_client()

    def create_token(self):
        """Connect to Gmail using OAuth."""

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        try:
            path_to_creds = self.config.path_to_credentials or 'credentials.json'
            scopes = self.config.scopes or SCOPES
            path_to_token = self.config.path_to_token or 'token.json'
            flow = InstalledAppFlow.from_client_secrets_file(path_to_creds, scopes)
            creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(path_to_token, 'w') as token:
                token.write(creds.to_json())

        except FileNotFoundError as error:
            file_name = error.filename
            strerror = error.strerror
            print(f"Failed: generate a token: `{file_name}` {strerror}")

    def get_user_credentials(self):
        """

        :return: gmail service
        """
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        scopes = self.config.scopes or SCOPES
        path_to_token = self.config.path_to_token or 'token.json'
        if not os.path.exists(path_to_token):
            self.create_token()

        try:
            creds = Credentials.from_authorized_user_file(path_to_token, scopes)
            # If there are no (valid) credentials available, let the user log in.
            if not creds.valid and creds.expired and creds.refresh_token:
                print(f'get_service: credentials: refresh')
                creds.refresh(Request())
            return creds

        except FileNotFoundError as error:
            file_name = error.filename
            strerror = error.strerror
            print(f"Failed: create a gmail service: `{file_name}` {strerror}")

    def get_client(self):
        """ Get client to interact with Gmail service.

        :return:
        """
        try:
            creds = self.get_user_credentials()
            return build('gmail', 'v1', credentials=creds)
        except DefaultCredentialsError as error:
            print(f"Failed: {error}")

    def emails(self):
        """Fetch emails from Gmail.

        :return: list of e-mails
        """
        users_messages = self.service.users().messages()
        results = users_messages.list(userId='me').execute()
        messages = results.get('messages', [])

        return messages

    def get_email(self, email_id):
        """Fetch emails from Gmail.

        :return: list of e-mails
        """
        users_messages = self.service.users().messages()
        msg_data = users_messages.get(userId='me', id=email_id).execute()

        return msg_data
    def labels(self):
        """List all labels in the user's mailbox using Gmail client"""
        users_labels = self.service.users().labels()
        labels = users_labels.list(userId='me').execute().get('labels', [])

        return labels

    def mark_as_read(self, msg_id):
        """ To mark message as read using Gmail client

        :param msg_id: message id
        :return:
        """
        print(f"Marking email as read: {msg_id}")
        users_messages = self.service.users().messages()
        users_messages.modify(userId='me', id=msg_id,
                              body={'removeLabelIds': ['UNREAD']}).execute()

    def mark_as_unread(self, msg_id):
        """ To mark message as unread using Gmail client

        :param msg_id: message id
        :return:
        """
        print(f"Marking email as unread: {msg_id}")
        users_messages = self.service.users().messages()
        users_messages.modify(userId='me', id=msg_id,
                              body={'addLabelIds': ['UNREAD']}).execute()

    def move_to_label(self, msg_id, label_id):
        """ To move message to a label/folder using Gmail client

        :param msg_id: message id
        :param label_id: label id
        :return:
        """
        print(f"Moving email: {msg_id} to {label_id}")
        users_messages  = self.service.users().messages()
        users_messages.modify(userId='me', id=msg_id,
                              body={'addLabelIds': [label_id]}).execute()