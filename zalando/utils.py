import re
import constants as const


async def parse_price(price):
    """
    Converts a string representing a price to a floating-point number.
    :param price: A string representing the price.
    :return: A float representing the price.
    """
    price = re.sub(r"[^0-9.,]", "", price)
    price = price.replace(",", ".")
    return float(price)


async def get_currency(url):
    for zalando_url in const.currency.keys():
        if zalando_url in url:
            return const.currency[zalando_url]
    return None
