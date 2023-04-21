import sqlite3
import aiosqlite


def add_url(db_name, url, store_name, item_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO urls (url, store_name, item_id)
                      VALUES (?, ?, ?)""",
        (url, store_name, item_id),
    )
    conn.commit()
    conn.close()


async def add_data(db_name, price, currency, date, url_id, item_id):
    async with aiosqlite.connect(db_name) as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            """INSERT INTO scraped_data (price, currency, date, url_id, item_id)
                               VALUES (?, ?, ?, ?, ?)""",
            (price, currency, date, url_id, item_id),
        )
        await conn.commit()
