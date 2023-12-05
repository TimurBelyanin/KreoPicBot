from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from core.filters.filter_for_back import IsNoneFilter
from core.keyboards.keyboards import (
    main_menu_keyboard,
    feedback_keyboard,
)
from core.utils.FSM import FSM

from core.data_base.queries_core import AsyncCore
from core.utils.rating import calculate_rating, calculate_personal_position
from core.utils import admins, get_id_pack
import asyncio
from core.utils.rating import username_func


router = Router()


async def left_time(message: Message, dp: Dispatcher):
    return await dp.get("redis").ttl(name=str(message.from_user.id) + "timer") // 60


async def timer_feedback_check(message: Message, dp: Dispatcher):
    """Function checks whether there is a set timer or not"""
    if await dp.get("redis").get(name=str(message.from_user.id) + "timer"):
        return True


async def timer_feedback_set(message: Message, dp: Dispatcher):
    """Function sets timer for 1 hour after getting feedback so that there is no abusing"""
    await dp.get("redis").set(
        name=str(message.from_user.id) + "timer", value="bebra", ex=3600
    )


@router.message(F.text == "Обратная связь✨", IsNoneFilter())
async def feedback(message: Message, state: FSMContext):
    await state.set_state(FSM.feedback)
    await message.answer(
        "Здесь вы можете сообщить о проблеме или предложить свою идею по улучшению✨\n\nВ случае, если вам не хватает определенного «формата» креативов - можете отправить нам пример, лучшие мы добавим 🙏",
        reply_markup=feedback_keyboard,
    )


# Global variable :|
tasks_dict = {}


# Хендлер для обработки фотографий
async def handler_photo(message: Message, state: FSMContext, dp: Dispatcher):
    async def send_thanks(user_id):
        # Ожидание перед отправкой сообщения
        await asyncio.sleep(1.5)
        await message.bot.send_sticker(
            chat_id=message.chat.id,
            sticker="CAACAgEAAxkBAAEK5lNlbsZQPNtSK6FM5dHzFmjhO6xeSwAC-gEAAoyxIER4c3iI53gcxDME",
            reply_markup=main_menu_keyboard,
        )
        await timer_feedback_set(message, dp)
        tasks_dict.pop(user_id)
        await state.clear()

    if await timer_feedback_check(message, dp):
        await message.answer(
            f"жди еще {await left_time(message, dp)} минут прежде чем написать",
            reply_markup=main_menu_keyboard,
        )
        await state.clear()
    else:
        from_user_id = message.from_user.id
        if from_user_id in tasks_dict and not tasks_dict[from_user_id].done():
            tasks_dict[from_user_id].cancel()

        # Создаём и сохраняем новую задачу
        tasks_dict[from_user_id] = asyncio.create_task(send_thanks(from_user_id))

        await message.bot.send_photo(
            chat_id=-4004038964,
            photo=message.photo[-1].file_id,
            caption=f"{message.caption} | @{await username_func(message.from_user.id, message.bot)}",
        )


async def handler_text(message: Message, state: FSMContext, dp: Dispatcher):
    if await timer_feedback_check(message, dp):
        await message.answer(
            f"жди еще {await left_time(message, dp)} минут прежде чем написать",
            reply_markup=main_menu_keyboard,
        )
        await state.clear()
    else:
        await message.bot.send_message(
            chat_id=-4004038964,
            text=f"{message.text} | @{await username_func(message.from_user.id, message.bot)}",
        )
        await timer_feedback_set(message, dp)

        await message.bot.send_sticker(
            chat_id=message.chat.id,
            sticker="CAACAgEAAxkBAAEK5lNlbsZQPNtSK6FM5dHzFmjhO6xeSwAC-gEAAoyxIER4c3iI53gcxDME",
            reply_markup=main_menu_keyboard,
        )

        await state.clear()


@router.message(FSM.feedback)
async def others(message: Message):
    await message.answer("‼️Пожалуйста, отправляйте только текст и изображения‼️")
