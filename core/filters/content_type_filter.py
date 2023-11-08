from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter
from aiogram.types import Message, ContentType, Update
from core.utils.FSM import FSM


class ContentTypeFilter(BaseFilter):  # [1]
    async def __call__(self, update: Update, state: FSMContext) -> bool:  # [3]
        return update.content_type == ContentType.SUCCESSFUL_PAYMENT
