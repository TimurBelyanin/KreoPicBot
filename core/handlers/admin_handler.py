from aiogram.types import Message, FSInputFile
from core.utils.FSM import FSM
from aiogram import Router, F, Bot
from core.keyboards.keyboards import (
    main_menu_keyboard,
    types_keyboard,
    offers_keyboard,
    geo_keyboard,
    languages_keyboard,
    main_menu_keyboard_admin,
    reports_keyboard,
    statistics_keyboard,
    tb_keyboard,
)
from aiogram.fsm.context import FSMContext
from core.filters.filter_for_back import IsNoneFilter
from core.utils import admins
from core.data_base.queries_core import AsyncCore
from datetime import datetime, timedelta
import tempfile
import pandas as pd
import os


router = Router()


@router.message(F.from_user.id.in_({*admins}), F.text == "Сгенерировать🤖")
async def test_or_buy(message: Message, state: FSMContext):
    await state.set_state(FSM.TB)
    await message.answer("Выбери характер операции", reply_markup=tb_keyboard)


@router.message(F.from_user.id.in_({*admins}), F.text.in_(["Test", "Buy"]), FSM.TB)
async def just_forward(message: Message, state: FSMContext):
    await state.update_data(TB=message.text)
    await state.set_state(FSM.types)
    await message.answer(
        "Выбери вид креатива👨🏻‍💻",
        reply_markup=types_keyboard,
    )


@router.message(F.from_user.id.in_({*admins}), F.text == "Статистика✨", IsNoneFilter())
async def statistics(message: Message, state: FSMContext):
    """Function returns statistics about bot to admin"""
    await state.set_state(FSM.statistics)
    await message.answer("Выбери опцию", reply_markup=statistics_keyboard)


@router.message(F.text == "Файл✨", FSM.statistics)
async def get_file(message: Message, state: FSMContext):
    """Function returns file which contains all the recordings about purchases"""
    await state.clear()
    temp_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    purchases = await AsyncCore.get_purchases()
    df = pd.DataFrame(purchases)[::-1]
    df.to_csv(temp_file.name)
    await message.bot.send_document(
        chat_id=message.chat.id,
        document=FSInputFile(path=temp_file.name, filename="purchases.csv"),
        caption="✨✨✨✨✨✨Получи таблицу с покупками✨✨✨✨✨✨✨✨",
        reply_markup=main_menu_keyboard_admin,
    )
    temp_file.close()
    os.remove(temp_file.name)


@router.message(F.text == "Отчёт✨", FSM.statistics)
async def report(message: Message, state: FSMContext):
    """Function returns something:)"""
    await state.set_state(FSM.report)
    await message.answer(
        "✨✨✨✨✨✨Выбери промежуток времени, за который хочешь узнать отчёт✨✨✨✨✨✨✨✨",
        reply_markup=reports_keyboard,
    )


@router.message(F.text.in_(["Сегодня", "Вчера", "Неделя", "Месяц"]), FSM.report)
async def users_options(message: Message, state: FSMContext):
    """Function which returns results of different sql-queries depending on the option"""
    date1, date2 = None, None
    match message.text:
        case "Сегодня":
            date1, date2 = (
                datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0),
                datetime.utcnow(),
            )
        case "Вчера":
            date1, date2 = datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0
            ) - timedelta(days=1), datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        case "Неделя":
            date1, date2 = datetime.utcnow() - timedelta(days=7), datetime.utcnow()
        case "Месяц":
            date1, date2 = datetime.utcnow() - timedelta(days=30), datetime.utcnow()

    packs, kreo, money = await AsyncCore.get_report(date1=date1, date2=date2)
    await message.answer(
        f"✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨За данный период сгенерировано:\nПаков: {packs}\nKreo: {kreo or 0}\nДоход: {int(money or 0)}$✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨",
        reply_markup=main_menu_keyboard_admin,
    )
    await state.clear()
