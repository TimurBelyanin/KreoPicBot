from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from core.keyboards.keyboards import (
    main_menu_keyboard,
    types_keyboard,
    offers_keyboard,
    geo_keyboard,
    languages_keyboard,
    sizes_keyboard,
)
from core.utils.FSM import FSM

router = Router()


@router.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext):
    await state.set_state(FSM.main_menu)
    await message.answer(
        "Добро пожаловать в лучший генератор креативов на Нутру - <b>KreoPic Bot 🤖</b>\n\nТвой верный помощник в заливах👾",
        reply_markup=main_menu_keyboard,
    )


@router.message(F.text == "Сгенерировать🤖", FSM.main_menu)
async def types(message: Message, state: FSMContext):
    # await state.update_data(type=message.text)
    await state.set_state(FSM.types)
    await message.answer(
        "Выбери вид креатива👨🏻‍💻",
        reply_markup=types_keyboard,
    )


@router.message(F.text.in_(["Товарный 💊", "Классический👨🏻‍⚕️"]), FSM.types)
async def offers(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    await state.set_state(FSM.offers)
    await message.answer(
        "Выбери категорию оффера 🙇🏻‍♂️",
        reply_markup=offers_keyboard,
    )


@router.message(
    F.text.in_(
        [
            "Похудение🍏",
            "Паразиты🦠",
            "Гипертония🫀",
            "Диабет👅",
            "Простатит🥚",
            "Потенция🍌",
            "Суставы🦵🏻",
            "Омоложение👶🏻",
        ]
    ),
    FSM.offers,
)
async def geo(message: Message, state: FSMContext):
    await state.update_data(offer=message.text)
    await state.set_state(FSM.geo)
    await message.answer(
        "Выбери ГЕО 🌎",
        reply_markup=geo_keyboard,
    )


# @router.message(F.text.in_(["Европа👨🏼", "Африка🧑🏿‍🦱"]), FSM.geo)
# @logger.catch
# async def languages(message: Message, state: FSMContext, bot: Bot):
#     await state.update_data(hair=message.text)
#     context_data = await state.get_data()
#     await state.clear()
#     sent_message = await bot.send_sticker(
#         chat_id=message.from_user.id,
#         sticker="CAACAgEAAxkBAAEKNcBk9GOLTc0Pbz3mSTj1cNDK6Kqm1gACLQIAAqcjIUQ9QDDJ7YO0tjAE",
#     )
#     await asyncio.sleep(1)
#     await message.answer(
#         f"Well done mate!\nHere're your parameters:\n1)food: {context_data['food']}\n"
#         f"2)drink: {context_data['beverage']}\n"
#         f"3)profession: {context_data['profession']}\n"
#         f"4)hair: {context_data['hair']}",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     await sent_message.delete()


@router.message(
    F.text.in_(["Европа👨🏼", "Африка🧑🏿‍🦱", "Латам👨🏽‍🦱", "Азия👨🏽‍🦲"]), FSM.geo
)
async def languages(message: Message, state: FSMContext):
    await state.update_data(geo=message.text)
    await state.set_state(FSM.languages)
    await message.answer(
        "Выбери язык 💆🏻‍♂️",
        reply_markup=languages_keyboard,
    )


@router.message(
    F.text.in_(["RU🇷🇺", "ES🇪🇸", "EN🇬🇧", "IT🇮🇹", "BG🇧🇬", "RO🇷🇴", "CZ🇨🇿", "FR🇫🇷"]),
    FSM.languages,
)
async def sizes(message: Message, state: FSMContext):
    await state.update_data(language=message.text)
    await state.set_state(FSM.sizes)
    await message.answer(
        "Выбери размер пака 💁🏻‍♂️",
        reply_markup=sizes_keyboard,
    )


@router.message(
    F.text.in_(["5 (XS)", "10 (S)", "20 (M)", "30 (L)", "50 (XL)", "100 (MAX)"]),
    FSM.sizes,
)
async def finish(message: Message, state: FSMContext):
    await state.update_data(size=message.text)
    context_data = await state.get_data()
    await state.clear()
    ################ Bussiness-logic
    # await message.answer(f"{context_data}", reply_markup=ReplyKeyboardRemove())
    print(context_data)
    await message.answer("Отсоси бля", reply_markup=ReplyKeyboardRemove())
