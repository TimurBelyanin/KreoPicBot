from aiogram.filters import Filter
from aiogram import Dispatcher


from typing import Any, Dict, Optional, Union
from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message, User


class DpFilter(Filter):
    def __init__(self, dp: Dispatcher):
        self.dp = dp

    async def __call__(self, message: Message) -> dict:  # [3]
        return {"dp": self.dp}
