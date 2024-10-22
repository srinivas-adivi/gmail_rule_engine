
class RuleExecutor:
    """Executes actions on emails that satisfy the rule conditions."""

    def __init__(self, email_service):
        self.email_service = email_service

    def _get_label_id(self, label_name):
        """Helper to find the label/folder ID by name."""
        labels = self.email_service.labels()
        for label in labels:
            if label['name'].lower() == label_name.lower():
                return label['id']
        print(f"Label '{label_name}' not found.")
        return None

    def _mark_as_read(self, msg_id):
        """Private method to mark message as read."""
        self.email_service.mark_as_read(msg_id)

    def _mark_as_unread(self, msg_id):
        """Private method to mark message as read."""
        self.email_service.mark_as_unread(msg_id)

    def _move_to_label(self, msg_id, label_id):
        """Private method to move message to a label/folder."""
        self.email_service.move_to_label(msg_id, label_id)

    def apply_actions(self, msg_id, actions):
        """Apply the actions to the email."""

        for action_info in actions:
            action = action_info.action.lower()
            if action == 'mark as read':
                self._mark_as_read(msg_id)
                print(f"Marked email {msg_id} as read.")
            elif action == 'mark as unread':
                self._mark_as_unread(msg_id)
                print(f"Marked email {msg_id} as unread.")
            elif action.startswith('move message'):
                label = action.split(':')[1]
                label_id = self._get_label_id(label)
                if label_id:
                    self._move_to_label(msg_id, label_id)
                    print(f"Moved email {msg_id} to label {label}.")
            else:
                print(f"Unknown action: {action}")
