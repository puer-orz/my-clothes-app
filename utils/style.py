import streamlit as st

def apply_global_style():
    """
    应用全局 CSS 样式
    主要负责隐藏侧边栏和调整主内容区域
    """
    st.markdown("""
    <style>
        /* 1. 强力隐藏原生侧边栏和折叠按钮 */
        [data-testid="stSidebar"], 
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        section[data-testid="stSidebar"] {
            display: none !important;
            visibility: hidden !important;
        }
        
        /* 2. 隐藏顶部 Header 的干扰元素 */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
            pointer-events: none !important;
            /* 尝试把 header 高度设为 0，防止占位 */
            height: 0 !important;
        }
        header[data-testid="stHeader"] > div {
            display: none !important;
        }
        
        /* 3. 调整主内容区域 - 更加智能的响应式布局 */
        /* 使用更高权重的选择器组合 */
        .appview-container .main .block-container,
        [data-testid="stAppViewContainer"] .main .block-container,
        section[data-testid="stMain"] .block-container {
            /* 网页级设计：放宽最大宽度，利用大屏幕空间 */
            max-width: 100% !important; /* 使用百分比，确保不超过视口 */
            width: calc(100% - 140px) !important; /* 减去左侧导航栏的宽度+留白 */
            
            /* 关键：使用 margin-left 代替 padding-left，更稳定 */
            margin-left: 120px !important;
            margin-right: 20px !important; /* 右侧留一点余地 */
            
            /* 内边距微调，增加呼吸感 */
            padding-left: 0 !important; /* padding 交给内部元素或已由 margin 处理 */
            padding-right: 0 !important;
            padding-bottom: 5rem !important;
            
            /* 【关键修改】移除顶部留空，不需要吸顶栏 */
            padding-top: 4rem !important;
            
            /* 防止出现横向滚动条 */
            overflow-x: hidden !important;
            box-sizing: border-box !important;
        }
        
        /* 4. 隐藏不需要的元素 */
        #MainMenu, footer {
            visibility: hidden !important;
        }
        
        /* 针对较窄屏幕的优化 (比如平板或窄窗口) */
        @media (max-width: 1000px) {
             .appview-container .main .block-container,
             [data-testid="stAppViewContainer"] .main .block-container {
                margin-left: 90px !important; /* 稍微缩减左边距 */
                padding-right: 1rem !important;
             }
        }
        
        /* 针对极窄屏幕 (手机) */
        @media (max-width: 768px) {
             .appview-container .main .block-container,
             [data-testid="stAppViewContainer"] .main .block-container {
                margin-left: auto !important; /* 恢复居中 */
                margin-right: auto !important;
                padding-left: 1rem !important;
                padding-bottom: 120px !important; /* 底部留空 */
                padding-top: 5rem !important; /* 增加顶部空间，为筛选栏留位 */
             }
        }
        
        /* 5. 筛选栏样式 (用于 pages/2_我的衣橱.py) */
        /* 回归正常流布局，仅做美化 */
        
        /* 针对包含 Selectbox 的列，添加一点样式让其看起来整齐 */
        /* 这里我们不特定定位，而是通用的 Selectbox 美化 */
        
        [data-testid="stSelectbox"] label {
            font-size: 12px !important;
            color: var(--text-color) !important;
            opacity: 0.8;
            margin-bottom: 0px !important;
            font-weight: 500 !important;
        }
        
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            font-size: 13px !important;
            min-height: 38px !important;
            height: 38px !important;
            border-radius: 8px !important;
            
            /* 输入框背景色：使用次级背景色 */
            background-color: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
            
            /* 文字颜色 */
            color: var(--text-color) !important;
            
            padding-left: 10px !important;
            padding-right: 10px !important;
            
            /* 垂直居中 */
            display: flex !important;
            align-items: center !important;
        }
        
        /* 鼠标悬停效果 */
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {
            border-color: var(--primary-color) !important;
            opacity: 0.9;
        }
        
        /* 汉化 File Uploader - 强力覆盖版 */
        
        /* 1. 隐藏 "Drag and drop files here" */
        /* 通常在 dropzone 的第一个 div 的 span 中 */
        [data-testid="stFileUploaderDropzone"] > div > div > span {
            font-size: 0 !important;
        }
        
        [data-testid="stFileUploaderDropzone"] > div > div > span::after {
            content: "拖拽文件至此";
            font-size: 1rem !important;
            visibility: visible !important;
            display: block !important;
        }
        
        /* 2. 隐藏 "Limit 200MB..." */
        /* 通常在 small 标签中 */
        [data-testid="stFileUploaderDropzone"] small {
            font-size: 0 !important;
        }
        
        [data-testid="stFileUploaderDropzone"] small::after {
            content: "单个文件限制 200MB • JPG, JPEG, PNG, WEBP";
            font-size: 0.8rem !important;
            visibility: visible !important;
            display: block !important;
        }
        
        /* 3. 汉化 "Browse files" 按钮 */
        [data-testid="stFileUploaderDropzone"] button {
            font-size: 0 !important;
        }
        
        [data-testid="stFileUploaderDropzone"] button::after {
            content: "浏览文件";
            font-size: 1rem !important;
            visibility: visible !important;
            display: block !important;
        }
        
        /* === 全局美化 === */
        
        /* 图片圆角与阴影 */
        [data-testid="stImage"] img {
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        [data-testid="stImage"] img:hover {
            transform: scale(1.02);
        }
        
        /* 提示卡片美化 */
        [data-testid="stAlert"] {
            border-radius: 10px;
            border: none;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        /* 表单区域美化 */
        [data-testid="stForm"] {
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 16px;
            padding: 2rem;
            background-color: rgba(255, 255, 255, 0.02);
        }
    </style>
    """, unsafe_allow_html=True)
