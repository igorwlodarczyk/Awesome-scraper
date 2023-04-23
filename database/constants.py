items_table = """CREATE TABLE items
                    (item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    brand TEXT(40) NOT NULL,
                    model TEXT(160) NOT NULL) """
urls_table = """CREATE TABLE urls
                  (url TEXT(500) NOT NULL,
                   store_name TEXT(150) NOT NULL,
                   item_id INTEGER NOT NULL,
                   FOREIGN KEY (item_id) REFERENCES items(item_id))"""
data_table = """CREATE TABLE scraped_data
                  (data_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   price FLOAT NOT NULL,
                   currency TEXT(30) NOT NULL,
                   size TEXT(30) NOT NULL,
                   date DATETIME NOT NULL,
                   url INTEGER NOT NULL,
                   item_id INTEGER NOT NULL,
                   FOREIGN KEY (url) REFERENCES urls(url),
                   FOREIGN KEY (item_id) REFERENCES items(item_id))"""
