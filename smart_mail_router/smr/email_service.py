from abc import ABC, abstractmethod

class EmailService(ABC):
    @abstractmethod
    def get_client(self, **kwargs):
        """Get client to interact with the email service."""
        pass

    @abstractmethod
    def emails(self):
        """Get list of messages from the email service."""
        pass

    @abstractmethod
    def get_email(self, msg_id):
        """Get message details from the email service."""
        pass

    @abstractmethod
    def labels(self):
        """Get labels from the email service."""
        pass

    @abstractmethod
    def mark_as_read(self, msg_id):
        """To mark message as read from the email service."""
        pass

    @abstractmethod
    def mark_as_unread(self, msg_id):
        """To mark message as read from the email service."""
        pass

    @abstractmethod
    def move_to_label(self, msg_id, label_id):
        """To move message to a label/folder from the email service."""
        pass