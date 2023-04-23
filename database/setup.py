import sqlite3
import database.constants as const


def setup_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(const.items_table)
    cursor.execute(const.urls_table)
    cursor.execute(const.data_table)
    conn.commit()
    conn.close()


def add_item(db_name, brand, model):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO items (brand, model)
                      VALUES (?, ?)""",
        (brand, model),
    )
    conn.commit()
    conn.close()
