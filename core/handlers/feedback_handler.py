from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from core.keyboards.keyboards import (
    main_menu_keyboard,
    feedback_keyboard,
)
from core.utils.FSM import FSM

from core.data_base.queries_core import AsyncCore
from core.utils.rating import calculate_rating, calculate_personal_position
from core.utils import admins, get_id_pack
import asyncio

router = Router()


@router.message(F.text == "Обратная связь✨", FSM.main_menu)
async def feedback(message: Message, state: FSMContext):
    await state.set_state(FSM.feedback)
    await message.answer(
        "Здесь вы можете сообщить о проблеме или предложить свою идею по улучшению✨\n\nВ случае, если вам не хватает определенного «формата» креативов - можете отправить нам пример, и мы обязательно его добавим🙏",
        reply_markup=feedback_keyboard,
    )


tasks_dict = {}


# Хендлер для обработки фотографий
@router.message(F.photo, FSM.feedback)
async def handler_photo(message: Message, state: FSMContext):
    async def send_thanks(user_id):
        # Ожидание перед отправкой сообщения
        await asyncio.sleep(1.5)
        await message.answer(
            "🫸Спасибо за ваше обращение🫷", reply_markup=main_menu_keyboard
        )
        tasks_dict.pop(user_id)
        await state.set_state(FSM.main_menu)

    from_user_id = message.from_user.id
    if from_user_id in tasks_dict and not tasks_dict[from_user_id].done():
        tasks_dict[from_user_id].cancel()

    # Создаём и сохраняем новую задачу
    tasks_dict[from_user_id] = asyncio.create_task(send_thanks(from_user_id))

    await message.bot.send_photo(
        chat_id=-4004038964,
        photo=message.photo[-1].file_id,
        caption=f"{message.caption} | {message.from_user.id}",
    )


@router.message(F.text, FSM.feedback)
async def text(message: Message, state: FSMContext):
    await message.bot.send_message(
        chat_id=-4004038964, text=f"{message.text} | {message.from_user.id}"
    )
    await state.set_state(FSM.main_menu)
    await message.answer("🫸Спасибо за ваше обращение🫷", reply_markup=main_menu_keyboard)


@router.message(FSM.feedback)
async def others(message: Message):
    await message.answer("‼️Пожалуйста, отправляйте только текст и изображения‼️")
