from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.config import router, bot
from bot.database.operations.setting_operations import get_settings
from bot.database.operations.user_operations import get_user_by_id
from bot.locales.message_translations import message_data
from bot.keyboards.user import keyboard_start


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Handles the start command message from users.

    :param message: The message object containing the command.
    :return: None
    """
    await start(message=message,
                chat_id=message.from_user.id,
                message_id=message.message_id)


async def start(message=None, chat_id=None, message_id=None, extra_text=''):
    """
    Handles the start command for the bot.

    :param message: The message object that triggered the command (optional).
    :param chat_id: The ID of the chat where the message was sent (optional).
    :param message_id: The ID of the message containing the command (optional).
    :param extra_text: Additional text to include in the message (optional).
    :return: None
    """
    user = await get_user_by_id(chat_id)
    keyboard = await keyboard_start(user.language, user.is_admin)

    settings = await get_settings()

    start_message = message_data['start'][user.language]
    try:
        if settings is not None or settings.start_message is not None:
            start_message = settings.welcome_message
    except Exception as e:
        print(e)


    if message:
        await bot.send_message(chat_id=message.from_user.id,
                               text=extra_text+start_message,
                               reply_markup=keyboard.as_markup())
        return

    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=extra_text+start_message,
                                reply_markup=keyboard.as_markup())
