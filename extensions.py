import json
import requests

from config import My_keys


class Exceptions(Exception):
    pass


class Converters(BaseException):
    @staticmethod
    def _convert(quote: str, base: str, amount: str):
        if quote == base:
            raise Exceptions(f'Одинаковые валюты {base} невозможно перевести!')

        try:
            quote_ticker = My_keys[quote]
        except KeyError:
            raise Exceptions(f'Валюта {quote} не может быть обработана!')

        try:
            base_ticker = My_keys[base]
        except KeyError:
            raise Exceptions(f'Валюта {base} не может быть обработана!')

        try:
            amount = float(amount)
        except ValueError:
            raise Exceptions(f'Число {amount} не может быть обработано!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[My_keys[base]] * amount

        return total_base
