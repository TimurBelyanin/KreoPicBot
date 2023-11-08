from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

food_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Milk"), KeyboardButton(text="Bread")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

drink_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Coffee"), KeyboardButton(text="Tea")],
        [KeyboardButton(text="Назад"), KeyboardButton(text="Домой")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

profession_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Programmer"), KeyboardButton(text="Designer")],
        [KeyboardButton(text="Firefighter"), KeyboardButton(text="Seller")],
        [KeyboardButton(text="Назад"), KeyboardButton(text="Домой")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

hair_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Black"), KeyboardButton(text="Brown")],
        [
            KeyboardButton(text="Blonde"),
            KeyboardButton(text="White"),
            KeyboardButton(text="Red"),
        ],
        [KeyboardButton(text="Назад"), KeyboardButton(text="Домой")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
