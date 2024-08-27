from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.database.operations.user_operations import add_or_update_user


class UserUpdateMiddleware(BaseMiddleware):
    """
    Middleware for updating user information.

    This middleware updates user information
    (user ID, username, and last message ID) in the database
    before passing the event to the handler.

    Example:
    ```python
    from aiogram import Bot, Dispatcher
    from aiogram.contrib.middlewares.logging import LoggingMiddleware

    bot = Bot(token="TOKEN")
    dp = Dispatcher(bot)

    dp.middleware.setup(UserUpdateMiddleware())
    ```
    """
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        await add_or_update_user(event.from_user.id, event.from_user.username, event.from_user.first_name,
                                  event.message_id+1)
        return await handler(event, data)
