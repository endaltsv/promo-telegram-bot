"""
This module handles the deletion
of categories in the admin menu
using the aiogram library.
It includes operations to display a
list of categories for deletion,
delete a selected category,
and update the admin menu accordingly.
"""
from bot.admin.admin_utils import end_admin_function
from bot.admin.keyboards.admin_keyboards import admin_menu_back_button
from bot.admin.keyboards.category_keyboards import create_categories_list_keyboard
from bot.admin.admin_menu import admin_menu
from bot.config import bot
from bot.database.operations.category_operations import delete_category_by_id
from bot.database.operations.user_operations import get_user_by_id
from bot.translations.locale import message_data


async def display_deletable_categories(chat_id, message_id):
    """
    Displays a list of categories that can be deleted and handles the deletion process.

    Parameters:
    chat_id (int): The ID of the chat where the message was sent.
    message_id (int): The ID of the message containing the user input.

    Returns:
    None
    """
    user = await get_user_by_id(chat_id)
    if not user.is_admin:
        return

    keyboard = await create_categories_list_keyboard(user.language)

    if not keyboard:
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=message_data['not_information'][user.language],
                                    reply_markup=await admin_menu_back_button(user.language))
        return
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=message_data['which_category_to_delete'][user.language],
                                reply_markup=keyboard)


async def execute_category_deletion(chat_id, message_id, category_id):
    """
    Deletes a category based on the provided category ID.

    Parameters:
    chat_id (int): The ID of the chat where the message was sent.
    message_id (int): The ID of the message containing the user input.
    category_id (int): The ID of the category to be deleted.

    Returns:
    None
    """
    user = await get_user_by_id(chat_id)
    await end_admin_function(function='delete_category_by_id', category_id=category_id, chat_id=chat_id, message_id=message_id)

