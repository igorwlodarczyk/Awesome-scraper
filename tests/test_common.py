import pytest
from common.utils import parse_price


@pytest.mark.parametrize(
    "price, expected_parsed_price",
    [("123,1 pln", 123.1), ("69,99 EUR", 69.99), ("75.99", 75.99)],
)
def test_parse_price(price, expected_parsed_price):
    assert parse_price(price) == expected_parsed_price
