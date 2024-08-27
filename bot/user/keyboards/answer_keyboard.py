from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.translations.locale import message_data


async def answer_keyboard(user):
    """
    Creates an inline keyboard with an "Answer" button.

    :return: InlineKeyboardMarkup: An inline keyboard markup with an "Answer" button.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text=message_data['answer'][user.language], callback_data=f"answer|{user.user_id}")

    return builder.as_markup()
