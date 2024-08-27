from bot.config import bot
from bot.database.operations.category_operations import get_category_by_id
from bot.database.operations.user_operations import get_language_by_user_id
from bot.user.keyboards.keyboard_back_to_menu import keyboard_back_menu


async def show_text_by_category(category, chat_id, message_id):
    """
    Shows the text of a category to the user.

    :param category: int, The ID of the category to show.
    :param chat_id: int, The ID of the chat where the message was sent.
    :param message_id: int, The ID of the message containing the user input.
    :return: None
    """
    category = await get_category_by_id(category)
    language = await get_language_by_user_id(chat_id)

    await bot.edit_message_text(text=category.description,
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=await keyboard_back_menu(language))
