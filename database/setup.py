import sqlite3
import constants as const


def setup_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(const.items_table)
    conn.commit()
    conn.close()
