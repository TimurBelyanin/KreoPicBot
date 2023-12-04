from aiogram import Bot, Dispatcher
from core.data_base.queries_core import AsyncCore
from aiogram.types import Message


positions = {
    0: "0️⃣",
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟",
}


async def username_func(user_id: int, bot: Bot):
    """Return username from user_id"""
    string = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
    return string.user.username


async def calculate_rating(bot: Bot):
    """Calculates the freshest rating"""

    users = await AsyncCore.select_workers()
    # Получаем список кортежей с ником и кол-вом kreo
    users = [(await username_func(i[0], bot), i[2]) for i in users]
    # Получить строку рейтинга в нужном формате
    string = "\n".join(
        [f"{positions[i + 1]} @{k[0]} | {k[1]} kreo" for i, k in enumerate(users)]
    )
    return f"Рейтинг KreoPicBot💎\n\n{string}"


async def calculate_personal_position(user_id: int, bot: Bot):
    """Function which calculates dynamic personal position"""

    user = await AsyncCore.get_personal_position(user_id)
    kreo, position = user[0][1:]
    # Here we build personal dynamic string
    username = await username_func(user_id, bot)
    string = f"{''.join([positions[int(i)] for i in str(position)])} @{username} | {kreo} kreo"
    return string


async def calculate_personal_position_and_push(user_id: int, bot: Bot, dp: Dispatcher):
    """Function which put personal string into cache if it's not there and return it from there"""

    if not await dp.get("redis").get(str(user_id) + "position"):
        await dp.get("redis").set(
            name=str(user_id) + "position",
            value=await calculate_personal_position(user_id, bot),
            ex=600,
        )
    return await dp.get("redis").get(str(user_id) + "position")


async def rating(message: Message, bot: Bot, dp: Dispatcher):
    """Function which returns rating"""
    # if value not in the cache, we add the value
    if not await dp.get("redis").get("string"):
        await dp.get("redis").set(name="string", value=await calculate_rating(bot))
    string = await dp.get("redis").get("string")  # from cache
    await message.answer(
        f"<b>{string}\n...\n{await calculate_personal_position_and_push(message.from_user.id, bot, dp)}</b>"
    )


# Динамическое получение индивидуального положения в рейтинге. Сам список рейтинга всегда берется из кэша. Первое получение
# С личным положением все так же, только оно меняется не после покупки а устанавливается в Redis на 10 минут.
