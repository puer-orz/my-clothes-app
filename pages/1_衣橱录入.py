import streamlit as st
import os
import time
from utils.database import save_clothes, get_user_settings
from PIL import Image
from utils.style import apply_global_style
from utils.navbar import render_navbar
from utils.ai_service import analyze_image_color, analyze_image_content

st.set_page_config(page_title="衣橱录入", page_icon=None, layout="wide", initial_sidebar_state="expanded")
apply_global_style()
render_navbar()

# 获取用户配置以便调用 AI
user = get_user_settings()

# 使用 session_state 来控制表单重置
if 'upload_key' not in st.session_state:
    st.session_state.upload_key = 0

# 存储 AI 识别的颜色 (字典：filename -> color)
if 'detected_colors' not in st.session_state:
    st.session_state.detected_colors = {}

# 存储 AI 识别的描述 (字典：filename -> description)
if 'detected_descriptions' not in st.session_state:
    st.session_state.detected_descriptions = {}

# 存储已保存的文件 (集合：filename)
if 'saved_files' not in st.session_state:
    st.session_state.saved_files = set()

def reset_form():
    st.session_state.upload_key += 1
    st.session_state.detected_colors = {}
    st.session_state.detected_descriptions = {}
    st.session_state.saved_files = set()

# 颜色选项
COLOR_OPTIONS = ["其他", "黑色", "白色", "灰色", "米色", "卡其色", "棕色", "红色", "粉色", "橙色", "黄色", "绿色", "蓝色", "紫色", "花色"]

# --- 1. 顶部提示区域 ---
st.info("👈 请先在左侧上传图片，AI 将辅助您完成录入")

