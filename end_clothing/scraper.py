import asyncio
import uuid
from datetime import datetime
import logging
from common.utils import parse_price, clear_debug_logs
from end_clothing.utils import parse_sizes
from playwright.async_api import async_playwright
import end_clothing.constants as const
from common.constants import db_name
from database.utils import get_urls_data, save_data


async def scrap_end_clothing(url_db):
    item_id = url_db["item_id"]
    url = url_db["url"]
    currency = const.currency
    unique_id = str(uuid.uuid4())[:10]
    logger = logging.getLogger(f"End_clothing_scraper__{unique_id}")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    log_file_name = (
        f"log_debug_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}__{unique_id}"
    )
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.debug(f"Start url: {url}")
    try:
        async with async_playwright() as p:
            user_agent = const.user_agent
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            await context.set_extra_http_headers({"User-Agent": user_agent})
            page = await context.new_page()
            await page.goto(url)
            logger.debug("Trying to get the price...")
            await page.wait_for_selector(const.xpath_price, timeout=const.timeout)
            price = await page.locator(const.xpath_price).text_content()
            logger.debug("Successfully gotten price!")
            logger.debug("Trying to get available sizes...")
            await page.wait_for_selector(const.xpath_sizes, timeout=const.timeout)
            sizes = await page.locator(const.xpath_sizes).all_inner_texts()
            logger.debug("Successfully gotten available sizes!")
            parsed_price = parse_price(price)
            parsed_sizes = parse_sizes(sizes)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if parsed_sizes is not None and parsed_price is not None:
                for size in parsed_sizes:
                    await save_data(
                        db_name,
                        parsed_price,
                        size,
                        currency,
                        date,
                        url,
                        item_id,
                    )
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)


async def scrap_urls():
    urls = await get_urls_data(db_name, const.store_name)
    tasks = [asyncio.create_task(scrap_end_clothing(url)) for url in urls]
    await asyncio.gather(*tasks)


def scraper_end_clothing():
    asyncio.run(scrap_urls())
    clear_debug_logs()
