from main import bot, dp 
from aiogram.types import Message
from base.bd_funcs import get_order_summ, make_description_order
from aiogram import types
from cfg import payment_token
from aiogram.types.message import ContentType
from aiogram.types import LabeledPrice
import os


@dp.callback_query_handler(text='pay_order')
async def add_to_basket_dish(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    PRICE = LabeledPrice(label='dadada', amount=get_order_summ(user_id=callback_query.from_user.id)*100)

    await bot.send_invoice(chat_id=user_id, title='Замовлення', description=make_description_order(user_id), payload='test-payload', provider_token=payment_token, currency='uah', prices=[PRICE])

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    user_id=message.from_id
    await bot.send_message(message.from_id, text='Ваше замовлення відправлено кухару.')
    try:
        os.remove(f'basket_base/{user_id}.json')
    except Exception as ex:
        print(ex)
