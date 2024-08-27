"""
This module contains a function to
edit the admin menu message with the
provided `extra_text` appended.
"""
from bot.keyboards.admin import admin_menu_keyboard
from bot.config import bot
from bot.database.operations.user_operations import get_user_by_id
from bot.locales.message_translations import message_data


async def admin_menu(chat_id, message_id, extra_text=''):
    """
    Edits the admin menu message with the provided `extra_text` appended.

    :param chat_id: The ID of the chat where the message is located.
    :param message_id: The ID of the message to be edited.
    :param extra_text: Additional text to be appended to the message. Default is an empty string.

    :return: None
    """
    user = await get_user_by_id(chat_id)
    if not user.is_admin:
        return

    keyboard = await admin_menu_keyboard(user.language)
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=keyboard,
                                text=extra_text + message_data['admin_info_menu'][user.language])
