from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.operations.category_operations import get_all_categories
from bot.locales.message_translations import message_data


async def answer_keyboard(user):
    """
    Creates an inline keyboard with an "Answer" button.

    :return: InlineKeyboardMarkup: An inline keyboard markup with an "Answer" button.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text=message_data['answer'][user.language], callback_data=f"answer|{user.user_id}")

    return builder.as_markup()


async def keyboard_back_menu(language='ru'):
    """
    Creates an inline keyboard with a "Back" button.

    :param language: The language code for the button text (default is 'ru').
    :return: InlineKeyboardMarkup: An inline keyboard markup with a "Back" button.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text=message_data['back_menu'][language], callback_data="back_menu")

    return builder.as_markup()


async def keyboard_start(language, is_admin):
    """
    Creates an inline keyboard for the start menu with category buttons, a support button,
    a language change button, and an admin button if the user is an admin.

    :param language: The language code for the button texts.
    :param is_admin: A boolean indicating if the user is an admin.
    :return: InlineKeyboardBuilder: An inline keyboard markup for the start menu.
    """
    categories = await get_all_categories()

    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category.name, callback_data=f"show_{category.id}")
    builder.button(text=message_data['send_support'][language], callback_data='send_support')
    builder.button(text=message_data['change_language_button'][language],
                   callback_data="change_language")
    if is_admin:
        builder.button(text=message_data['admin_button'][language], callback_data="admin-panel")

    builder.adjust(1,1,2)

    return builder
