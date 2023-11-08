from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сгенерировать🤖"), KeyboardButton(text="Рейтинг 💎")],
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
        [KeyboardButton(text="Похудение🍏"), KeyboardButton(text="Паразиты🦠")],
        [KeyboardButton(text="Гипертония🫀"), KeyboardButton(text="Диабет👅")],
        [KeyboardButton(text="Простатит🥚"), KeyboardButton(text="Потенция🍌")],
        [KeyboardButton(text="Суставы🦵🏻"), KeyboardButton(text="Омоложение👶🏻")],
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
            KeyboardButton(text="ES🇪🇸"),
            KeyboardButton(text="IT🇮🇹"),
        ],
        [
            KeyboardButton(text="BG🇧🇬"),
            KeyboardButton(text="RO🇷🇴"),
            KeyboardButton(text="CZ🇨🇿"),
            KeyboardButton(text="FR🇫🇷"),
        ],
        [KeyboardButton(text="◀️Назад"), KeyboardButton(text="В начало🏠")],
    ],
    resize_keyboard=True,
)

sizes_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="5 (XS)"),
            KeyboardButton(text="10 (S)"),  # 1$
            KeyboardButton(text="20 (M)"),
        ],
        [
            KeyboardButton(text="30 (L)"),
            KeyboardButton(text="50 (XL)"),
            KeyboardButton(text="100 (MAX)"),  # 10$
        ],
        [KeyboardButton(text="◀️Назад"), KeyboardButton(text="В начало🏠")],
    ],
    resize_keyboard=True,
)