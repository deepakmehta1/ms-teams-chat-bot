from typing import List
from botbuilder.core import (
    ConversationState,
    UserState,
    TurnContext,
)
from botbuilder.dialogs import Dialog
from botbuilder.schema import ChannelAccount
from src.helpers.dialog_helper import DialogHelper
from src.bots.dialog_bot import DialogBot


class AuthBot(DialogBot):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        super(AuthBot, self).__init__(conversation_state, user_state, dialog)

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello, welcome to Bot 😊")
                print("new member has been added!")

    async def on_sign_in_invoke(self, turn_context: TurnContext):
        return await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )
