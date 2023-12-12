from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    cache = TTLCache(maxsize=10_000, ttl=1)  # Единое время для всех типов сообщений

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        chat_id = event.chat.id
        if chat_id in self.cache:
            return  # Пропустить обработку сообщения, если оно уже в кэше
        else:
            self.cache[chat_id] = None  # Добавить chat_id в кэш
        return await handler(event, data)
