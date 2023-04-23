import asyncio
import zalando.constants as const
import logging
from zalando.utils import get_currency, parse_sizes, parse_price
from common.utils import clear_debug_logs
from database.utils import get_urls_data, save_data
from datetime import datetime
from playwright.async_api import async_playwright
from common.constants import db_name
import uuid


async def scrap_zalando(url_db):
    item_id = url_db["item_id"]
    url = url_db["url"]
    currency = await get_currency(url)
    unique_id = str(uuid.uuid4())[:10]
    logger = logging.getLogger(f"Zalando_scraper__{unique_id}")
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
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            await context.set_extra_http_headers({"User-Agent": user_agent})
            page = await context.new_page()
            await page.goto(url)
            logger.debug("Trying to accept cookies...")
            try:
                await page.wait_for_selector(
                    const.xpath_cookies_button, timeout=const.timeout
                )
                await page.locator(const.xpath_cookies_button).click()
            finally:
                try:
                    logger.debug("Successfully accepted cookies!")
                    logger.debug("Trying to get discounted price...")
                    await page.wait_for_selector(
                        const.xpath_discounted_price, timeout=const.timeout
                    )
                    price = await page.locator(
                        const.xpath_discounted_price
                    ).text_content()
                    logger.debug("Successfully gotten discounted price!")
                except:
                    logger.debug("Trying to get regular price...")
                    await page.wait_for_selector(
                        const.xpath_regular_price, timeout=const.timeout
                    )
                    price = await page.locator(const.xpath_regular_price).text_content()
                    logger.debug("Successfully gotten regular price!")
                finally:
                    logger.debug(f"Scraped price: {price}")
                    try:
                        logger.debug("Trying to get available sizes...")
                        await page.wait_for_selector(
                            const.xpath_sizes_button, timeout=const.timeout
                        )
                        await page.locator(const.xpath_sizes_button).click()
                        await page.wait_for_selector(
                            const.xpath_sizes, timeout=const.timeout
                        )
                        sizes = await page.locator(const.xpath_sizes).all_inner_texts()
                        logger.debug("Successfully gotten available sizes!")
                    except:
                        logger.debug("Checking if this item is one size")
                        await page.wait_for_selector(
                            const.css_one_size, timeout=const.timeout
                        )
                        sizes = await page.locator(const.css_one_size).text_content()
                        logger.debug("It is one size item")
                    finally:
                        parsed_price = await parse_price(price)
                        parsed_sizes = await parse_sizes(sizes)
                        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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


async def scrape_urls():
    urls = await get_urls_data(db_name, const.store_name)
    tasks = [asyncio.create_task(scrap_zalando(url)) for url in urls]
    await asyncio.gather(*tasks)


def scraper_zalando():
    asyncio.run(scrape_urls())
    clear_debug_logs()
