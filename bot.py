import os

from aiogram import Bot, Dispatcher, types
from helper import PRICES

bot = Bot(token=os.environ.get('API_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'report'])
async def subscribe_payment(message: types.Message):
    """Метод, который отправляет счет пользователю"""
    if os.environ.get('PAYMENT_TOKEN').split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, 'Это тестовый вариант оплаты, так что нужно использовать тестовую карту с реквизитами 1111 1111 1111 1026')
    await bot.send_invoice(
        message.chat.id,
        title='Подписка на бота',
        description='Вы оплачиваете тестовую подписку',
        provider_token=os.environ.get('PAYMENT_TOKEN'),
        currency='rub',
        is_flexible=False,
        prices=[PRICES['1']],
        start_parameter='service-subscription',
        payload=f'subscription-for-user_{message.chat.id}',
        need_email=True,
        need_phone_number=True,
        send_email_to_provider=True,
        send_phone_number_to_provider=True,
        provider_data={
            'receipt': {
                'items': [
                    {
                        'description': 'оплата подписки',
                        'quantity': '1.00',
                        'amount': {
                            'value': "990.00",
                            'currency': 'RUB'
                        },
                        'vat_code': 1
                    }
                ]
            }
        }
    )

@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    """Метод, который занимается проверкой правильности заполнения счета пользователем"""
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    """Метод, который вызывается после успешной оплаты и регистрирует пользователя на сервере"""
    payload = message.successful_payment.invoice_payload
    print(payload)
    await message.answer("Молодец, ты оплатил подписку")
