import streamlit as st
import time
import json
from utils.database import get_user_settings, get_all_clothes, save_history, get_today_history
from utils.ai_service import get_ai_recommendation, generate_image, get_weather_from_ai, get_weather_and_outfit_combined
from utils.style import apply_global_style
from utils.navbar import render_navbar
from utils.helpers import get_current_location, get_current_location_data, get_weather_from_open_meteo

st.set_page_config(page_title="今日穿搭", page_icon=None, initial_sidebar_state="collapsed")
apply_global_style()
render_navbar()

# 获取数据
user = get_user_settings()
clothes = [dict(row) for row in get_all_clothes()]

# 检查 API Key
if not user or not user['api_key']:
    st.warning("请先在 [个人设置](/个人设置) 中配置 API Key，否则无法使用 AI 推荐功能。")
    st.info("推荐使用 DeepSeek API (性价比高) 或 OpenAI API。")
else:
    # 检查是否已有今日推荐 (提前检查，如果有了就不用任何 AI 调用)
    today_history = get_today_history()
    
    if today_history:
        # 如果有记录，直接展示，不需要再请求 AI 获取天气或穿搭
        # 但我们需要解析出 weather 信息来展示天气卡片
        weather = {}
        result = {}
        
        if today_history['result_json']:
            try:
                full_result = json.loads(today_history['result_json'])
                # 兼容新旧格式：新格式是 {weather:..., outfit:...}，旧格式直接是 outfit
                if 'weather' in full_result and 'outfit' in full_result:
                    weather = full_result['weather']
                    result = full_result['outfit']
                else:
                    # 旧数据，weather 存储在 weather_info 字段
                    result = full_result
                    # 尝试从 raw string 解析 weather (不够准，但兼容旧数据)
                    weather = {'description': '历史数据', 'temp': 'N/A', 'feels_like': 'N/A', 'raw': today_history['weather_info']}
            except:
                pass
        
        # 兼容旧数据 fallback
        if not result and today_history['recommendation']:
            result['recommendation_text'] = today_history['recommendation']
            weather = {'description': '历史数据', 'temp': 'N/A', 'feels_like': 'N/A', 'raw': today_history['weather_info']}

        # 展示天气卡片 (从历史记录中恢复)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("地点", "历史记录")
            st.caption(f"天气: {weather.get('description', '未知')}")
        with col2:
            st.metric("气温", f"{weather.get('temp', 'N/A')}°C")
        with col3:
            st.metric("体感", f"{weather.get('feels_like', 'N/A')}°C")
            
        st.divider()
        
        st.success("已为您加载今日的穿搭方案")
        st.markdown(f"### 搭配思路\n{result.get('recommendation_text', '暂无详细描述')}")
        
        # 展示衣物
        if 'outfit_ids' in result:
            st.subheader("推荐单品")
            cols = st.columns(3)
            recommended_ids = result['outfit_ids']
            
            found_count = 0
            for item in clothes:
                if item['id'] in recommended_ids:
                    with cols[found_count % 3]:
                        if item['image_path']:
                            st.image(item['image_path'], use_container_width=True)
                        st.caption(f"{item['category']} - {item['season']}")
                    found_count += 1
        
        if result.get('missing_items'):
            st.info(f"**搭配建议**: {result['missing_items']}")
            
    else:
        # 如果没有记录，需要生成
        if not clothes:
            st.error("衣橱里还没有衣服呢！请先去 [录入](/衣橱录入) 一些衣服吧。")
        else:
            # 这里的逻辑完全变了：
            # 1. 快速获取天气 (Open-Meteo)
            # 2. 调用 AI 进行穿搭推荐 (将真实天气传给 AI)
            
            with st.status("正在分析天气与衣橱...", expanded=True) as status:
                st.write("正在定位并获取实时天气...")
                
                # 获取位置和天气
                loc_data = get_current_location_data()
                weather_data = None
                
                if loc_data:
                    st.write(f"已定位: {loc_data['display']}")
                    weather_data = get_weather_from_open_meteo(loc_data['lat'], loc_data['lon'])
                else:
                    st.warning("定位失败，默认使用北京天气。")
                    weather_data = get_weather_from_open_meteo(39.90, 116.40) # 北京坐标
                
                if weather_data:
                    st.write(f"获取到实时天气: {weather_data['raw']}")
                else:
                    st.warning("天气获取失败，将由 AI 自行推测。")
                    weather_data = {"raw": "天气获取失败，请根据季节推测。", "description": "未知", "temp": "N/A"}

                st.write("AI 正在为您挑选最佳搭配...")
                api_model = user['api_model'] if user and 'api_model' in user.keys() and user['api_model'] else "deepseek-chat"
                
                # 调用 AI (仅穿搭)
                # 复用 get_ai_recommendation，它接收 weather_info
                result = get_ai_recommendation(
                    weather_data,
                    dict(user),
                    clothes,
                    user['api_key'],
                    user['api_base_url'],
                    api_model
                )
                
                if "error" in result:
                    status.update(label="生成失败", state="error")
                    st.error(result["error"])
                else:
                    status.update(label="搭配完成！", state="complete")
                    
                    # 构造 combined result 格式以便统一存储
                    combined_result = {
                        "weather": weather_data,
                        "outfit": result
                    }
                    
                    # 保存历史记录
                    save_history(result.get('recommendation_text', ''), weather_data.get('raw', ''), combined_result)
                    
                    # 刷新页面
                    st.rerun()

    # 绘图功能 (保持手动触发)
    # ... (代码不变)
    if today_history or (st.session_state.get("generated_result")): 
        if st.checkbox("生成 AI 上身效果图 (需要额外消耗 Token)"):
             # 需要重新获取 result 对象 (如果是在 history 分支里)
            current_result = result if 'result' in locals() else {}
            if not current_result and today_history and today_history['result_json']:
                 # 重新解析
                 try:
                     full = json.loads(today_history['result_json'])
                     if 'outfit' in full:
                         current_result = full['outfit']
                     else:
                         current_result = full
                 except:
                     pass
            
            if current_result and 'image_prompt' in current_result:
                with st.spinner("正在绘制效果图..."):
                    image_url = generate_image(current_result['image_prompt'], user['api_key'], user['api_base_url'])
                    if image_url:
                        st.image(image_url, caption="AI 生成的穿搭效果图", use_container_width=True)
                    else:
                        st.warning("绘图失败，可能是 API 不支持绘图功能。")
