
import sqlite3
import os
import sys
from utils.database import get_connection
from utils.ai_service import analyze_image_color

# 添加父目录到 sys.path 以便导入 utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def batch_update_colors():
    """
    批量更新数据库中颜色为空的衣服
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # 查找颜色为空、None 或 "未知" 的记录
    c.execute("SELECT * FROM clothes WHERE color IS NULL OR color = '' OR color = '未知'")
    rows = c.fetchall()
    
    if not rows:
        print("没有需要更新的记录。")
        conn.close()
        return

    print(f"找到 {len(rows)} 件需要识别颜色的衣服。")
    
    # 获取 API 配置 (假设只有一个用户)
    c.execute('SELECT * FROM users LIMIT 1')
    user = c.fetchone()
    
    if not user or not user['api_key']:
        print("警告: 未找到 API Key 配置，将使用 PIL 进行基础颜色提取。")
        api_key = None
        base_url = None
        model = None
    else:
        api_key = user['api_key']
        base_url = user['api_base_url']
        model = user['api_model']
    
    updated_count = 0
    
    # 预设颜色选项 (用于匹配)
    COLOR_OPTIONS = ["黑色", "白色", "灰色", "米色", "卡其色", "棕色", "红色", "粉色", "橙色", "黄色", "绿色", "蓝色", "紫色", "花色", "其他"]
    
    for row in rows:
        image_path = os.path.join(os.getcwd(), row['image_path'])
        
        if not os.path.exists(image_path):
            print(f"Skipping {row['id']}: Image not found at {image_path}")
            continue
            
        print(f"Analyzing item {row['id']} ({row['category']})...")
        
        try:
            detected_color = analyze_image_color(image_path, api_key, base_url, model)
            
            # 尝试标准化颜色名称
            final_color = "其他"
            if detected_color:
                for opt in COLOR_OPTIONS:
                    if opt in detected_color:
                        final_color = opt
                        break
            
            # 更新数据库
            c.execute("UPDATE clothes SET color = ? WHERE id = ?", (final_color, row['id']))
            conn.commit()
            updated_count += 1
            print(f"  -> Updated to: {final_color}")
            
        except Exception as e:
            print(f"  -> Error: {e}")
            
    conn.close()
    print(f"Batch update completed. Updated {updated_count} items.")

if __name__ == "__main__":
    batch_update_colors()
