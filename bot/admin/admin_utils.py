from typing import Optional, Callable, Dict, Any

from aiogram.types import Message

from bot.admin.admin_menu import admin_menu
from bot.config import bot
from bot.database.operations.category_operations import delete_category_by_id
from bot.database.operations.setting_operations import update_support_id, update_welcome_text
from bot.database.operations.user_operations import get_all_users, get_user_by_id
from bot.locales.message_translations import message_data

AdminFunction = Callable[[str], Any]

ADMIN_FUNCTIONS: Dict[str, AdminFunction] = {
    'update_support_id': update_support_id,
    'update_welcome_text': update_welcome_text,
    'delete_category_by_id': delete_category_by_id,
    'send_message_to_all_users': lambda x: distribute_message(x)
}


async def execute_admin_action(
        message: Optional[Message] = None,
        user: Optional[Any] = None,
        action: str = '',
        category_id: Optional[int] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None
) -> None:
    """
    Executes an admin action and updates the admin menu accordingly.

    Args:
        message (Optional[Message]): The message object, if available.
        user (Optional[Any]): The user object, if available.
        action (str): The action to be executed.
        category_id (Optional[int]): The category ID, if applicable.
        chat_id (Optional[int]): The chat ID, if not provided in the message.
        message_id (Optional[int]): The message ID, if not provided in the message.
    """
    chat_id, message_id = extract_chat_message_ids(message, chat_id, message_id)
    user = user or await get_user_by_id(chat_id)

    try:
        if action not in ADMIN_FUNCTIONS:
            raise KeyError(f"Action '{action}' not found")

        result = await execute_function(ADMIN_FUNCTIONS, action, message, category_id)
        extra_text = build_result_message(action, result, user.language)
        await admin_menu(chat_id, user.last_message, extra_text=extra_text)
    except Exception as e:
        print(f"Error executing admin action '{action}': {e}")
        await admin_menu(chat_id, user.last_message, extra_text=message_data['error'][user.language] + '\n\n')


def extract_chat_message_ids(message: Optional[Message], chat_id: Optional[int], message_id: Optional[int]) -> tuple:
    """Extracts chat and message IDs from the message object or uses provided values."""
    if message:
        return message.from_user.id, message.message_id
    return chat_id, message_id


async def execute_function(functions: Dict[str, AdminFunction], action: str, message: Message,
                           category_id: Optional[int]) -> Any:
    """Executes the specified admin function with appropriate arguments."""
    if action == 'delete_category_by_id':
        return await functions[action](category_id)
    return await functions[action](message.text)


def build_result_message(action: str, result: Any, language: str) -> str:
    """Builds a result message based on the executed action and its result."""
    if action == 'send_message_to_all_users':
        return message_data['success_sended'][language] + result + '\n\n'
    return message_data['success'][language] + '\n\n'


async def distribute_message(message_text: str) -> str:
    """Distributes a message to all users and returns a summary of the operation."""
    users = await get_all_users()
    send_count = sum(1 for user in users if await try_send_message(user.user_id, message_text))
    return f'[{send_count}/{len(users)}]'


async def try_send_message(user_id: int, message_text: str) -> bool:
    """Attempts to send a message to a user and returns the success status."""
    try:
        await bot.send_message(chat_id=user_id, text=message_text)
        return True
    except Exception as e:
        print(f"Failed to send message to user {user_id}: {e}")
        return False
