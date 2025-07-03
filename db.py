import sqlite3 as sql

# Connects with the database


def init_db():
    db = sql.connect("database.db", timeout=10, check_same_thread=False)
    cr = db.cursor()
    cr.execute(
        "CREATE TABLE IF NOT EXISTS master (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, hash TEXT NOT NULL)")
    cr.execute(
        "CREATE TABLE IF NOT EXISTS vault"
        " (id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " username TEXT NOT NULL,"
        " site_username TEXT NOT NULL,"
        " site TEXT NOT NULL, salt TEXT NOT NULL,"
        " encryption TEXT NOT NULL,"
        " nonce TEXT NOT NULL,"
        " date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    db.commit()
    db.close()


def db_conn():
    return sql.connect("database.db", timeout=10, check_same_thread=False)


def db_vault():
    return sql.connect("database.db", timeout=10, check_same_thread=False)
