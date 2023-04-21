items_table = """CREATE TABLE items
                    (item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT(40),
                    model TEXT(160))"""
urls_table = """CREATE TABLE urls
                  (url_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   url TEXT(500),
                   store_name TEXT(150),
                   item_id INTEGER,
                   FOREIGN KEY (item_id) REFERENCES items(item_id))"""
data_table = """CREATE TABLE scraped_data
                  (data_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   price FLOAT,
                   currency TEXT(30),
                   date DATETIME,
                   url_id INTEGER,
                   item_id INTEGER,
                   FOREIGN KEY (url_id) REFERENCES urls(url_id),
                   FOREIGN KEY (item_id) REFERENCES items(item_id))"""
