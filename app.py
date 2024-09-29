import logging
from datetime import datetime
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    ConversationState,
    MemoryStorage,
    TurnContext,
    UserState,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import (
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication,
)
from botbuilder.schema import Activity, ActivityTypes

from src.bots import AuthBot
from config import DefaultConfig
from src.dialogs import MainDialog
from src.conversation.services.conversation_service import ConversationService
from src.conversation.history.conversation_history import ConversationHistory
from src.conversation.services.key_manager import KeyManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG = DefaultConfig()

ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    logger.error(f"[on_turn_error] unhandled error: {error}", exc_info=True)

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )

    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)


ADAPTER.on_turn_error = on_error

MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)

KEY_MANAGER = KeyManager(CONFIG)
CONVERSATION_HISTORY = ConversationHistory()
CONVERSATION_SERVICE = ConversationService(KEY_MANAGER)

DIALOG = MainDialog(CONFIG, CONVERSATION_HISTORY, CONVERSATION_SERVICE)

BOT = AuthBot(CONVERSATION_STATE, USER_STATE, DIALOG)


async def messages(req: Request) -> Response:
    logger.info(f"API called: {req.method} {req.path}")
    response = await ADAPTER.process(req, BOT)
    if response:
        if response.body is None:
            args = {"status": response.status}
        else:
            args = {"data": response.body, "status": response.status}

        return json_response(**args)
    return Response(status=201)


async def ping(req: Request) -> Response:
    return json_response(
        {"status": "ok", "message": "Service is running"}, status=HTTPStatus.OK
    )


APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/internal/api/messages", messages)
APP.router.add_get("/health", ping)

if __name__ == "__main__":
    try:
        logger.info("Starting the web server...")
        web.run_app(APP, host="0.0.0.0", port=CONFIG.PORT)
    except Exception as error:
        logger.exception("Failed to start the server: %s", error)
        raise
