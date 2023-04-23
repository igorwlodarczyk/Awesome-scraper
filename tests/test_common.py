import pytest
from common.utils import parse_price, clear_debug_logs


@pytest.mark.parametrize(
    "price, expected_parsed_price",
    [("123,1 pln", 123.1), ("69,99 EUR", 69.99), ("75.99", 75.99)],
)
def test_parse_price(price, expected_parsed_price):
    """
    This test checks if function parse_price returns correct float value.
    :param price: string
    :param expected_parsed_price: float
    """
    assert parse_price(price) == expected_parsed_price


def test_clear_debug_logs(tmp_path):
    """
    This test checks if function clear_debug_logs correctly removes all debug log files that do not contain word error.
    :param tmp_path: temporary path provided by pytest framework
    """
    file_path_1 = tmp_path / "log_debug_2137"
    file_path_1.write_text("Error")
    file_path_2 = tmp_path / "log_debug_2138"
    file_path_2.write_text("Successful scraping!")
    clear_debug_logs(tmp_path)
    file_count = 0
    for file in tmp_path.iterdir():
        file_count += 1
    assert file_count == 1
