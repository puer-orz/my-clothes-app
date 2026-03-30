import streamlit as st
import time
import json
from streamlit_js_eval import streamlit_js_eval
from utils.database import get_user_settings, get_all_clothes, save_history, get_today_history, delete_today_history
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

# 获取 HTML5 浏览器地理位置 (最高精度)
browser_location = streamlit_js_eval(
    js_expressions="""
    new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            position => resolve({lat: position.coords.latitude, lon: position.coords.longitude}),
            error => resolve({error: error.message})
        )
    })
    """,
    key="browser_location"
)

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

        # 自定义 CSS 优化信息栏样式
        st.markdown("""
        <style>
        /* 1. 基础文字样式 */
        .info-label {
            font-size: 12px;
            color: rgba(255,255,255,0.6);
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.2;
            white-space: nowrap !important; /* 强制不换行 */
        }
        .info-value {
            font-size: 16px;
            font-weight: 500;
            color: rgba(255,255,255,0.95);
            margin-top: 2px;
        }
        
        /* 2. 刷新按钮样式：终极修正，使用 !important 覆盖一切 */
        /* 针对 secondary 类型的按钮，彻底清除所有边框和背景 */
        button[kind="secondary"], 
        button[kind="secondary"]:focus,
        button[kind="secondary"]:active {
            border: 0px solid transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            outline: none !important;
            color: rgba(255,255,255,0.6) !important;
            padding: 0 !important;
            margin: 0 !important;
            min-height: 0 !important;
            height: auto !important;
            line-height: 1.2 !important;
            display: flex !important;
            align-items: center !important;
            transform: translateY(6px) !important; /* 继续加大下移量，从 3px 增加到 6px */
            margin-left: -25px !important; /* 继续加大负边距，从 -15px 增加到 -25px */
        }
        button[kind="secondary"]:hover {
            border: 0px solid transparent !important;
            background-color: transparent !important;
            color: #fff !important;
        }
        
        /* 隐藏按钮内的任何额外容器的边距 */
        button[kind="secondary"] > div {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }

        /* 3. 强制所有列的内容顶部对齐 */
        /* Streamlit 的列默认是 top 对齐的，但内部元素可能有 margin 差异 */
        /* 统一所有 .info-label 的 margin */
        .info-label {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            line-height: 1.5 !important; /* 统一行高 */
            height: 24px !important; /* 强制统一高度 */
            display: flex !important;
            align-items: center !important;
        }
        
        /* 4. 强制刷新按钮容器的高度与 label 一致 */
        div[data-testid="column"] button[kind="secondary"] {
            height: 24px !important; /* 与 label 高度一致 */
        }
        
        /* 3. 换搭配按钮样式 */
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: transparent !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            color: rgba(255, 255, 255, 0.9) !important;
            padding: 2px 8px !important;
            height: 28px !important;
            font-size: 13px !important;
            border-radius: 14px !important;
            width: auto !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # 展示天气卡片
        # 终极物理对齐方案：将标题行和数值行彻底拆分为两个独立的 st.columns
        # 这样无论第一行的按钮如何折腾，第二行的数值永远在同一水平线上
        
        # --- 第一行：标题 ---
        h_col1, h_col2, h_col3, h_col4 = st.columns(4)
        
        with h_col1:
            # 嵌套列：地点 + 按钮
            # 保持之前的紧凑布局
            sub_c1, sub_c2 = st.columns([1.5, 5], gap="small", vertical_alignment="center")
            with sub_c1:
                st.markdown("<div class='info-label'>地点</div>", unsafe_allow_html=True)
            with sub_c2:
                # 刷新按钮
                if st.button("⟳", key="refresh_top", help="刷新定位与天气"):
                    # 重置状态，强制重新获取 HTML5 定位
                    if 'browser_location' in st.session_state:
                        del st.session_state['browser_location']
                    delete_today_history()
                    time.sleep(0.5)
                    st.rerun()
        
        with h_col2:
            st.markdown("<div class='info-label'>天气</div>", unsafe_allow_html=True)
            
        with h_col3:
            st.markdown("<div class='info-label'>气温</div>", unsafe_allow_html=True)
            
        with h_col4:
            st.markdown("<div class='info-label'>体感</div>", unsafe_allow_html=True)
            
        # --- 第二行：数值 ---
        # 使用一个新的 columns 容器，确保所有数值的起点绝对一致
        v_col1, v_col2, v_col3, v_col4 = st.columns(4)
        
        with v_col1:
            location_name = weather.get('location', '本地')
            st.markdown(f"<div class='info-value'>{location_name}</div>", unsafe_allow_html=True)
            
        with v_col2:
            st.markdown(f"<div class='info-value'>{weather.get('description', '未知')}</div>", unsafe_allow_html=True)
            
        with v_col3:
            st.markdown(f"<div class='info-value'>{weather.get('temp', 'N/A')}°C</div>", unsafe_allow_html=True)
            
        with v_col4:
            st.markdown(f"<div class='info-value'>{weather.get('feels_like', 'N/A')}°C</div>", unsafe_allow_html=True)
            
        # 补充 CSS：消除两行之间的过大间距
        st.markdown("""
        <style>
        /* 减少第一行标题和第二行数值之间的距离 */
        /* 选中包含标题的第一行 columns */
        div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div:nth-last-child(2) {
            /* 这是一个比较模糊的选择器，我们尝试用更通用的方式：减少 info-label 的容器底部边距 */
        }
        
        /* 暴力消除两行 columns 之间的默认 gap */
        div.stMarkdown {
            margin-bottom: 0 !important;
        }
        
        /* 专门针对我们拆分出来的两行 columns 容器，拉近它们的距离 */
        /* 这种结构下，两个 st.columns 之间会有默认的垂直间距。我们可以通过负 margin 来拉近 */
        div[data-testid="column"] .info-value {
            margin-top: -15px !important; /* 向上拉，抵消 st.columns 之间的间距 */
        }
        </style>
        """, unsafe_allow_html=True)
            
        st.divider()
        
        st.success("已为您加载今日的穿搭方案")
        
        # 搭配思路标题 + 换一组按钮
        # 使用三列布局：标题 | 按钮 | 空白
        # 通过精细的比例控制 [1.2, 1.5, 7.3]，让标题列极度收缩
        col_title, col_btn, _ = st.columns([1.2, 1.5, 7.3], gap="small", vertical_alignment="center")
        
        with col_title:
            # 使用 HTML h3 以消除默认 margin 并防止换行，确保紧凑
            st.markdown("<h3 style='margin:0; padding:0; white-space:nowrap; font-size: 1.3rem; font-weight: 600;'>搭配思路</h3>", unsafe_allow_html=True)
            
        with col_btn:
            # 扁平风格按钮 "换一组" -> 改为 "换搭配"，并且使用 primary 样式
            # 强制按钮左对齐
            st.markdown("""
            <style>
            div[data-testid="column"] button[kind="primary"] {
                margin-left: -15px !important; /* 从 -25px 调整回 -15px，保持适中距离 */
                float: left !important;
            }
            </style>
            """, unsafe_allow_html=True)
            if st.button("换搭配", type="primary", use_container_width=False):
                # 获取当前的 outfit_ids，作为排除项传给 AI
                current_ids = result.get('outfit_ids', [])
                
                with st.spinner("正在为您重新搭配..."):
                    # 重新调用 AI 生成
                    # 需要重新获取天气数据 (可以直接复用当前的 weather 字典)
                    # 重新调用 get_ai_recommendation
                    
                    api_model = user['api_model'] if user and 'api_model' in user.keys() and user['api_model'] else "deepseek-chat"
                    
                    # 构造 weather_data 格式
                    weather_data = weather.copy() # 复用当前展示的天气
                    if 'raw' not in weather_data:
                        weather_data['raw'] = f"{weather.get('description','')} {weather.get('temp','')}度"

                    new_result = get_ai_recommendation(
                        weather_data,
                        dict(user),
                        clothes,
                        user['api_key'],
                        user['api_base_url'],
                        model_name=api_model,
                        exclude_outfit_ids=current_ids # 传入要排除的 ID
                    )
                    
                    if "error" not in new_result:
                        # 更新数据库中的今日记录 (覆盖旧的)
                        combined_result = {
                            "weather": weather_data,
                            "outfit": new_result
                        }
                        # 保存 (save_history 内部逻辑是 insert，我们需要 update 或者 delete insert)
                        # 简单起见，先 delete 再 save
                        delete_today_history()
                        save_history(
                            new_result.get('recommendation_text', ''), 
                            weather_data.get('raw', ''), 
                            combined_result # save_history 会处理 json.dumps
                        )
                        st.rerun()
                    else:
                        st.error(f"生成失败: {new_result['error']}")
        
        st.markdown(f"{result.get('recommendation_text', '暂无详细描述')}")
        
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
            
        # 移除底部的重复刷新按钮，只保留顶部的
        # st.divider()
        # if st.button("🔄 不满意？重新生成今日搭配", ...):
        #     ...
            
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
                
                weather_data = None
                location_display = "未知地点"
                
                # 优先级 1: HTML5 浏览器定位 (最高精度)
                if browser_location and 'lat' in browser_location:
                    try:
                        lat = browser_location['lat']
                        lon = browser_location['lon']
                        # 使用经纬度去反查城市名 (这里简单调用 Open-Meteo，它其实不需要城市名，只需要经纬度)
                        # 如果需要城市名，可以通过经纬度调用高德/百度 API，这里我们暂且显示坐标或让 AI 猜
                        location_display = f"经度:{lon:.2f}, 纬度:{lat:.2f}" 
                        weather_data = get_weather_from_open_meteo(lat, lon)
                        if weather_data:
                            weather_data['location'] = "精准定位"
                    except Exception as e:
                        print(f"Browser location error: {e}")
                
                # 优先级 2: IP 定位 (如果不允许浏览器定位或失败)
                if not weather_data:
                    loc_data = get_current_location_data()
                    if loc_data and loc_data.get('lat') and loc_data.get('lon'):
                        location_display = loc_data['display']
                        weather_data = get_weather_from_open_meteo(loc_data['lat'], loc_data['lon'])
                        if weather_data:
                            weather_data['location'] = location_display
                
                # 优先级 3: 兜底交由 AI 猜测 (如果上面全挂了，或者获取到了地址但没获取到天气)
                if not weather_data:
                    st.info("正在尝试通过 AI 智能推测...")
                    api_model = user['api_model'] if user and 'api_model' in user.keys() and user['api_model'] else "deepseek-chat"
                    
                    weather_data = get_weather_from_ai(
                        location_display, # 传入当前的 location_display，如果为空或未知，AI服务内部会处理
                        user['api_key'], 
                        user['api_base_url'], 
                        api_model
                    )
                
                if weather_data and "error" not in weather_data:
                    st.write(f"获取到天气: {weather_data.get('raw', 'AI 生成数据')}")
                    # 确保使用 AI 推测的城市名称覆盖原来的“未知地点”
                    if 'location' in weather_data and weather_data['location'] != "未知":
                        location_display = weather_data['location']
                else:
                    st.warning("天气获取失败，将使用默认数据。")
                    weather_data = {
                        "raw": "天气未知，请根据季节自行判断。", 
                        "description": "未知", 
                        "temp": "N/A", 
                        "location": "未知",
                        "feels_like": "N/A"
                    }

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

    # 绘图功能 (已屏蔽：API 暂不支持)
    # if today_history or (st.session_state.get("generated_result")): 
    #     if st.checkbox("生成 AI 上身效果图 (需要额外消耗 Token)"):
    #          ...
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
            
    #                 with st.spinner("正在绘制效果图..."):
    #                     image_url = generate_image(current_result['image_prompt'], user['api_key'], user['api_base_url'])
    #                     if image_url:
    #                         st.image(image_url, caption="AI 生成的穿搭效果图", use_container_width=True)
    #                     else:
    #                         st.warning("绘图失败，可能是 API 不支持绘图功能。")
