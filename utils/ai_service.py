import json
from openai import OpenAI
import streamlit as st

from datetime import datetime

import base64
from PIL import Image
import io

def encode_image(image_file):
    """将上传的文件对象转换为 Base64 字符串"""
    if isinstance(image_file, (str, bytes)):
        # 如果是路径或字节流
        return base64.b64encode(image_file).decode('utf-8')
    else:
        # 如果是 Streamlit UploadedFile 对象
        return base64.b64encode(image_file.getvalue()).decode('utf-8')

def analyze_image_content(image_file, api_key, base_url, model_name="qwen-vl-max"):
    """
    使用 Vision 模型分析图片内容，返回详细的文字描述。
    支持 Qwen-VL, Doubao-Vision, GPT-4o 等 OpenAI 兼容格式。
    """
    if not api_key:
        return None
        
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        base64_image = encode_image(image_file)
        
        system_prompt = """
        你是一位专业的时尚买手和服装设计师。
        请仔细观察这张图片中的衣物，并生成一段详细的、专业的描述。
        
        描述应包含以下要素（如果可见）：
        1. **基础信息**：颜色（包括色调、饱和度）、类别（如卫衣、衬衫、半身裙）。
        2. **设计细节**：版型（宽松/修身）、领型、袖型、衣长。
        3. **材质纹理**：面料质感（如牛仔、丝绸、针织）、是否有图案或印花。
        4. **风格特征**：如复古、极简、街头、商务等。
        
        此外，请在最后额外输出一行 JSON 格式的结构化信息（不要包含在描述段落中，单独一行），用于自动填表：
        {"category": "上衣/裤子/裙子/外套/鞋子/包袋/配饰/其他", "color": "黑色/白色/灰色/米色/卡其色/棕色/红色/粉色/橙色/黄色/绿色/蓝色/紫色/花色/其他"}
        
        注意：
        - category 必须从给定的选项中选择最接近的一个。
        - color 必须从给定的选项中选择最接近的一个。
        
        请直接输出描述文本，然后在最后一行输出 JSON。
        """
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": system_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        content = response.choices[0].message.content.strip()
        
        # 解析混合输出 (文本描述 + JSON)
        description = content
        extracted_info = {}
        
        try:
            # 尝试找到最后一行 JSON
            lines = content.split('\n')
            last_line = lines[-1].strip()
            if last_line.startswith('{') and last_line.endswith('}'):
                extracted_info = json.loads(last_line)
                # 移除 JSON 行，保留纯描述
                description = '\n'.join(lines[:-1]).strip()
        except:
            pass
            
        return description, extracted_info
            
    except Exception as e:
        print(f"Vision Analysis Error: {e}")
        return None, {}

def analyze_image_color(image_file, api_key, base_url, model_name="gpt-4o"):
    """
    分析图片颜色
    优先尝试使用 Vision 模型 (如 gpt-4o)，如果失败则使用 PIL 提取主色调
    """
    try:
        # 1. 尝试使用 Vision 模型
        # 注意：DeepSeek-V3 不支持 Vision，只有 gpt-4o, claude-3, gemini-pro-vision, llava 等支持
        # 我们简单判断一下模型名，如果是 text model 则跳过 Vision
        is_vision_model = any(m in model_name.lower() for m in ['gpt-4o', 'vision', 'llava', 'claude-3', 'gemini'])
        
        if is_vision_model and api_key:
            client = OpenAI(api_key=api_key, base_url=base_url)
            base64_image = encode_image(image_file)
            
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "请识别这件衣服的主要颜色。请只返回一个最准确的颜色词（例如：黑色、白色、藏青色、米色、卡其色、红色等），不要包含任何其他文字或标点。"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=10
            )
            color = response.choices[0].message.content.strip()
            return color
            
    except Exception as e:
        print(f"Vision API Error: {e}")
        # Fallback to PIL
        pass

    # 2. Fallback: 使用 PIL 提取主色调 (简单版)
    try:
        if isinstance(image_file, (str, bytes)):
             img = Image.open(io.BytesIO(image_file) if isinstance(image_file, bytes) else image_file)
        else:
             img = Image.open(image_file)
             
        # 调整大小以加快处理
        img = img.resize((50, 50))
        # 转换为 RGB
        img = img.convert("RGB")
        # 获取颜色直方图
        colors = img.getcolors(50*50)
        # 排序找到最多的颜色
        most_frequent_pixel = max(colors, key=lambda item: item[0])[1]
        
        # 简单的 RGB 到颜色名映射
        r, g, b = most_frequent_pixel
        
        # 非常简陋的映射，仅作示例
        if r > 200 and g > 200 and b > 200: return "白色"
        if r < 50 and g < 50 and b < 50: return "黑色"
        if r > 200 and g < 50 and b < 50: return "红色"
        if r < 50 and g > 200 and b < 50: return "绿色"
        if r < 50 and g < 50 and b > 200: return "蓝色"
        if r > 200 and g > 200 and b < 50: return "黄色"
        
        return "其他颜色" # 实在太难映射了
        
    except Exception as e:
        print(f"PIL Color Error: {e}")
        return "未知"

