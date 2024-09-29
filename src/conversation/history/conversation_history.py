from src.conversation.roles.role_classes import BaseRole


class ConversationHistory:
    """
    A class to manage the history of a conversation between the user and assistant using role classes.
    """

    def __init__(self):
        self.history = []

    def add_message(self, message: BaseRole):
        """
        Add a role-based message to the conversation history.

        Args:
            message (BaseRole): A message object from a specific role (UserRole, AssistantRole, SystemRole).
        """
        self.history.append(message.to_dict())

    def get_history(self):
        """
        Get the entire conversation history in dictionary format.

        Returns:
            list: The list of conversation messages.
        """
        return self.history

    def clear_history(self):
        """
        Clear the conversation history.
        """
        self.history = []
