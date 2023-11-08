from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message
from aiogram.fsm.storage.redis import RedisStorage, StorageKey
import asyncio


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware for throttling"""

    def __init__(self, storage: RedisStorage, bot: Bot):
        self.storage = storage
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user = str(event.from_user.id)
        check_user = await self.storage.redis.get(name=user)
        if check_user:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=user, value=0, px=400)
                await asyncio.sleep(0)  # Даем время Redis выполнить операцию записи
            return
        await self.storage.redis.set(name=user, value=1, px=400)
        await asyncio.sleep(0)  # Даем время Redis выполнить операцию записи
        return await handler(event, data)
