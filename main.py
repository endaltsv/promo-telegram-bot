import asyncio
import logging
import sys

from bot.admin.scenes.category_creation import confirm_category_creation, process_category_name
from bot.admin.scenes.welcome_text_update import set_welcome_text
from bot.admin.scenes.mass_message_dispatch import process_and_dispatch_mass_message
from bot.admin.scenes.support_id_management import process_and_apply_support_id
from bot.config import dp, bot
from bot.database.operations.category_operations import insert_initial_data
from bot.database.database_config import initialize_database
from bot.handlers.callback_handlers import callback_handler
from bot.handlers.start_command_handler import command_start_handler


async def main() -> None:
    """
    Main entry point for the bot. Creates necessary database tables,
    inserts initial data, and starts the bot's polling process.
    """
    await insert_initial_data()
    await initialize_database()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
