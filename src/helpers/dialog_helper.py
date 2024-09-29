from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus


class DialogHelper:
    @staticmethod
    async def run_dialog(
        dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        """
        Executes a dialog using the provided context and state accessor. This function
        continues an existing dialog if one is active or starts a new dialog if no active
        dialog is found.

        Args:
            dialog (Dialog): The dialog to be executed.
            turn_context (TurnContext): The context for the current turn of the bot, containing information
                                        about the conversation and activities.
            accessor (StatePropertyAccessor): The state property accessor used to manage dialog state.

        Returns:
            None: This function doesn't explicitly return a value. The dialog's state and results
                  are managed within the bot's context.
        """
        # Create a DialogSet and add the dialog to it
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        # Create a DialogContext from the DialogSet and TurnContext
        dialog_context = await dialog_set.create_context(turn_context)

        # Continue the current dialog if one is in progress
        results = await dialog_context.continue_dialog()

        # If no dialog is active, start the specified dialog
        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(dialog.id)
