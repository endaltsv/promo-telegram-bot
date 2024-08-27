from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.config import bot, support_router
from bot.database.operations.setting_operations import get_settings
from bot.database.operations.user_operations import get_user_by_id
from bot.handlers.start import start
from bot.translations.locale import message_data
from bot.user.keyboards.answer_keyboard import answer_keyboard
from bot.user.keyboards.keyboard_back_to_menu import keyboard_back_menu


class Support(StatesGroup):
    message_text = State()


async def enter_message_text_to_support(chat_id, message_id, state: FSMContext):
    """
    Handles the user input for entering the text to send to support.

    :param chat_id: int, The ID of the chat where the message was sent.
    :param message_id: int, The ID of the message containing the user input.
    :param state: FSMContext, The state context for the finite state machine.
    :return: None
    """
    user = await get_user_by_id(chat_id)
    await state.set_state(Support.message_text)
    keyboard = await keyboard_back_menu(user.language)
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=message_data['enter_text_support'][user.language],
                                reply_markup=keyboard)


@support_router.message(Support.message_text)
async def sending_message_text(message: Message, state: FSMContext):
    """
    Handles sending the user's message to support.

    :param message: Message, The message containing the user input.
    :param state: FSMContext, The state context for the finite state machine.
    :return: None
    """
    user = await get_user_by_id(message.from_user.id)
    settings = await get_settings()
    await state.clear()
    try:
        # pylint: disable=line-too-long
        user_link = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
        message_text = \
            (f'<b>🪧 Пришло сообщение от {user_link}\n\n</b>'
             f'Текст сообщения: <code>{message.text}</code>') \
                if user.language == 'ru' else (f'<b>🪧 A message arrived from {user_link}\n\n</b>'
                                               f'Message text: <code>{message.text}</code>')

        keyboard = await answer_keyboard(user)
        await bot.send_message(chat_id=settings.support_id,
                               text=message_text,
                               reply_markup=keyboard,
                               parse_mode='HTML')

        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await start(chat_id=message.from_user.id,
                    message_id=user.last_message,
                    extra_text=message_data['success'][user.language]+'\n\n')
    except Exception as e:
        print(e)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await start(chat_id=message.from_user.id,
                    message_id=user.last_message,
                    extra_text=message_data['error'][user.language] + '\n\n')
