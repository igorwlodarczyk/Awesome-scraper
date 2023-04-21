import aiosqlite


async def get_urls(db_name, store_name):
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute(
            "SELECT url FROM urls WHERE store_name = ?", (store_name,)
        )
        results = await cursor.fetchall()
        urls = [row[0] for row in results]
        return urls
