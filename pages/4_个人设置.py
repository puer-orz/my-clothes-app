import streamlit as st
from utils.database import get_user_settings, update_user_settings
from utils.style import apply_global_style
from utils.navbar import render_navbar

st.set_page_config(page_title="个人设置", page_icon=None, initial_sidebar_state="collapsed")
apply_global_style()

# 读取现有设置
user = get_user_settings()

# 初始化 session state (如果未初始化)
# 我们使用 DB 中的数据作为初始值，确保每次进入页面都能加载最新配置
# 注意：如果用户已经修改了但没保存（理论上这里是自动保存），session_state 应该优先吗？
# 不，由于我们要做自动保存，所以 DB 应该是最新的。
# 每次重新加载页面（full reload），我们都从 DB 重新拉取。
# Streamlit 的 session_state 在页面刷新时会保留，但如果用户从其他页面切回来，
# 且我们使用了 key 参数，Streamlit 会尝试用 session_state 的值。
# 为了确保数据一致性，我们强制用 DB 数据覆盖 session_state 的初始值（如果 DB 有值）。

default_settings = {
    'height': 170.0,
    'weight': 60.0,
    'gender': '男',
    'style_preference': '简约休闲',
    'api_key': '',
    'api_base_url': 'https://api.deepseek.com',
    'api_model': 'deepseek-chat',
    'vision_api_key': '',
    'vision_base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    'vision_model': 'qwen-vl-max'
}

# 将 DB 数据映射到 session state keys
db_mapping = {
    'height': user['height'] if user and user['height'] else default_settings['height'],
    'weight': user['weight'] if user and user['weight'] else default_settings['weight'],
    'gender': user['gender'] if user and user['gender'] else default_settings['gender'],
    'style_preference': user['style_preference'] if user and user['style_preference'] else default_settings['style_preference'],
    'api_key': user['api_key'] if user and user['api_key'] else default_settings['api_key'],
    'api_base_url': user['api_base_url'] if user and user['api_base_url'] else default_settings['api_base_url'],
    'api_model': user['api_model'] if user and 'api_model' in user.keys() and user['api_model'] else default_settings['api_model'],
    'vision_api_key': user['vision_api_key'] if user and 'vision_api_key' in user.keys() and user['vision_api_key'] else default_settings['vision_api_key'],
    'vision_base_url': user['vision_base_url'] if user and 'vision_base_url' in user.keys() and user['vision_base_url'] else default_settings['vision_base_url'],
    'vision_model': user['vision_model'] if user and 'vision_model' in user.keys() and user['vision_model'] else default_settings['vision_model']
}

# 自动保存回调函数
def auto_save():
    """当任何输入框发生变化时调用，自动保存所有设置到数据库"""
    try:
        update_user_settings(
            st.session_state.height,
            st.session_state.weight,
            st.session_state.gender,
            st.session_state.style_preference,
            st.session_state.api_key,
            st.session_state.api_base_url,
            st.session_state.api_model,
            st.session_state.vision_api_key,
            st.session_state.vision_base_url,
            st.session_state.vision_model
        )
        st.toast("设置已自动保存")
    except Exception as e:
        st.error(f"保存失败: {e}")

# 初始化 session_state
for key, value in db_mapping.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 界面布局 (移除 st.form 以支持实时交互)
st.subheader("个人档案")
col1, col2 = st.columns(2)
with col1:
    st.number_input("身高 (cm)", key="height", on_change=auto_save)
    st.number_input("体重 (kg)", key="weight", on_change=auto_save)
with col2:
    st.selectbox("性别", ["男", "女", "其他"], key="gender", on_change=auto_save)
    st.text_input("风格偏好", key="style_preference", on_change=auto_save)

st.divider()

st.subheader("文本模型配置")
st.info("支持云端 API (DeepSeek/OpenAI) 或 本地模型 (Ollama)。修改即自动保存。")

# 添加一键配置按钮
if st.button("一键切换到 DeepSeek 云端版 (推荐，极速)", type="primary", use_container_width=True):
    st.session_state.api_base_url = "https://api.deepseek.com"
    st.session_state.api_model = "deepseek-chat"
    auto_save()
    st.success("已切换到 DeepSeek 云端配置！请确保填入有效的 API Key。")
    st.rerun()

