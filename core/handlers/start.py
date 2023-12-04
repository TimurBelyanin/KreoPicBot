from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from core.keyboards.keyboards import (
    main_menu_keyboard,
    types_keyboard,
    offers_keyboard,
    geo_keyboard,
    languages_keyboard,
    sizes_keyboard,
    main_menu_keyboard_admin,
    tb_keyboard,
    feedback_keyboard,
)
from core.utils.FSM import FSM

from core.data_base.queries_core import AsyncCore
from core.utils.rating import calculate_rating, calculate_personal_position
from core.utils import admins, get_id_pack
import tempfile
import pandas as pd
import os


router = Router()


@router.message(Command(commands=["start"]), flags={"chat_action": "typing"})
async def start(message: Message, state: FSMContext):
    await state.set_state(FSM.main_menu)
    keyboard = (
        main_menu_keyboard_admin
        if message.from_user.id in admins
        else main_menu_keyboard
    )
    if not await AsyncCore.does_user_exist(message.from_user.id):
        await AsyncCore.insert_user(user_id=message.from_user.id, kreo=0)
    await message.answer(
        "Добро пожаловать в лучший генератор креативов на Нутру - <b>KreoPic Bot 🤖</b>\n\nТвой верный помощник в заливах👾",
        reply_markup=keyboard,
    )


# @router.message(F.text == "Обратная связь✨", FSM.main_menu)
# async def feedback(message: Message, state: FSMContext):
#     await state.set_state(FSM.feedback)
#     await message.answer(
#         "Здесь вы можете сообщить о проблеме или предложить свою идею по улучшению✨\n\nВ случае, если вам не хватает определенного «формата» креативов - можете отправить нам пример, и мы обязательно его добавим🙏",
#         reply_markup=feedback_keyboard,
#     )

#
# @router.message(
#     F.from_user.id.in_({*admins}), F.text == "Сгенерировать🤖", FSM.main_menu
# )
# async def test_or_buy(message: Message, state: FSMContext):
#     await state.set_state(FSM.TB)
#     await message.answer("Выбери характер операции", reply_markup=tb_keyboard)


########################################################################################################################
@router.message(F.text == "Сгенерировать🤖", FSM.main_menu)
async def types(message: Message, state: FSMContext):
    await state.set_state(FSM.types)
    await message.answer(
        "Выбери вид креатива👨🏻‍💻",
        reply_markup=types_keyboard,
    )


@router.message(F.text.in_(["Товарный 💊", "Классический👨🏻‍⚕️"]), FSM.types)
async def offers(message: Message, state: FSMContext):
    await state.update_data(type=message.text.rstrip(" 💊👨🏻‍⚕️"))
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
    await state.update_data(offer=message.text.rstrip("🍏🦠🫀👅🥚🍌🦵🏻👶🏻"))
    data = await state.get_data()
    if data["type"] == "Товарный":
        await state.set_state(FSM.languages)
        await message.answer(
            "Выбери язык 💆🏻‍♂️",
            reply_markup=languages_keyboard,
        )
    else:
        await state.set_state(FSM.geo)
        await message.answer(
            "Выбери ГЕО 🌎",
            reply_markup=geo_keyboard,
        )


@router.message(
    F.text.in_(["Европа👨🏼", "Африка🧑🏿‍🦱", "Латам👨🏽‍🦱", "Азия👨🏽‍🦲"]),
    FSM.geo,
)
async def languages(message: Message, state: FSMContext):
    await state.update_data(geo=message.text.rstrip("👨🏼🧑🏿‍🦱👨🏽‍🦱👨🏽‍🦲"))
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
    await state.update_data(language=message.text.rstrip("🇷🇺🇪🇸🇬🇧🇮🇹🇧🇬🇷🇴🇨🇿🇫🇷"))
    await state.set_state(FSM.sizes)
    await message.answer(
        "Выбери размер пака 💁🏻‍♂️",
        reply_markup=sizes_keyboard,
    )


async def finish(message: Message, state: FSMContext, dp: Dispatcher, bot: Bot):
    redis = dp.get("redis")
    await state.update_data(size=int(message.text.split()[0]))
    context_data = await state.get_data()
    await state.clear()
    ################ Bussiness-logic
    # await message.answer(f"{context_data}", reply_markup=ReplyKeyboardRemove())
    # We need to update the rating, but firstly add kreo to user and purchases
    async for i in redis.scan_iter(match="*position"):
        await redis.delete(i)

    await AsyncCore.insert_purchase(
        id_user=message.from_user.id,
        id_pack=get_id_pack(),
        TB=context_data.get("TB", "Buy"),
        kreo_type=context_data["type"],
        GEO=context_data.get("geo"),
        language=context_data["language"],
        size=context_data["size"],
        offer=context_data["offer"],
        price=context_data["size"] / 5,
    )  ### clearly
    await AsyncCore.update_kreo(
        message.from_user.id, context_data["size"]
    )  ### Udpated kreo in POSTGRES

    # Update the rating
    await redis.set(name="string", value=await calculate_rating(bot))

    # And we also need to update the personal rating
    await redis.set(
        name=str(message.from_user.id) + "position",
        value=await calculate_personal_position(message.from_user.id, bot),
        ex=600,
    )

    await message.answer(
        f"Get your fucking {context_data['size']} kreo!",
        reply_markup=main_menu_keyboard_admin
        if message.from_user.id in admins
        else main_menu_keyboard,
    )

    await state.set_state(FSM.main_menu)


# Все работает четко, осталось сделать так, чтобы когда происходит покупка пака, чтобы у всех кэш (position) удалялся,
# так как он уже недействителен, так как позиция человека может поменяться из-за других

# Фидбек Косте будет отправляться. Нужно это сейчас реализовать.
