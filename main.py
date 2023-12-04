import asyncio
from typing import List

from aiogram import Bot, Dispatcher, F
from config import settings
from core.handlers.back_handler import router as back_router
from core.handlers.start import router as start_router, finish
from core.handlers.admin_handler import router as admin_router
from core.handlers.feedback_handler import router as feedback_router
import logging
from logging.handlers import RotatingFileHandler
from redis import asyncio as aioredis
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from core.data_base.queries_core import AsyncCore
from core.utils.FSM import FSM
from core.utils.rating import rating
from core.filters.dp_filter import DpFilter  ###########
from core.handlers.start import finish
import datetime


# def on_startup(bot: Bot, user_id):
#     user = bot.get_chat_member(chat_id=user_id, user_id=user_id)
#     print(user)


async def main():
    bot = Bot(token=settings.TOKEN_KOSTYA.get_secret_value(), parse_mode="HTML")
    # await create_database()

    redis_connection = aioredis.client.Redis(decode_responses=True)

    # await redis_connection.set(name="kek", value=23, ex=10)
    # redis_connection = redis.StrictRedis(
    #     host="109.172.82.65", port="6379", username="default", password="Lx)J&WH6$.xyD8"
    # )

    storage = RedisStorage(redis=redis_connection)
    dp = Dispatcher(storage=storage)
    dp["redis"] = redis_connection

    # dp.shutdown.register(on_shutdown)
    dp.message.register(rating, DpFilter(dp), F.text == "Рейтинг 💎", FSM.main_menu)
    dp.message.register(
        finish,
        DpFilter(dp),
        F.text.in_(["5 (XS)", "10 (S)", "20 (M)", "30 (L)", "50 (XL)", "100 (MAX)"]),
        FSM.sizes,
    )

    dp.include_routers(admin_router, start_router, back_router, feedback_router)
    # dp.message.
    try:
        await bot.delete_webhook(drop_pending_updates=False)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await dp["redis"].aclose()


if __name__ == "__main__":
    log_formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
    # log_handler = RotatingFileHandler(
    #     "py_log.log", maxBytes=5 * 1024 * 1024, backupCount=1
    # )
    # log_handler = RotatingFileHandler(
    #     "py_log.log", maxBytes=5 * 1024 * 1024, backupCount=1
    # )
    # log_handler.setFormatter(log_formatter)
    # logging.basicConfig(level=logging.INFO, handlers=[log_handler])
    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())

# подключение БД sqlite
# создание стикера во время создания зип-архива
# логгирование (буду использовать Loguru) - нет, logging!
# антифлуд (миддлвари) - походу придется для этого прикручивать redis, а уж потом ставить антифлуд
# цель на данный момент - пройтись по логированию и системе оплаты
# также реализовать цепочку вопрсоов, без бизнес-логики, пока Костя не сделал папочную структуру
# на данный момент моя цель - реализовать вебхук, после него оплата и все - моя часть фактически готова


# Вебхук готов. Оплата
# Судя по всему, оплата будет через робокассу
# Кэширование через Redis пока делать не буду, огромного потока народу в один момент времени быть не должно
# Сделал кэширование для рейтинга. Нужно обработать команду покупки
# Сейчас накидываю мидлварь на команду start чтобы пропускала только тех, кто в белом списке
