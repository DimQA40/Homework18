import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConvector:
    @staticmethod
    def get_price(base: str, quota: str, amount: str):

        if base == quota:
            raise APIException(f'Невозможно перевести одинаковые валюты "{base}".')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Неправильно указана валюта "{base}".')

        try:
            quota_ticker = keys[quota]
        except KeyError:
            raise APIException(f'Неправильно указана валюта "{quota}".')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неправильно указано количество конвертируемой валюты "{amount}".')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quota_ticker}')
        total_sum = json.loads(r.content)[keys[quota]]
        sum_all = round(total_sum * amount, 4)

        return sum_all
