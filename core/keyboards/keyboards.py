from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_keyboard_admin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сгенерировать🤖"), KeyboardButton(text="Рейтинг 💎")],
        [KeyboardButton(text="Обратная связь✨")],
        [KeyboardButton(text="Статистика✨")],
    ],
    resize_keyboard=True,
)

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сгенерировать🤖"), KeyboardButton(text="Рейтинг 💎")],
        [KeyboardButton(text="Обратная связь✨")],
    ],
    resize_keyboard=True,
)

types_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Классический👨🏻‍⚕️"), KeyboardButton(text="Товарный 💊")],
        [KeyboardButton(text="◀️Назад")],
    ],
    resize_keyboard=True,
)

offers_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Похудение🍏"),
            KeyboardButton(text="Суставы🦵🏻"),
        ],
        [KeyboardButton(text="Диабет👅"), KeyboardButton(text="Гипертония🫀")],
        [KeyboardButton(text="Потенция🍌"), KeyboardButton(text="Простатит🥚")],
        [KeyboardButton(text="Паразиты🦠"), KeyboardButton(text="Омоложение👶🏻")],
        [KeyboardButton(text="◀️Назад"), KeyboardButton(text="В начало🏠")],
    ],
    resize_keyboard=True,
)

geo_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Европа👨🏼"),
            KeyboardButton(text="Латам👨🏽‍🦱"),
        ],
        [KeyboardButton(text="Африка🧑🏿‍🦱"), KeyboardButton(text="Азия👨🏽‍🦲")],
        [KeyboardButton(text="◀️Назад"), KeyboardButton(text="В начало🏠")],
    ],
    resize_keyboard=True,
)

languages_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="RU🇷🇺"),
            KeyboardButton(text="EN🇬🇧"),
            # KeyboardButton(text="ES🇪🇸"),
            KeyboardButton(text="IT🇮🇹"),
        ],
        [
            KeyboardButton(text="UA🇺🇦"),
            KeyboardButton(text="ES🇪🇸"),
            # KeyboardButton(text="BG🇧🇬"),
            # KeyboardButton(text="RO🇷🇴"),
            # KeyboardButton(text="CZ🇨🇿"),
            KeyboardButton(text="FR🇫🇷"),
        ],
        [KeyboardButton(text="◀️Назад"), KeyboardButton(text="В начало🏠")],
    ],
    resize_keyboard=True,
)

sizes_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="5 | S | 1$"),  # 1$
            KeyboardButton(text="10 | M | 2$"),
        ],
        [
            KeyboardButton(text="20 | L | 4$"),
            KeyboardButton(text="30 | XL | 6$"),
            # KeyboardButton(text="50 | XL | 10$"),
            # KeyboardButton(text="100 | XXL | 20$"),  # 20$
        ],
        [KeyboardButton(text="◀️Назад"), KeyboardButton(text="В начало🏠")],
    ],
    resize_keyboard=True,
)

statistics_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отчёт✨"), KeyboardButton(text="Файл✨")],
        [KeyboardButton(text="◀️Назад")],
    ],
    resize_keyboard=True,
)

reports_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сегодня"), KeyboardButton(text="Вчера")],
        [KeyboardButton(text="Неделя"), KeyboardButton(text="Месяц")],
        [KeyboardButton(text="◀️Назад")],
    ],
    resize_keyboard=True,
)

tb_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Test"), KeyboardButton(text="Buy")]],
    resize_keyboard=True,
)

feedback_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="◀️Назад")]], resize_keyboard=True
)