def get_weather_and_outfit_combined(location, user_profile, wardrobe_items, api_key, base_url, model_name="deepseek-chat"):
    """
    一次性调用 AI：获取天气预估 + 穿搭建议。
    优化速度，减少一次 LLM 往返。
    """
    if not api_key:
        return {"error": "未配置 API Key"}
        
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 构建衣橱数据的简化描述
        wardrobe_text = []
        for item in wardrobe_items:
            wardrobe_text.append({
                "id": item['id'],
                "category": item['category'],
                "desc": item['description'],
                "season": item['season']
            })
            
        system_prompt = """
        你是一位全能的个人生活助手，集成了【气象分析师】和【时尚搭配师】的能力。
        
        任务一：推测天气
        根据用户所在的地点和当前日期，推测当天的天气情况。如果无法获取实时数据，请根据该地点的气候特征和当前季节进行合理估算。
        
        任务二：推荐穿搭
        基于推测出的天气、用户的个人特征以及衣橱里的衣服，搭配出一套最合适的着装。
        
        请严格遵循以下 JSON 格式输出，不要输出任何额外的文本：
        {
            "weather": {
                "description": "天气状况 (如: 晴, 多云, 小雨)",
                "temp": "温度数值 (如: 25)",
                "humidity": "湿度数值 (如: 60)",
                "feels_like": "体感温度数值 (如: 27)",
                "raw": "一段完整的天气描述文本"
            },
            "outfit": {
                "reasoning": "简短的思考过程，分析天气和风格",
                "recommendation_text": "一段温馨、专业的推荐文案，解释为什么这样搭配，以及这套搭配的亮点。",
                "outfit_ids": [1, 5, 8],  // 推荐的衣服在衣橱中的 ID 列表（必须从提供的衣橱列表中选，不要捏造）
                "missing_items": "如果衣橱里的衣服不够完美，建议补充的单品（可选）",
                "image_prompt": "一段用于生成这套穿搭上身效果图的详细英文 Prompt"
            }
        }
        """
        
        user_message = f"""
        【当前状态】
        地点: {location}
        日期: {date_str}
        
        【用户信息】
        身高: {user_profile['height']}cm
        体重: {user_profile['weight']}kg
        性别: {user_profile['gender']}
        风格偏好: {user_profile['style_preference']}
        
        【我的衣橱】
        {json.dumps(wardrobe_text, ensure_ascii=False)}
        
        请一步到位，先推测天气，然后据此为我推荐今日穿搭。
        """
        
        response = client.chat.completions.create(
            model=model_name, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        # 清洗可能存在的 Markdown 代码块标记
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        
        result = json.loads(content.strip())
        return result
        
    except Exception as e:
        print(f"get_weather_and_outfit_combined error: {e}")
        return {"error": f"AI 调用失败: {str(e)}"}

def get_weather_from_ai(location, api_key, base_url, model_name="deepseek-chat"):
    """
    让 AI 推测天气。
    如果 location 无法获取（例如为"未知地点"），则让 AI 根据当前用户的 IP 或上下文自行推断位置和天气。
    """
    if not api_key:
        return {"error": "未配置 API Key"}

    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        system_prompt = """
        你是一个拥有联网能力和 IP 定位能力的智能天气助手。
        请根据用户的请求，获取当前的准确地点（城市）、天气状况、温度等信息。
        如果用户没有提供明确的地点，请你根据你接收到的请求来源 IP 或你的内置推测机制，猜一个最可能的中国城市（例如：北京、上海、广州、深圳、杭州等），并给出该城市今天的天气预估。
        
        请严格遵循以下 JSON 格式输出，不要输出任何其他多余的文字或 markdown 标记：
        {
            "location": "城市名称 (如: 杭州市)",
            "description": "天气状况 (如: 晴, 多云, 小雨)",
            "temp": "温度数值 (如: 22)",
            "humidity": "湿度数值 (如: 45)",
            "feels_like": "体感温度数值 (如: 24)",
            "wind": "风向风力 (如: 北风3级)",
            "raw": "一段完整的天气播报文本"
        }
        """
        
        if location and location != "未知地点":
            user_message = f"请查询 {location} 今天 ({date_str}) 的实时天气。"
        else:
            user_message = f"我不知道我现在在哪。请根据我的请求来源推测我的城市，并告诉我那里今天 ({date_str}) 的实时天气。"
        
        # 为了提高稳定性，去除强制 JSON mode，因为部分模型可能不支持或者在返回错误信息时解析失败
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        # 清洗 Markdown
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        result = json.loads(content.strip())
        
        # 确保返回的数据类型是字符串，避免页面渲染错误
        for k, v in result.items():
            result[k] = str(v)
            
        return result
        
    except Exception as e:
        print(f"get_weather_from_ai error: {e}")
        return {
            "location": "自动定位失败",
            "description": "未知",
            "temp": "N/A",
            "humidity": "N/A",
            "feels_like": "N/A",
            "raw": f"AI 天气获取失败: {str(e)}",
            "error": str(e)
        }

def get_ai_recommendation(weather_info, user_profile, wardrobe_items, api_key, base_url, model_name="deepseek-chat", exclude_outfit_ids=None):
    """
    调用 LLM 生成穿搭建议。
    增强逻辑：
    1. 利用详细描述 (detailed_description) 而非仅靠 category/desc 标签。
    2. 支持 exclude_outfit_ids 参数，用于生成不重复的搭配。
    """
    if not api_key:
        return {"error": "请先在'个人设置'中配置 API Key"}
    
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # 构建衣橱数据的简化描述
        wardrobe_text = []
        for item in wardrobe_items:
            # 优先使用详细描述
            desc = item.get('description', '')
            wardrobe_text.append({
                "id": item['id'],
                "category": item['category'],
                "details": desc, 
                "season": item['season'],
                "color": item.get('color', '')
            })
            
        system_prompt = """
        你是一位专业的个人形象顾问和时尚搭配师。
        你的任务是根据用户的个人特征、当天的天气以及用户衣橱里现有的衣服，搭配出一套最合适的着装。
        
        请特别注意衣橱清单中的 `details` 字段，那里可能包含衣服的材质、版型、风格等详细信息。请充分利用这些细节来做出更精准的搭配。
        """
        
        # 如果有排除列表，增加相应的 Prompt
        if exclude_outfit_ids and len(exclude_outfit_ids) > 0:
            system_prompt += f"""
            
            【重要限制】
            用户刚才已经尝试过一套搭配（包含单品ID: {exclude_outfit_ids}）。
            现在的任务是**生成一套全新的搭配**。
            1. **必须与上一套明显不同**：至少更换 50% 以上的单品，或者风格完全改变。
            2. **允许复用基础款**：比如鞋子或配饰可以重复，但核心单品（上衣、外套、裤子/裙子）最好更换。
            3. 请不要推荐与上一套极其相似的方案。
            """
        
        system_prompt += """
        请严格遵循以下输出格式（JSON）：
        {
            "reasoning": "简短的思考过程，分析天气、用户风格以及选中衣物的细节匹配度，并说明与上一套的区别（如果有）",
            "recommendation_text": "一段温馨、专业的推荐文案，解释为什么这样搭配，以及这套搭配的亮点。",
            "outfit_ids": [1, 5, 8],  // 推荐的衣服在衣橱中的 ID 列表（必须从提供的衣橱列表中选，不要捏造）
            "missing_items": "如果衣橱里的衣服不够完美，建议补充的单品（可选）",
            "image_prompt": "一段用于生成这套穿搭上身效果图的详细英文 Prompt，包含人物特征、衣服细节、姿势和背景。"
        }
        """
        
        user_message = f"""
        【用户信息】
        身高: {user_profile['height']}cm
        体重: {user_profile['weight']}kg
        性别: {user_profile['gender']}
        风格偏好: {user_profile['style_preference']}
        
        【今日天气】
        {weather_info['raw']}
        
        【我的衣橱】
        {json.dumps(wardrobe_text, ensure_ascii=False)}
        
        请为我推荐一套今日穿搭。
        """
        
        response = client.chat.completions.create(
            model=model_name, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        # 清洗可能存在的 Markdown 代码块标记
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        
        result = json.loads(content.strip())
        return result
        
    except Exception as e:
        print(f"get_ai_recommendation error: {e}")
        return {"error": f"AI 调用失败: {str(e)}"}

def generate_image(prompt, api_key, base_url):
    """
    调用绘图 API (支持 OpenAI DALL-E 3 和 SiliconFlow Flux)
    """
    try:
        # 检查是否是 SiliconFlow (api.siliconflow.cn)
        if "siliconflow" in base_url:
            client = OpenAI(api_key=api_key, base_url=base_url)
            # SiliconFlow 使用 Flux 模型，通常比 DALL-E 3 快且便宜
            response = client.images.generate(
                model="black-forest-labs/FLUX.1-schnell", # 极速版 Flux
                prompt=prompt,
                size="1024x1024",
                n=1,
            )
            return response.data[0].url
        else:
            # 默认 OpenAI
            client = OpenAI(api_key=api_key, base_url=base_url)
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return response.data[0].url
    except Exception as e:
        print(f"Image Gen Error: {e}")
        return None
