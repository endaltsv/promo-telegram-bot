from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message


class DeleteMessageMiddleware(BaseMiddleware):
    """
    Middleware for deleting the message after processing it.
    """
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        await event.bot.delete_message(chat_id=event.chat.id, message_id=event.message_id)
        return await handler(event, data)
