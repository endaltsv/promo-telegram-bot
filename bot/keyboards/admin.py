from typing import Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.operations.category_operations import get_all_categories
from bot.locales.message_translations import message_data


async def admin_menu_back_button(language: str) -> InlineKeyboardMarkup:
    """
    Creates a keyboard with a single button "Back to admin menu" in the specified language.

    :param language: Language code for the button text.
    :return InlineKeyboardMarkup: Keyboard markup with the button.
    """
    builder = InlineKeyboardBuilder()
    button_text = message_data['back_menu'].get(language, "Back")
    builder.button(text=button_text, callback_data='back_admin_menu')

    return builder.as_markup()


async def admin_menu_keyboard(language: str) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard for the admin menu with various options.

    Parameters:
    language (str): The language code for the button texts.

    Returns:
    InlineKeyboardMarkup: An inline keyboard markup with admin menu options.
    """
    builder = InlineKeyboardBuilder()

    builder.button(text=message_data['add_category_button'][language], callback_data='admin_add_category')
    builder.button(text=message_data['delete_category_button'][language], callback_data='admin_delete_category')
    builder.button(text=message_data['send_a_message_button'][language], callback_data='admin_send_message')

    builder.button(text=message_data['change_welcomes'][language], callback_data='admin_change_welcome')
    builder.button(text=message_data['change_id_support_button'][language], callback_data='admin_update_id_support')
    builder.button(text=message_data['back_menu'][language], callback_data='back_menu')
    builder.adjust(2,1, repeat=True)

    return builder.as_markup()


async def create_category_keyboard(category_name: str, category_text: str,
                                   language: str) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard with "Yes" and "No" buttons for adding a category.

    Parameters:
    category_name (str): The name of the category.
    category_text (str): The text of the category.
    language (str): The language code for the button texts.

    Returns:
    InlineKeyboardMarkup: An inline keyboard markup with "Yes" and "No" buttons.
    """
    builder = InlineKeyboardBuilder()

    yes_text = message_data['yes'].get(language, "Yes")
    no_text = message_data['no'].get(language, "No")

    builder.button(text=yes_text, callback_data='add_category_success')
    builder.button(text=no_text, callback_data='back_admin_menu')
    return builder.as_markup()


async def create_categories_list_keyboard(language: str) -> Union[InlineKeyboardMarkup, bool]:
    """
    Build an inline keyboard with buttons for all categories.

    Args:
        language (str): The language code to use for the button labels.

    Returns:
        Union[InlineKeyboardMarkup, bool]: An InlineKeyboardMarkup with category buttons
        or False if no categories were found.
    """
    builder = InlineKeyboardBuilder()
    categories = await get_all_categories()

    if len(categories) == 0:
        return False

    for category in categories:
        builder.button(text=category.name, callback_data=f"delete_category_{category.id}")
    builder.button(text=message_data['back_menu'][language], callback_data="back_admin_menu")

    return builder.as_markup()
