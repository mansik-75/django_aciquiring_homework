from aiogram.types import LabeledPrice

prices = {
    'success': True,
    'tariffs': [
        {
            'id': 1,
            'price': 99000,
            'description': 'Тариф базовый'
        }
    ]
}
PRICES = {}
PRICE_IDS = tuple(str(price['id']) for price in prices['tariffs'])

for price in prices['tariffs']:
    PRICES[str(price['id'])] = LabeledPrice(label=price['description'], amount=price['price'])


