import sqlite3
import os
from utils.database import get_user_settings, update_user_settings, DB_PATH

# 打印当前 DB 路径
print(f"DB Path: {DB_PATH}")

# 获取当前设置
print("Before update:")
user = get_user_settings()
if user:
    print(dict(user))
else:
    print("No user found")

# 更新设置
print("Updating settings...")
try:
    update_user_settings(180, 75, '男', '街头潮流', 'test-key', 'http://test.url', 'test-model')
    print("Update called.")
except Exception as e:
    print(f"Error updating: {e}")

# 再次获取
print("After update:")
user = get_user_settings()
if user:
    print(dict(user))
else:
    print("No user found")
