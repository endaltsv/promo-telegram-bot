"""
This module handles the
process of updating the
support ID in the admin settings
using the aiogram library.
It includes form state management for entering
the support ID,
setting the new support
ID in the database, and updating the admin menu accordingly.
"""
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.admin.admin_utils import end_admin_function
from bot.keyboards.admin import admin_menu_back_button
from bot.admin.admin_menu import admin_menu
from bot.config import bot, support_router
from bot.database.operations.setting_operations import update_support_id

from bot.database.operations.user_operations import get_user_by_id
from bot.locales.message_translations import message_data


class SupportIDUpdateForm(StatesGroup):
    support_id = State()


async def initiate_support_id_update(chat_id, message_id, state: FSMContext):
    """
    Handles the user input for entering the support ID in the admin settings.

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
    await state.set_state(SupportIDUpdateForm.support_id)
    keyboard = await admin_menu_back_button(user.language)
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=message_data['enter_changing_id_support'][user.language],
                                reply_markup=keyboard)


@support_router.message(SupportIDUpdateForm.support_id)
async def process_and_apply_support_id(message: Message, state: FSMContext):
    """
    Handles setting the new support ID in the admin settings.

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

    await end_admin_function(message, user, function='update_support_id')
