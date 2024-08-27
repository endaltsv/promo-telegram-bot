"""
This module handles the category addition process in the admin
menu using the aiogram library. It includes form state management
for entering category names and texts, as well as operations to add
the category to the database and update the admin menu.
"""
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot.keyboards.admin import admin_menu_back_button, create_category_keyboard
from bot.admin.admin_menu import admin_menu
from bot.config import bot, form_router
from bot.database.operations.category_operations import add_category
from bot.database.operations.user_operations import get_user_by_id
from bot.locales.message_translations import message_data


# pylint: disable=too-few-public-methods
class AdminResponseForm(StatesGroup):
    text_for_answer = State()


async def initiate_admin_response(chat_id, message_id, state: FSMContext, user_to_answer):
    user = await get_user_by_id(chat_id)
    if not user.is_admin:
        return

    await state.set_state(AdminResponseForm.text_for_answer)
    await state.update_data(chat_id=chat_id, message_id=message_id, user_to_answer=user_to_answer)
    keyboard = await admin_menu_back_button(user.language)
    await bot.send_message(chat_id=chat_id,
                           text=message_data['enter_text_answer_admin'][user.language],
                           reply_markup=keyboard)


@form_router.message(AdminResponseForm.text_for_answer)
async def process_and_send_admin_response(message: Message, state: FSMContext):
    user = await get_user_by_id(message.from_user.id)
    if not user.is_admin:
        return
    data = await state.get_data()
    await state.clear()

    await bot.delete_messages(chat_id=message.from_user.id,
                              message_ids=[message.message_id - 1, message.message_id])

    await bot.send_message(chat_id=message.from_user.id,
                           text=message_data['success'][user.language] + '\n\n'
                                + message_data['answer_text'][user.language] + f" <code>{message.text}</code>",
                           reply_to_message_id=data['message_id'])

    await bot.send_message(chat_id=data['user_to_answer'],
                           text=message_data['answer_user_text'][user.language] + '\n\n'
                                + message_data['answer_text'][user.language] + f" <code>{message.text}</code>")
