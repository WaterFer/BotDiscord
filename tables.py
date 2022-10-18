import sqlite3
connectionDB = sqlite3.connect("siu.db")
cur = connectionDB.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users(
    discord_id TEXT PRIMARY KEY,
    name TEXT
)''')