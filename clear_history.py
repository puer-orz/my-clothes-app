import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.getcwd(), 'data', 'wardrobe.db')

def clear_today_history():
    if not os.path.exists(DB_PATH):
        print("DB not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Clearing history for date: {date_str}")
    c.execute('DELETE FROM history WHERE date = ?', (date_str,))
    rows_deleted = c.rowcount
    conn.commit()
    conn.close()
    print(f"Deleted {rows_deleted} rows.")

if __name__ == "__main__":
    clear_today_history()
