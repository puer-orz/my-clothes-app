import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), 'data', 'wardrobe.db')

if not os.path.exists(DB_PATH):
    print("Database file not found.")
else:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT api_model, api_base_url FROM users LIMIT 1')
    row = c.fetchone()
    if row:
        print(f"Current Model: {row['api_model']}")
        print(f"Base URL: {row['api_base_url']}")
    else:
        print("No user settings found.")
    conn.close()
