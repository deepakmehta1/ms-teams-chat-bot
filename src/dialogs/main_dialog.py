import logging
from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import OAuthPrompt, OAuthPromptSettings, ConfirmPrompt
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions
from config import DefaultConfig
from src.dialogs.logout_dialog import LogoutDialog
from src.services import Auth, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainDialog(LogoutDialog):
    def __init__(
        self,
        config: DefaultConfig,
    ):
        """
        Initializes MainDialog with configuration and services.
        """
        super(MainDialog, self).__init__(
            MainDialog.__name__, config.CONNECTION_NAME
        )
        self.config = config

        self._add_prompts_and_dialogs()
        self._setup_config_attributes()

    def _add_prompts_and_dialogs(self):
        """Adds OAuth and confirmation prompts, and sets up the waterfall dialog."""
        self.add_dialog(self._create_oauth_prompt())
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog("WFDialog", [self.prompt_step, self.login_step])
        )

    def _create_oauth_prompt(self) -> OAuthPrompt:
        """Creates the OAuth prompt for user authentication."""
        return OAuthPrompt(
            OAuthPrompt.__name__,
            OAuthPromptSettings(
                connection_name=self.config.CONNECTION_NAME,
                text="Welcome to Syntea, Please sign in to continue",
                title="Sign In",
                timeout=180000,
            ),
        )

    def _setup_config_attributes(self):
        """Stores configuration values like OAuth, LLM, and template settings."""
        self.auth0_issuer = self.config.AUTH_ISSUER
        self.auth0_audience = self.config.AUTH_AUDIENCE
        self.auth0_algorithm = self.config.AUTH_ALGORITHM
        self.gcd_orch_template_id = self.config.GCD_ORCH_TEMPLATE
        self.gcd_orch_template_version_id = self.config.GCD_ORCH_TEMPLATE_VERSION
        self.llm_flow_service_url = self.config.LLM_FLOW_SERVICE_URL
        self.initial_dialog_id = "WFDialog"

    async def prompt_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Starts the OAuth prompt."""
        logger.info("Prompt step started.")
        return await step_context.begin_dialog(OAuthPrompt.__name__)

    async def login_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Handles login result and initiates the conversation."""
        logger.info("Login step started.")

        if step_context.result:
            return await self._handle_successful_login(step_context)

        logger.warning("Login failed. User did not authenticate.")
        await step_context.context.send_activity(
            "Login was not successful, please try again."
        )
        return await step_context.end_dialog()

    async def _handle_successful_login(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Processes successful login and handles conversation."""
        try:
            user = self._authenticate_user(step_context.result.token)
            response_text, help_text = await self._execute_conversation(
                step_context, user
            )
            await self._send_response_with_suggestions(
                step_context, response_text, help_text
            )
            return await step_context.end_dialog()

        except Exception as e:
            return await self._handle_login_error(step_context, e)

    def _authenticate_user(self, token: str) -> User:
        """Authenticates the user using the provided token."""
        auth = Auth(self.auth0_issuer, self.auth0_audience, self.auth0_algorithm)
        decoded_token = auth.decode_jwt(token)
        return User(token, decoded_token)

    async def _execute_conversation(
        self, step_context: WaterfallStepContext, user: User
    ) -> tuple[str, list]:
        """Executes the conversation using the LLM flow service."""
        # todo execute the conversation here 
        pass 

    async def _send_response_with_suggestions(
        self, step_context: WaterfallStepContext, response_text: str, help_text: list
    ):
        """Sends the response with suggested actions to the user."""
        reply = MessageFactory.text(response_text)
        actions = [
            CardAction(title=ht, type=ActionTypes.im_back, value=ht) for ht in help_text
        ]
        reply.suggested_actions = SuggestedActions(actions=actions)
        await step_context.context.send_activity(reply)

    async def _handle_login_error(
        self, step_context: WaterfallStepContext, error: Exception
    ) -> DialogTurnResult:
        """Handles errors during login."""
        logger.error(f"An error occurred during login: {str(error)}", exc_info=True)
        await step_context.context.send_activity(
            "😔 Something went wrong... type logout and try again!"
        )
        return await step_context.end_dialog()
