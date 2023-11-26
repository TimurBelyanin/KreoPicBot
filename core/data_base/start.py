from queries_core import AsyncCore
import asyncio
from time import time
from aiogram.fsm.context import FSMContext


a = time()
asyncio.run(AsyncCore.create_tables())

print(time() - a)


# SELECT created_at AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Moscow' AS local_time
# FROM users;
