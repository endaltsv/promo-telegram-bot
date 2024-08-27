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
class Form(StatesGroup):
    name_category = State()
    text_category = State()


async def start_category_creation_flow(chat_id, message_id, state: FSMContext):
    """
    Handles the user input for entering the name of a category in the category adding form.

    Parameters:
    chat_id (int): The ID of the chat where the message was sent.
    message_id (int): The ID of the message containing the user input.
    state (FSMContext): The state context for the finite state machine.

    Returns:
    None
    """
    user = await get_user_by_id(chat_id)
    if not user.is_admin:
        return
    await state.set_state(Form.name_category)
    keyboard = await admin_menu_back_button(user.language)
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=message_data['admin_enter_name_category'][user.language],
                                reply_markup=keyboard)


@form_router.message(Form.name_category)
async def process_category_name(message: Message, state: FSMContext):
    """
    Handles the user input for entering the text of a category in the category adding form.

    Parameters:
    message (Message): The message containing the user input.
    state (FSMContext): The state context for the finite state machine.

    Returns:
    None
    """
    user = await get_user_by_id(message.from_user.id)
    if not user.is_admin:
        return

    await state.update_data(name_category=message.text)
    await state.set_state(Form.text_category)
    keyboard = await admin_menu_back_button(user.language)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id)

    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id=user.last_message,
                                text=message_data['admin_enter_text_category'][user.language],
                                reply_markup=keyboard)


@form_router.message(Form.text_category)
async def confirm_category_creation(message: Message, state: FSMContext):
    """
    Handles the user confirmation for adding a category in the category adding form.

    Parameters:
    message (Message): The message containing the user confirmation.
    state (FSMContext): The state context for the finite state machine.

    Returns:
    None
    """
    user = await get_user_by_id(message.from_user.id)
    if not user.is_admin:
        return

    data = await state.get_data()
    await state.update_data(text_category=message.text)
    # await state.clear()

    full_text_message = (
        message_data['admin_confirm_add_category'][user.language] +
        (
            "\n\n"
            f"<b>Название категории:</b> <code>{data['name_category']}</code>\n"
            f"<b>Текст категории:</b> <code>{message.text}</code>"
        )
        if user.language == 'ru' else
        (
                message_data['admin_confirm_add_category'][user.language] +
                (
                    "\n\n"
                    f"<b>Category name:</b> <code>{data['name_category']}</code>\n"
                    f"<b>Category text:</b> <code>{message.text}</code>"
                )
        )
    )

    keyboard = await create_category_keyboard(data['name_category'],
                                              message.text,
                                              user.language)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id)
    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id=user.last_message,
                                text=full_text_message,
                                reply_markup=keyboard)


async def finalize_category_creation(chat_id, message_id, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    name_category, text_category = data['name_category'], data['text_category']

    user = await get_user_by_id(chat_id)
    if not user.is_admin:
        return

    try:
        await add_category(category_name=name_category,
                           text=text_category)
        await admin_menu(chat_id, message_id,
                         extra_text=message_data['success'][user.language] + '\n\n')
    except Exception as e:
        print(e)
        await admin_menu(chat_id, message_id,
                         extra_text=message_data['error'][user.language] + '\n\n')