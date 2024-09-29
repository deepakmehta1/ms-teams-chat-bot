import logging
from openai import AsyncOpenAI
from src.conversation.history.conversation_history import ConversationHistory
from src.conversation.roles.role_classes import UserRole, AssistantRole


class ConversationService:
    """
    A service class to manage conversation with OpenAI and keep track of the history.
    """

    def __init__(self, key_manager):
        """
        Initialize the ConversationService with the OpenAI API key.

        Args:
            key_manager (KeyManager): Instance of the KeyManager class to retrieve the API key.
        """
        self.api_key = key_manager.get_api_key()
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def _send_message(
        self, history, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150
    ):
        """
        Sends the current conversation history to OpenAI asynchronously and returns the assistant's response.

        This method is intended for internal use only and should not be accessed directly.

        Args:
            history (list): The full conversation history with both user and assistant messages.
            model (str): The model to use for the chat completion.
            temperature (float): The temperature setting for the OpenAI model.
            max_tokens (int): The maximum number of tokens in the response.

        Returns:
            str: The assistant's response message.
        """
        try:
            # Use OpenAI's async method to send the conversation history
            response = await self.client.chat.completions.create(
                model=model,
                messages=history,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            response = response.to_dict()
            assistant_message = response["choices"][0]["message"]["content"]
            return assistant_message
        except Exception as e:
            logging.error(f"An error occurred while sending the message: {e}")
            raise e

    async def process_message(
        self, conversation: ConversationHistory, user_message: str
    ):
        """
        Process a new user message by sending it to the OpenAI API asynchronously, updating the conversation history,
        and returning the assistant's response.

        Args:
            conversation (ConversationHistory): The conversation object that tracks the conversation history.
            user_message (str): The user's message to be sent to OpenAI.

        Returns:
            str: The assistant's response message.
        """
        # Step 1: Add the user's message to the conversation history
        conversation.add_message(UserRole(user_message))

        # Step 2: Send the conversation history to OpenAI and get the assistant's response
        assistant_message = await self._send_message(conversation.get_history())

        # Step 3: Add the assistant's response to the conversation history
        conversation.add_message(AssistantRole(assistant_message))

        # Step 4: Return the assistant's response
        return assistant_message
