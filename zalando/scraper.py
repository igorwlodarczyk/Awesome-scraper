import asyncio
import constants as const
import logging
from utils import clear_debug_logs
from datetime import datetime
from playwright.async_api import async_playwright
import uuid


async def scrap_zalando(url):
    unique_id = str(uuid.uuid4())[:10]
    logger = logging.getLogger(f"Zalando_scraper__{unique_id}")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    log_file_name = f"log_debug_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}__{unique_id}"
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.debug(f"Start url: {url}")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto(url)
            logger.debug("Trying to accept cookies...")
            try:
                await page.locator(const.xpath_cookies_button).click()
            finally:
                try:
                    logger.debug("Successfully accepted cookies!")
                    logger.debug("Trying to get discounted price...")
                    await page.wait_for_selector(const.xpath_discounted_price, timeout=const.timeout)
                    price = await page.locator(const.xpath_discounted_price).text_content()
                    logger.debug("Successfully gotten discounted price!")
                except:
                    logger.debug("Trying to get regular price...")
                    await page.wait_for_selector(const.xpath_regular_price, timeout=const.timeout)
                    price = await page.locator(const.xpath_regular_price).text_content()
                    logger.debug("Successfully gotten regular price!")
                finally:
                    logger.debug(f"Scraped price: {price}")
                    try:
                        logger.debug("Trying to get available sizes...")
                        await page.wait_for_selector(const.xpath_sizes_button, timeout=const.timeout)
                        await page.locator(const.xpath_sizes_button).click()
                        sizes = await page.locator(const.xpath_sizes).all_inner_texts()
                        logger.debug("Successfully gotten available sizes!")
                        print(sizes)
                    except:
                        logger.debug("Checking if this item is one size")
                        await page.wait_for_selector(const.css_one_size, timeout=const.timeout)
                        sizes = await page.locator(const.css_one_size).text_content()
                        logger.debug("It is one size item")
                    finally:
                        return price, sizes
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)


async def scrape_urls(urls):
    tasks = [asyncio.create_task(scrap_zalando(url)) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

lis = ["https://www.zalando.pl/ombre-kardigan-green-om422e020-m11.html",
       "https://www.zalando.pl/ombre-spodnie-treningowe-navy-blue-om422e00j-k11.html",
       "https://www.zalando.pl/mcm-okulary-przeciwsloneczsdne-black-mc152k00c-q11.html"]
results = asyncio.run(scrape_urls(lis))
print(results)
clear_debug_logs()