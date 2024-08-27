from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.translations.locale import message_data


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
