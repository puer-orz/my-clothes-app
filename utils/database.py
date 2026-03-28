import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.getcwd(), 'data', 'wardrobe.db')

def init_db():
    """初始化数据库，创建必要的表"""
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 用户表
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            height REAL,
            weight REAL,
            gender TEXT,
            style_preference TEXT,
            api_key TEXT,
            api_base_url TEXT,
            api_model TEXT,
            vision_api_key TEXT,
            vision_base_url TEXT,
            vision_model TEXT
        )
    ''')
    
    # 检查 api_model 列是否存在 (用于旧数据库迁移)
    c.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in c.fetchall()]
    if 'api_model' not in columns:
        try:
            c.execute("ALTER TABLE users ADD COLUMN api_model TEXT")
            c.execute("UPDATE users SET api_model = 'deepseek-chat'")
        except Exception as e:
            print(f"Migration error: {e}")
            
    # 检查 vision_api_key 列是否存在 (用于旧数据库迁移)
    if 'vision_api_key' not in columns:
        try:
            c.execute("ALTER TABLE users ADD COLUMN vision_api_key TEXT")
            c.execute("ALTER TABLE users ADD COLUMN vision_base_url TEXT")
            c.execute("ALTER TABLE users ADD COLUMN vision_model TEXT")
        except Exception as e:
            print(f"Migration error (vision): {e}")
    
    # 衣服表
    c.execute('''
        CREATE TABLE IF NOT EXISTS clothes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            image_path TEXT,
            description TEXT,
            size TEXT,
            season TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 检查 color 列是否存在 (用于旧数据库迁移)
    c.execute("PRAGMA table_info(clothes)")
    clothes_columns = [info[1] for info in c.fetchall()]
    if 'color' not in clothes_columns:
        try:
            c.execute("ALTER TABLE clothes ADD COLUMN color TEXT")
        except Exception as e:
            print(f"Migration error (clothes color): {e}")

    # 历史记录表
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            recommendation TEXT,
            weather_info TEXT,
            result_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 检查 result_json 列是否存在 (用于旧数据库迁移)
    c.execute("PRAGMA table_info(history)")
    history_columns = [info[1] for info in c.fetchall()]
    if 'result_json' not in history_columns:
        try:
            c.execute("ALTER TABLE history ADD COLUMN result_json TEXT")
        except Exception as e:
            print(f"Migration error (history): {e}")
    
    # 确保有一个默认用户
    c.execute('SELECT count(*) FROM users')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO users (height, weight, style_preference, api_base_url, api_model) VALUES (?, ?, ?, ?, ?)', 
                 (170, 60, '简约休闲', 'https://api.deepseek.com', 'deepseek-chat'))
    
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)

def save_clothes(category, image_path, description, size, season, color=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO clothes (category, image_path, description, size, season, color)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (category, image_path, description, size, season, color))
    conn.commit()
    conn.close()

def get_all_clothes():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM clothes ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def delete_clothes(clothes_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM clothes WHERE id = ?', (clothes_id,))
    conn.commit()
    conn.close()

def update_clothes(clothes_id, category, description, size, season, color):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE clothes 
        SET category = ?, description = ?, size = ?, season = ?, color = ?
        WHERE id = ?
    ''', (category, description, size, season, color, clothes_id))
    conn.commit()
    conn.close()

def get_user_settings():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM users LIMIT 1')
    row = c.fetchone()
    conn.close()
    return row

def update_user_settings(height, weight, gender, style_preference, api_key, api_base_url, api_model, vision_api_key=None, vision_base_url=None, vision_model=None):
    conn = get_connection()
    c = conn.cursor()
    # 假设只有一个用户
    c.execute('''
        UPDATE users 
        SET height = ?, weight = ?, gender = ?, style_preference = ?, api_key = ?, api_base_url = ?, api_model = ?,
            vision_api_key = ?, vision_base_url = ?, vision_model = ?
        WHERE id = (SELECT id FROM users LIMIT 1)
    ''', (height, weight, gender, style_preference, api_key, api_base_url, api_model, vision_api_key, vision_base_url, vision_model))
    conn.commit()
    conn.close()

import json

def save_history(recommendation, weather_info, result_json=None):
    conn = get_connection()
    c = conn.cursor()
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # 如果传入的是 dict，转换为 json string
    if isinstance(result_json, dict):
        result_json = json.dumps(result_json, ensure_ascii=False)
        
    c.execute('''
        INSERT INTO history (date, recommendation, weather_info, result_json)
        VALUES (?, ?, ?, ?)
    ''', (date_str, recommendation, weather_info, result_json))
    conn.commit()
    conn.close()

def get_today_history():
    """获取今日的穿搭推荐"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    date_str = datetime.now().strftime('%Y-%m-%d')
    c.execute('SELECT * FROM history WHERE date = ? ORDER BY created_at DESC LIMIT 1', (date_str,))
    row = c.fetchone()
    conn.close()
    return row

def delete_today_history():
    """删除今日的穿搭推荐历史"""
    conn = get_connection()
    c = conn.cursor()
    date_str = datetime.now().strftime('%Y-%m-%d')
    c.execute('DELETE FROM history WHERE date = ?', (date_str,))
    conn.commit()
    conn.close()

def get_history():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM history ORDER BY created_at DESC LIMIT 20')
    rows = c.fetchall()
    conn.close()
    return rows
