"""
This module handles the updating
of the welcome text in the admin
settings using the aiogram library.
It includes form state management for entering and setting the welcome text,
as well as operations to update the welcome
text in the database and update the admin menu.
"""

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.admin.admin_utils import end_admin_function
from bot.admin.keyboards.admin_keyboards import admin_menu_back_button
from bot.config import bot, form_router

from bot.database.operations.user_operations import get_user_by_id
from bot.translations.locale import message_data


class WelcomeTextForm(StatesGroup):
    welcome_text = State()


async def initiate_welcome_text_update(chat_id, message_id, state: FSMContext):
    """
    Handles the user input for entering the welcome text in the admin settings.

    Parameters:
    chat_id (int): The ID of the chat where the message was sent.
    message_id (int): The ID of the message containing the user input.
    state (FSMContext): The state context for the finite state machine.

    Returns:
    None
    """
    user = await get_user_by_id(chat_id)
    if not user.is_admin:
        return

    await state.set_state(WelcomeTextForm.welcome_text)

    keyboard = await admin_menu_back_button(user.language)
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=message_data['admin_enter_text_welcome'][user.language],
                                reply_markup=keyboard)


@form_router.message(WelcomeTextForm.welcome_text)
async def set_welcome_text(message: Message, state: FSMContext):
    """
    Handles setting the new welcome text in the admin settings.

    Parameters:
    message (Message): The message containing the user input.
    state (FSMContext): The state context for the finite state machine.

    Returns:
    None
    """

    user = await get_user_by_id(message.from_user.id)
    if not user.is_admin:
        return

    await state.clear()
    await end_admin_function(message, user, function='update_welcome_text')

