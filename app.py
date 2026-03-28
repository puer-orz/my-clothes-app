import streamlit as st
import os
from utils.database import init_db
from utils.style import apply_global_style
from utils.navbar import render_navbar

# 页面配置
st.set_page_config(
    page_title="穿搭衣橱",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed" # 默认收起
)

# 应用全局样式
apply_global_style()

# 渲染底部导航 (实际上是左侧悬浮导航)
render_navbar()

# 初始化数据库
if 'db_initialized' not in st.session_state:
    init_db()
    st.session_state['db_initialized'] = True

# 自定义 CSS 样式，打造简易高级风
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #2c3e50;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #34495e;
        color: white;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    .css-1d391kg {
        padding-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
### 欢迎回来！

这是一个为您量身打造的本地穿搭助手。

**您可以做什么？**
- **在左侧菜单** 选择功能
- **衣橱录入**: 上传您的新衣服
- **我的衣橱**: 浏览和管理已有的衣物
- **今日穿搭**: 根据天气和您的风格获取 AI 穿搭建议
- **个人设置**: 配置您的身材数据和 AI 设置

开始您的时尚之旅吧！
""")

# 显示一些简单的统计数据或欢迎图
# from utils.database import get_all_clothes
# clothes = get_all_clothes()
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.metric("当前衣橱单品", f"{len(clothes)} 件")
# with col2:
#     st.metric("今日天气", "请在'今日穿搭'中查看")
# with col3:
#     st.metric("系统状态", "本地运行中")
