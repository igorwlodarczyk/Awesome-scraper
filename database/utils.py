import aiosqlite


async def get_urls_data(db_name, store_name):
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute(
            "SELECT url, item_id FROM urls WHERE store_name = ?", (store_name,)
        )
        results = await cursor.fetchall()
        urls = [{"url": row[0], "item_id": row[1]} for row in results]
        return urls
