from aiogram.types import Message
from core.utils.FSM import FSM
from aiogram import Router, F, Bot
from core.keyboards.keyboards import (
    main_menu_keyboard,
    types_keyboard,
    offers_keyboard,
    geo_keyboard,
    languages_keyboard,
    main_menu_keyboard_admin,
    statistics_keyboard,
)
from aiogram.fsm.context import FSMContext
from core.filters.filter_for_back import IsNoneFilter
from core.utils import admins


router = Router()


@router.message(F.text == "◀️Назад", IsNoneFilter())
async def back_handler_10(message: Message, state: FSMContext):
    """В данном хендлере необходимо реализовать кнопку 'Назад'"""
    # await bot.delete_message(
    #     chat_id=message.chat.id, message_id=message.reply_to_message.message_id
    # )
    await message.delete()
    context_data = await state.get_data()  # Словарь
    curent_state = await state.get_state()  # Состояние бота
    match curent_state:
        case FSM.types:
            await state.set_state(FSM.main_menu)
            keyboard = (
                main_menu_keyboard_admin
                if message.from_user.id in admins
                else main_menu_keyboard
            )
            await message.answer(
                "Добро пожаловать в лучший генератор креативов на Нутру - <b>KreoPic Bot 🤖</b>\n\nЯ буду твоим верным помощником в заливах👾",
                reply_markup=keyboard,
            )
        case FSM.offers:
            await state.set_data(
                {key: value for key, value in context_data.items() if key != "type"}
            )
            await state.set_state(FSM.types)
            await message.answer(
                "Выбери вид креатива👨🏻‍💻",
                reply_markup=types_keyboard,
            )
        case FSM.geo:
            await state.set_data(
                {key: value for key, value in context_data.items() if key != "offer"}
            )
            await state.set_state(FSM.offers)
            await message.answer(
                "Выбери категорию оффера 🙇🏻‍♂️",
                reply_markup=offers_keyboard,
            )
        case FSM.languages:
            await state.set_data(
                {key: value for key, value in context_data.items() if key != "geo"}
            )
            if context_data["type"] == "Товарный":
                await state.set_state(FSM.offers)
                await message.answer(
                    "Выбери категорию оффера 🙇🏻‍♂️",
                    reply_markup=offers_keyboard,
                )
            else:
                await state.set_state(FSM.geo)
                await message.answer(
                    "Выбери ГЕО 🌎",
                    reply_markup=geo_keyboard,
                )
        case FSM.sizes:
            await state.set_data(
                {key: value for key, value in context_data.items() if key != "language"}
            )
            await state.set_state(FSM.languages)
            await message.answer(
                "Выбери язык 💆🏻‍♂️",
                reply_markup=languages_keyboard,
            )
        case FSM.feedback:
            await state.set_state(FSM.main_menu)
            keyboard = (
                main_menu_keyboard_admin
                if message.from_user.id in admins
                else main_menu_keyboard
            )
            await message.answer(
                "Добро пожаловать в лучший генератор креативов на Нутру - <b>KreoPic Bot 🤖</b>\n\nЯ буду твоим верным помощником в заливах👾",
                reply_markup=keyboard,
            )
        case FSM.statistics:
            await state.set_state(FSM.main_menu)

            await message.answer(
                "Добро пожаловать в лучший генератор креативов на Нутру - <b>KreoPic Bot 🤖</b>\n\nЯ буду твоим верным помощником в заливах👾",
                reply_markup=main_menu_keyboard_admin,
            )
        case FSM.report:
            await state.set_state(FSM.statistics)
            await message.answer("Выбери опцию", reply_markup=statistics_keyboard)


@router.message(F.text == "В начало🏠", IsNoneFilter())
async def home_handler_10(message: Message, state: FSMContext):
    """В данном хендлере необходимо реализовать кнопку 'Домой'"""
    await state.clear()
    await state.set_state(FSM.main_menu)
    keyboard = (
        main_menu_keyboard_admin
        if message.from_user.id in admins
        else main_menu_keyboard
    )
    await message.answer(
        "Добро пожаловать в лучший генератор креативов на Нутру - KreoPic Bot 🤖\n\nЯ буду твоим верным помощником в заливах👾",
        reply_markup=keyboard,
    )