# --- 2. 上传区域 (全宽) ---
# 使用 CSS 强制固定宽度，避免 file_uploader 上传前后宽度跳变
st.markdown("""
<style>
/* 固定上传区域的最大宽度，使其与上下文保持一致 */
[data-testid="stFileUploader"] {
    max-width: 100%; 
    width: 100%;
}
/* 修复 section 容器的宽度跳变问题 - 使用更高权重 */
section[data-testid="stFileUploaderDropzone"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    box-sizing: border-box !important;
    min-height: 150px;
}
/* 针对上传后的文件列表容器 */
[data-testid="stFileUploader"] > div > div {
    width: 100% !important;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "上传图片 (支持多选)", 
    type=['jpg', 'jpeg', 'png', 'webp'], 
    accept_multiple_files=True, 
    key=f"uploader_{st.session_state.upload_key}"
)

# --- 3. 内容编辑区域 ---
if uploaded_files:
    st.divider()
    
    # 图片选择器 (如果有多张)
    selected_index = 0
    if len(uploaded_files) > 1:
        st.write("### 选择要编辑的图片")
        # 使用文件名列表供选择
        file_names = [f"{i+1}. {f.name}" + (" (已保存)" if f.name in st.session_state.saved_files else "") for i, f in enumerate(uploaded_files)]
        
        # 使用 pills (如果版本支持) 或 radio
        # 这里使用 radio horizontal 模拟 tab 效果，或者使用 columns 放置缩略图按钮（太复杂），简单点用 radio/pills
        # 考虑到 Streamlit 版本，这里用 horizontal radio 比较稳妥
        selected_option = st.radio("切换图片:", file_names, horizontal=True, label_visibility="collapsed")
        selected_index = file_names.index(selected_option)
    
    current_file = uploaded_files[selected_index]
    is_saved = current_file.name in st.session_state.saved_files
    
    # 布局：左侧预览 (小)，右侧表单 (大)
    col_preview, col_form = st.columns([1, 3])
    
    with col_preview:
        st.markdown("#### 图片预览")
        image = Image.open(current_file)
        st.image(image, use_container_width=True)
        
        # AI 颜色识别逻辑
        current_color = st.session_state.detected_colors.get(current_file.name, "未知")
        current_description = st.session_state.detected_descriptions.get(current_file.name, "")
        
        if (current_color == "未知" or not current_description) and not is_saved:
            with st.spinner("正在分析图片..."):
                # 1. 颜色识别 (原逻辑)
                if current_color == "未知":
                    detected = analyze_image_color(
                        current_file, 
                        user['api_key'] if user else None, 
                        user['api_base_url'] if user else None,
                        user['api_model'] if user else None
                    )
                    if detected:
                        found = False
                        for opt in COLOR_OPTIONS:
                            if opt in detected:
                                current_color = opt
                                found = True
                                break
                        if not found:
                            current_color = "其他"
                        st.session_state.detected_colors[current_file.name] = current_color
                
                # 2. 详细描述识别 (Vision API)
                # 检查是否配置了 Vision API
                if user and 'vision_api_key' in user.keys() and user['vision_api_key']:
                    vision_desc, vision_info = analyze_image_content(
                        current_file,
                        user['vision_api_key'],
                        user['vision_base_url'],
                        user['vision_model']
                    )
                    
                    if vision_desc:
                        current_description = vision_desc
                        st.session_state.detected_descriptions[current_file.name] = current_description
                        
                    # 如果 Vision API 返回了结构化信息，用它来更新颜色和分类
                    if vision_info:
                        if 'color' in vision_info:
                            # 尝试匹配已有的颜色选项
                            found = False
                            for opt in COLOR_OPTIONS:
                                if opt in vision_info['color']:
                                    current_color = opt
                                    found = True
                                    break
                            if not found and vision_info['color']:
                                # 如果是全新的颜色，也许可以考虑作为“其他”或者直接使用 AI 的描述（如果允许新增）
                                # 这里我们保守一点，还是归为“其他”，但可以在界面上显示出来
                                current_color = "其他" 
                            
                            st.session_state.detected_colors[current_file.name] = current_color
                            
                        # 我们还可以把 category 存起来，虽然目前 session_state 没专门存 category
                        # 但我们可以临时存到 detected_descriptions 的附加字段里，或者直接刷新后在下面的 default value 里用
                        if 'category' in vision_info:
                            st.session_state.detected_category = st.session_state.get('detected_category', {})
                            st.session_state.detected_category[current_file.name] = vision_info['category']
                
                st.rerun() # 刷新以更新表单默认值
        
        if current_color != "未知":
            st.caption(f"🎨 AI 识别颜色: **{current_color}**")
        if current_description:
            st.caption("📝 AI 已生成详细描述")

    with col_form:
        st.markdown(f"#### 单品详情 - {current_file.name}")
        
        if is_saved:
            st.success("✅ 该单品已保存！")
            st.info("💡 您可以点击上方标签切换到其他图片继续录入，或者点击下方按钮开始新的一批。")
            if st.button("清空并开始新的一批", type="primary"):
                reset_form()
                st.rerun()
        else:
            with st.form(f"form_{selected_index}", clear_on_submit=False):
                # 第一行：分类、颜色、尺码
                c1, c2, c3 = st.columns(3)
                
                # 获取 AI 识别的分类
                ai_category = st.session_state.get('detected_category', {}).get(current_file.name, "上衣")
                category_options = ["上衣", "裤子", "裙子", "外套", "鞋子", "包袋", "配饰", "其他"]
                # 尝试匹配
                cat_index = 0
                for i, opt in enumerate(category_options):
                    if opt in ai_category:
                        cat_index = i
                        break
                
                with c1:
                    category = st.selectbox("分类", category_options, index=cat_index)
                
                with c2:
                    # 颜色选择器 (自动填充 AI 结果)
                    try:
                        color_index = COLOR_OPTIONS.index(current_color) if current_color in COLOR_OPTIONS else 0
                    except:
                        color_index = 0
                        
                    color = st.selectbox("颜色 (AI)", COLOR_OPTIONS, index=color_index)
                    
                with c3:
                    # 尺码逻辑 - 默认为"均码"
                    size_options = ["XS", "S", "M", "L", "XL", "XXL", "均码", "其他"]
                    if category == "鞋子":
                        size_options = [str(i) for i in range(34, 47)] + ["其他"]
                    elif category in ["包袋", "配饰", "其他"]:
                        size_options = ["均码", "其他"]
                    
                    # 默认选中"均码" (index 6)
                    default_size_index = 6 if "均码" in size_options else 0
                    size = st.selectbox("尺码", size_options, index=default_size_index)
                
                # 第二行：季节
                season = st.multiselect("适用季节", ["春", "夏", "秋", "冬"], default=["春", "秋"])
                
                # 自动填充 AI 描述
                default_desc = current_description if current_description else ""
                description = st.text_area("描述 (AI 辅助生成)", value=default_desc, placeholder="AI 将自动识别图片细节并填入此处...", height=100)
                
                # 提交按钮
                submitted = st.form_submit_button("保存当前单品", use_container_width=True, type="primary")
            
            if submitted:
                try:
                    # 1. 保存图片
                    assets_dir = os.path.join(os.getcwd(), 'assets')
                    if not os.path.exists(assets_dir):
                        os.makedirs(assets_dir)
                        
                    file_ext = os.path.splitext(current_file.name)[1]
                    filename = f"{int(time.time())}_{selected_index}_{category}{file_ext}"
                    file_path = os.path.join(assets_dir, filename)
                    
                    with open(file_path, "wb") as f:
                        f.write(current_file.getbuffer())
                    
                    # 2. 保存数据库
                    rel_path = os.path.join('assets', filename)
                    season_str = ",".join(season)
                    final_desc = description if description else f"{category} (未填写描述)"
                    
                    save_clothes(category, rel_path, final_desc, size, season_str, color)
                    
                    # 3. 标记为已保存
                    st.session_state.saved_files.add(current_file.name)
                    st.toast(f"✅ {current_file.name} 保存成功！")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"保存失败: {str(e)}")

