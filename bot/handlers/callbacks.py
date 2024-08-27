from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.admin.scenes.category_creation import start_category_creation_flow, finalize_category_creation
from bot.admin.admin_menu import admin_menu
from bot.admin.scenes.welcome_text_update import initiate_welcome_text_update
from bot.admin.scenes.category_deletion import display_deletable_categories, execute_category_deletion
from bot.admin.scenes.mass_message_dispatch import initiate_mass_message_composition
from bot.admin.scenes.admin_user_response import initiate_admin_response
from bot.admin.scenes.support_id_management import initiate_support_id_update
from bot.config import router
from bot.database.operations.user_operations import update_language_by_user_id
from bot.handlers.start import start
from bot.user.scenes.send_message_to_support import enter_message_text_to_support
from bot.user.view.show_details import show_text_by_category


@router.callback_query()
async def callback_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Handle callback queries from users.
    """
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    data = callback_query.data

    async def show_text_by_category_action():
        await show_text_by_category(data.split("show_")[1], chat_id, message_id)

    async def back_menu_action():
        await start(chat_id=chat_id, message_id=message_id)

    async def change_language_action():
        await update_language_by_user_id(chat_id)
        await start(chat_id=chat_id, message_id=message_id)

    async def send_support_action():
        await enter_message_text_to_support(chat_id=chat_id, message_id=message_id, state=state)

    async def admin_panel_action():
        await admin_menu(chat_id=chat_id, message_id=message_id)

    async def admin_add_category_action():
        await start_category_creation_flow(chat_id=chat_id, message_id=message_id, state=state)

    async def admin_change_welcome_action():
        await initiate_welcome_text_update(chat_id=chat_id, message_id=message_id, state=state)

    async def admin_send_message_action():
        await initiate_mass_message_composition(chat_id=chat_id, message_id=message_id, state=state)

    async def admin_update_id_support_action():
        await initiate_support_id_update(chat_id=chat_id, message_id=message_id, state=state)

    async def admin_delete_category_action():
        await display_deletable_categories(chat_id=chat_id, message_id=message_id)

    async def delete_category_action():
        category_id = data.split("delete_category_")[1]
        await execute_category_deletion(chat_id=chat_id, message_id=message_id, category_id=category_id)

    async def back_admin_menu_action():
        await admin_menu(chat_id, message_id)

    async def answer_action():
        user_to_answer = data.split("answer|")[1]
        await initiate_admin_response(chat_id=chat_id, message_id=message_id, state=state, user_to_answer=user_to_answer)

    async def add_category_success_action():
        await finalize_category_creation(chat_id=chat_id, message_id=message_id, state=state)

    action_map = {
        "show_": show_text_by_category_action,
        "back_menu": back_menu_action,
        "change_language": change_language_action,
        "send_support": send_support_action,
        "admin-panel": admin_panel_action,
        "admin_add_category": admin_add_category_action,
        "admin_change_welcome": admin_change_welcome_action,
        "admin_send_message": admin_send_message_action,
        "admin_update_id_support": admin_update_id_support_action,
        "admin_delete_category": admin_delete_category_action,
        "delete_category_": delete_category_action,
        "back_admin_menu": back_admin_menu_action,
        "answer": answer_action,
        "add_category_success": add_category_success_action,
    }

    # Execute the corresponding action
    for action, func in action_map.items():
        if data.startswith(action):
            await func()
            await callback_query.answer()
            return

    await callback_query.answer()
