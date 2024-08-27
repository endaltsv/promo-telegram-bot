from typing import Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.operations.category_operations import get_all_categories
from bot.translations.locale import message_data


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
