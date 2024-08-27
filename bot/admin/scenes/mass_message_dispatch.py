"""
This module handles the
process of sending a
message to all users in the
admin menu using the aiogram library.
It includes form state management for entering the message text,
sending the message to all users,
and updating the admin menu accordingly.
"""
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.admin.admin_utils import end_admin_function
from bot.admin.keyboards.admin_keyboards import admin_menu_back_button
from bot.config import bot, form_router
from bot.database.operations.user_operations import get_user_by_id, get_all_users
from bot.translations.locale import message_data


class MassMessageForm(StatesGroup):
    message_text = State()


async def initiate_mass_message_composition(chat_id, message_id, state: FSMContext):
    """
    Handles the user input for entering the text of a message to send to all users.

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
    await state.set_state(MassMessageForm.message_text)
    keyboard = await admin_menu_back_button(user.language)
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=message_data['admin_enter_text_send'][user.language],
                                reply_markup=keyboard)


@form_router.message(MassMessageForm.message_text)
async def process_and_dispatch_mass_message(message: Message, state: FSMContext):
    """
    Handles sending the message to all users based on the user input.

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
    await end_admin_function(message, user, function='send_message_to_all_users')



