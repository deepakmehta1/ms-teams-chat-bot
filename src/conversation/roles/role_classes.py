class BaseRole:
    """
    Base class representing a participant in the conversation.
    Each role (system, user, assistant) will inherit from this class.
    """

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        """
        Convert the role and content into a dictionary format, as required by the OpenAI API.

        Returns:
            dict: A dictionary representation of the message.
        """
        return {"role": self.role, "content": self.content}


class SystemRole(BaseRole):
    """
    Represents the 'system' role in the conversation, used to set the behavior and context.
    """

    def __init__(self, content: str):
        super().__init__(role="system", content=content)


class UserRole(BaseRole):
    """
    Represents the 'user' role in the conversation, typically used for the user's input.
    """

    def __init__(self, content: str):
        super().__init__(role="user", content=content)


class AssistantRole(BaseRole):
    """
    Represents the 'assistant' role in the conversation, typically used for the AI model's responses.
    """

    def __init__(self, content: str):
        super().__init__(role="assistant", content=content)