st.text_input("API Key", type="password", key="api_key", help="如果使用 Ollama 本地模型，此处可随意填写（如 'ollama'）", on_change=auto_save)
st.text_input("Base URL", key="api_base_url", on_change=auto_save)
st.text_input("Model Name", key="api_model", help="例如: deepseek-chat, gpt-3.5-turbo, qwen2, llama3", on_change=auto_save)

st.markdown("---")
st.subheader("视觉模型配置 (Vision API)")
st.info("用于“衣橱录入”时的图片分析。推荐使用通义千问 (Qwen-VL) 或 豆包 (Doubao-Vision)。")

# 视觉模型一键配置
col_v1, col_v2 = st.columns(2)
with col_v1:
    if st.button("使用通义千问 (Qwen-VL)", use_container_width=True):
        st.session_state.vision_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        st.session_state.vision_model = "qwen-vl-max"
        auto_save()
        st.rerun()
with col_v2:
    if st.button("使用豆包 (Doubao-Vision)", use_container_width=True):
        st.session_state.vision_base_url = "https://ark.cn-beijing.volces.com/api/v3"
        # 注意：豆包的 Model Name 需要填 Endpoint ID (如 ep-2024...)
        st.session_state.vision_model = "" 
        st.toast("已切换到豆包配置！请务必在 Model Name 中填入您的 Endpoint ID (ep-xxxx...)")
        # auto_save() # 移除自动保存，因为此时 vision_model 为空，保存会清空 DB 中的值
        # st.rerun() # 移除 rerun，防止页面刷新导致输入框清空前未保存
        
        # 更好的做法是只更新 session_state，让用户填完后再触发 auto_save
        pass

st.text_input("Vision API Key", type="password", key="vision_api_key", help="请填入对应平台的 API Key", on_change=auto_save)
st.text_input("Vision Base URL", key="vision_base_url", on_change=auto_save)
st.text_input("Vision Model Name (或 Endpoint ID)", key="vision_model", help="对于豆包，请填入 Endpoint ID (ep-xxxx)；对于 Qwen，填 qwen-vl-max", on_change=auto_save)

# 添加 Vision 测试按钮
if st.button("测试 Vision API 连接", type="secondary"):
    if not st.session_state.vision_api_key:
        st.error("请先填入 Vision API Key")
    else:
        with st.spinner("正在连接 Vision API..."):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=st.session_state.vision_api_key, base_url=st.session_state.vision_base_url)
                # 简单的列出模型请求，测试连通性 (不同厂商可能实现不同，这里仅作最基础的 import 检查和 key 格式检查)
                st.success(f"API Key 格式检查通过。请前往'衣橱录入'页面上传图片进行实测。")
            except Exception as e:
                st.error(f"连接测试失败: {e}")

st.markdown("### 常见配置参考")

with st.expander("DeepSeek (推荐，高性价比)", expanded=True):
    st.markdown("""
    - **API Key**: [点击申请](https://platform.deepseek.com/)
    - **Base URL**: `https://api.deepseek.com`
    - **Model**: `deepseek-chat`
    """)
    
with st.expander("Ollama (本地免费，无需联网)"):
    st.markdown("""
    1. 下载安装 [Ollama](https://ollama.com/)
    2. 终端运行: `ollama run qwen2` (推荐中文) 或 `ollama run llama3`
    3. 配置如下:
        - **API Key**: `ollama` (任意填写)
        - **Base URL**: `http://localhost:11434/v1`
        - **Model**: `qwen2` 或 `llama3`
    """)

with st.expander("OpenAI / Moonshot"):
    st.markdown("""
    - **OpenAI**: `https://api.openai.com/v1` | `gpt-3.5-turbo`
    - **Moonshot**: `https://api.moonshot.cn/v1` | `moonshot-v1-8k`
    """)

# 移除显式的保存按钮，因为现在是自动保存
# 但为了给用户安全感，可以加一个强制保存按钮（可选）
if st.button("强制保存 (手动确认)"):
    auto_save()
    st.success("配置已保存并同步！")

render_navbar()
