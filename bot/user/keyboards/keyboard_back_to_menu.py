from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.translations.locale import message_data


async def keyboard_back_menu(language='ru'):
    """
    Creates an inline keyboard with a "Back" button.

    :param language: The language code for the button text (default is 'ru').
    :return: InlineKeyboardMarkup: An inline keyboard markup with a "Back" button.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text=message_data['back_menu'][language], callback_data="back_menu")

    return builder.as_markup()
