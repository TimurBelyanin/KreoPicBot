from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, F
from aiogram.types import Message
from cachetools import TTLCache
from aiogram.dispatcher.flags import get_flag


class ThrottlingMiddleware(BaseMiddleware):
    cache = TTLCache(maxsize=10_000, ttl=0.5)  # Единое время для всех типов сообщений

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.type == "private":
            chat_id = event.chat.id
            if chat_id in self.cache:
                return  # Пропустить обработку сообщения, если оно уже в кэше
            elif get_flag(data, "bebra"):
                return await handler(event, data)
            else:
                self.cache[chat_id] = None  # Добавить chat_id в кэш
                return await handler(event, data)

            # print(handler(event, data))
