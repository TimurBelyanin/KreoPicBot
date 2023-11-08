import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from config import settings
from core.handlers.back_handler import router as back_router
from core.handlers.start import router as start_router
from core.handlers.pay import router as pay_router
from core.middlewares.throttling_middleware import ThrottlingMiddleware
from aiohttp import web  #########

# def start():
#     print(333)


async def main():
    bot = Bot(token=settings.TOKEN_KOSTYA.get_secret_value(), parse_mode="HTML")
    # await create_database()

    storage = RedisStorage.from_url(url="redis://localhost:6379/0")
    dp = Dispatcher(storage=storage)
    # dp.message.middleware(ThrottlingMiddleware(storage=storage, bot=bot))
    # await dp.emit_startup(start())
    # dp.message.outer_middleware(SomeMiddleware())
    dp.include_routers(start_router, back_router)
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == "__main__":
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
