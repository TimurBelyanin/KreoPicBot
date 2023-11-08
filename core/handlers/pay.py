from aiogram import Bot, Router
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command
from core.filters.content_type_filter import ContentTypeFilter
import time
from secrets import token_hex


router = Router()


@router.message(Command(commands=["buy"]))
async def order(message: Message, bot: Bot):
    start_parameter = token_hex(5)
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Our digital product",
        description="test payment",
        payload="some shit",
        provider_token="381764678:TEST:69893",
        currency="USD",
        prices=[
            LabeledPrice(label="хуята", amount=9900),
            LabeledPrice(label="еще одна хуята", amount=1000),
        ],
        start_parameter=start_parameter,
        need_name=True,
        need_phone_number=True,
        need_shipping_address=False,
        protect_content=True,
        request_timeout=15,
        photo_url="https://kaliboys.com/wp-content/uploads/2021/07/AIOGram.jpg",
        photo_width=416,
        photo_height=234,
        photo_size=416,
    )


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(ContentTypeFilter())
async def successful_payment(message: Message, bot: Bot):
    await message.answer("Лови свой пак")
    await bot.send_message(
        message.chat.id,
        f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!",
    )
