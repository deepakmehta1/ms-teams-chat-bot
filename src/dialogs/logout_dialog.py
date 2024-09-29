import logging
from botbuilder.dialogs import DialogTurnResult, ComponentDialog, DialogContext
from botbuilder.schema import ActivityTypes
from botframework.connector.auth.user_token_client import UserTokenClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LogoutDialog(ComponentDialog):
    def __init__(
        self,
        dialog_id: str,
        connection_name: str,
    ):
        super(LogoutDialog, self).__init__(dialog_id)

        self.connection_name = connection_name

        logger.info(
            f"LogoutDialog initialized with dialog_id: {dialog_id} and connection_name: {connection_name}"
        )

    async def on_begin_dialog(
        self, inner_dc: DialogContext, options: object
    ) -> DialogTurnResult:
        logger.info("Begin dialog called.")
        result = await self._interrupt(inner_dc)
        if result:
            logger.info("Dialog interrupted and will be canceled.")
            return result
        logger.info("No interruption, proceeding with dialog.")
        return await super().on_begin_dialog(inner_dc, options)

    async def on_continue_dialog(self, inner_dc: DialogContext) -> DialogTurnResult:
        logger.info("Continue dialog called.")
        result = await self._interrupt(inner_dc)
        if result:
            logger.info("Dialog interrupted and will be canceled.")
            return result
        logger.info("No interruption, continuing with dialog.")
        return await super().on_continue_dialog(inner_dc)

    async def _interrupt(self, inner_dc: DialogContext):
        if inner_dc.context.activity.type == ActivityTypes.message:
            text = inner_dc.context.activity.text.lower()
            logger.info(f"Received message: {text}")
            if text == "logout":
                logger.info("Logout command received.")
                try:
                    user_token_client: UserTokenClient = (
                        inner_dc.context.turn_state.get(UserTokenClient.__name__, None)
                    )
                    if user_token_client:
                        user_id = inner_dc.context.activity.from_property.id
                        channel_id = inner_dc.context.activity.channel_id
                        logger.info(
                            f"Signing out user with id: {user_id} on channel: {channel_id}"
                        )

                        await user_token_client.sign_out_user(
                            user_id,
                            self.connection_name,
                            channel_id,
                        )
                        logger.info("User signed out successfully.")

                        await inner_dc.context.send_activity(
                            "You have been signed out."
                        )
                        logger.info("Sign-out confirmation sent to user.")
                        return await inner_dc.cancel_all_dialogs()
                    else:
                        logger.error("UserTokenClient not found in turn state.")
                        await inner_dc.context.send_activity(
                            "Failed to sign out. User token client not found."
                        )
                except Exception as e:
                    logger.error(
                        f"An error occurred during logout: {str(e)}", exc_info=True
                    )
                    await inner_dc.context.send_activity(
                        "An error occurred while signing out. Please try again."
                    )
        else:
            logger.debug("Activity type is not a message, no interruption needed.")
        return None
