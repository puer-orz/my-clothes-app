from utils.database import get_all_clothes, DB_PATH
import os

print(f"DB Path: {DB_PATH}")
if os.path.exists(DB_PATH):
    print("DB file exists.")
else:
    print("DB file does NOT exist.")

clothes = get_all_clothes()
print(f"Total clothes in DB: {len(clothes)}")
for item in clothes:
    print(dict(item))
