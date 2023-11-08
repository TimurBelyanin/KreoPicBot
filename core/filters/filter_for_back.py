from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter
from aiogram.types import Message
from core.utils.FSM import FSM


class IsNoneFilter(BaseFilter):  # [1]
    async def __call__(self, message: Message, state: FSMContext) -> bool:  # [3]
        return await state.get_state() not in [None, FSM.main_menu]
