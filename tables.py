import sqlite3
connectionDB = sqlite3.connect("tutorial.db")
cur = connectionDB.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS USERS(
    discord_id TEXT PRIMARY KEY,
    name TEXT
)''')