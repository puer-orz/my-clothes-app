import streamlit as st

def render_navbar():
    """
    渲染左侧悬浮导航栏 (Persistent JS Injection 版)
    
    原理：
    为了避免页面切换时侧边栏闪烁，我们使用 streamlit.components.v1.html 执行一段 JavaScript。
    这段 JS 会检查 window.parent.document (Streamlit 主页面 DOM) 中是否已经存在我们的导航栏。
    如果不存在，则动态创建并插入到 body 中。
    如果存在，则仅更新高亮状态。
    
    改进：
    为了解决 SPA 模式下手动 pushState 不触发 Streamlit 页面更新的问题，
    我们采取【混合策略】：
    1. 在页面底部渲染隐藏的原生 st.page_link (Streamlit 1.31+ 支持)。
    2. 当点击自定义侧边栏时，JS 拦截点击，并在 DOM 中找到对应的原生链接并模拟点击 (link.click())。
    这样既保留了自定义 UI，又利用了 Streamlit 原生的无刷新路由机制。
    """
    
    # 隐藏原生链接的 CSS
    st.markdown(
        """
        <style>
        /* 隐藏所有的 st.page_link 渲染结果 - 修正选择器以兼容不同标签 */
        [data-testid="stPageLink-NavLink"] {
            display: none !important;
        }
        
        /* 额外保险：隐藏包含这些链接的容器 */
        /* 注意：这可能会误伤其他内容，所以只针对特定结构 */
        div[data-testid="stElementContainer"]:has(a[data-testid="stPageLink-NavLink"]) {
            display: none !important;
        }
        
        /* 也可以通过父容器隐藏，这里为了保险直接隐藏元素 */
        .hidden-nav-links {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # 渲染隐藏的原生链接 (用于 JS 模拟点击)
    # 注意：page 参数必须是相对于主脚本的文件路径
    with st.container():
        st.page_link("pages/2_我的衣橱.py", label="我的衣橱", icon="👗")
        st.page_link("pages/1_衣橱录入.py", label="衣橱录入", icon="➕")
        st.page_link("pages/3_今日穿搭.py", label="今日穿搭", icon="✨")
        st.page_link("pages/4_个人设置.py", label="个人设置", icon="⚙️")
    
    import streamlit.components.v1 as components

    # SVG 图标定义
    
    # --- 1. 衣橱图标 (Outline/Open) ---
    wardrobe_default = """<svg class="icon-default" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="1" /><path d="M12 3v18" /><circle cx="10" cy="12" r="0.5" fill="currentColor" stroke="none" /><circle cx="14" cy="12" r="0.5" fill="currentColor" stroke="none" /></svg>"""
    
    wardrobe_hover = """<svg class="icon-hover" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="1" /><path d="M8 3v18" /><path d="M16 3v18" /></svg>"""
    
    # --- 2. 录入图标 (Outline/Filled) ---
    add_default = """<svg class="icon-default" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>"""
    
    add_hover = """<svg class="icon-hover" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>"""
    
    # --- 3. 穿搭图标 (Morphing T-Shirt -> Long Sleeve) ---
    outfit_morph = """<svg class="icon-morph" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path class="outfit-body" d="" /> <!-- d 属性由 CSS 定义 --><path class="outfit-collar" d="M6 4 Q12 8 18 4" /></svg>"""
    
    # --- 其他图标 ---
    icons = {
        "settings": """<svg class="icon-settings" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.1a2 2 0 0 1-1-1.72v-.51a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>"""
    }
    
    # 导航配置
    # href 需要与 st.page_link 生成的 href 部分匹配
    # st.page_link 生成的 href 通常是 "我的衣橱", "衣橱录入" 等 (Streamlit 会处理路径)
    nav_items = [
        {"id": "wardrobe", "label": "衣橱", "href": "我的衣橱", "custom_html": f'<span class="nav-icon swap-icon">{wardrobe_default}{wardrobe_hover}</span>'},
        {"id": "add", "label": "录入", "icon": "", "href": "衣橱录入", "custom_html": f'<span class="nav-icon swap-icon">{add_default}{add_hover}</span>'},
        {"id": "magic", "label": "穿搭", "icon": "", "href": "今日穿搭", "custom_html": f'<span class="nav-icon">{outfit_morph}</span>'},
        {"id": "settings", "label": "设置", "icon": icons["settings"], "href": "个人设置"},
    ]
    
    # JS: 拦截点击 -> 查找对应的隐藏原生链接 -> 模拟点击
    onclick_js = """
    event.preventDefault(); 
    const targetHref = this.getAttribute('data-href');
    const anchors = window.parent.document.querySelectorAll('a');
    let found = false;
    for (let i = 0; i < anchors.length; i++) {
        // Streamlit 链接通常以页面名结尾，或者包含页面名
        // 解码 href 以处理中文字符
        const anchorHref = decodeURIComponent(anchors[i].href);
        if (anchorHref.endsWith(targetHref) || anchorHref.includes('/' + targetHref)) {
            anchors[i].click();
            found = true;
            break;
        }
    }
    // 如果没找到（兜底），则直接跳转（可能会刷新）
    if (!found) {
        window.parent.location.href = targetHref;
    }
    """
    # 压缩 onclick 代码
    onclick_js_min = onclick_js.replace('\n', ' ').replace('    ', '')
    
    nav_links_html = ""
    for item in nav_items:
        if "custom_html" in item:
            icon_html = item["custom_html"]
        else:
            icon_html = f'<span class="nav-icon">{item["icon"]}</span>'
            
        nav_links_html += f"""
<a href="{item['href']}" target="_self" class="nav-link" data-href="{item['href']}" onclick="{onclick_js_min}">
{icon_html}
<span class="nav-text">{item['label']}</span>
</a>
"""

    full_html = f"""
<div class="floating-sidebar-nav">
{nav_links_html}
</div>
"""
    
    full_html_minified = full_html.replace('\n', '')

    # 2. 构建 CSS
    css_content = """
/* 导航栏容器 */
.floating-sidebar-nav {
    position: fixed !important;
    top: 50% !important;
    left: 20px !important;
    bottom: auto !important;
    transform: translateY(-50%) !important;
    z-index: 999999 !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 24px !important;
    background: rgba(28, 31, 46, 0.75);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border-radius: 16px !important;
    padding: 24px 12px !important;
    width: auto !important;
    min-width: 60px !important;
    min-height: 200px !important;
}

/* 链接项 */
.nav-link {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-decoration: none !important;
    color: #a0a0a0 !important;
    transition: all 0.3s ease !important;
    background: transparent !important;
    border: none !important;
    cursor: pointer !important;
    width: 100% !important;
    padding: 8px 0 !important;
    border-radius: 8px !important;
}

.nav-link:hover, .nav-link.active {
    transform: scale(1.1) !important;
    color: #ffffff !important;
    background: rgba(255, 255, 255, 0.05) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}

/* 图标容器 */
.nav-icon {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 24px !important;
    height: 24px !important;
    margin-bottom: 6px !important;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}

/* SVG 图标样式 */
.nav-icon svg {
    width: 24px !important;
    height: 24px !important;
    stroke-width: 2px !important;
}

/* --- 1. 通用图标切换逻辑 --- */
.swap-icon .icon-hover { display: none; }
.swap-icon .icon-default { display: block; }

.nav-link:hover .swap-icon .icon-default, .nav-link.active .swap-icon .icon-default { display: none; }
.nav-link:hover .swap-icon .icon-hover, .nav-link.active .swap-icon .icon-hover { display: block; }

/* --- 2. 设置图标旋转动画 --- */
@keyframes spin-custom {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(120deg); }
}
.nav-link:hover .icon-settings, .nav-link.active .icon-settings {
    animation: spin-custom 0.6s ease-in-out; 
    animation-fill-mode: forwards;
}

/* --- 3. 穿搭图标变形动画 (CSS Path Morphing) --- */
.outfit-body {
    d: path("M6 4 L2 8 L6 10 L6 20 L18 20 L18 10 L22 8 L18 4 Z");
    transition: d 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-link:hover .outfit-body, .nav-link.active .outfit-body {
    d: path("M6 4 L2 14 L6 16 L6 20 L18 20 L18 16 L22 14 L18 4 Z");
}

/* 文字 */
.nav-text {
    font-size: 10px !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    opacity: 0.9;
}
"""
    # 压缩 CSS
    css_content_minified = css_content.replace('\n', ' ')

    # 3. 构建 JS
    # 使用 Python 字符串替换，避免 JS 和 Python 格式化冲突
    js_template = """
    <script>
        (function() {{
            const navId = 'persistent-floating-nav-container';
            const styleId = 'persistent-floating-nav-style';
            
            try {{
                const doc = window.parent.document;
                
                // 1. 注入 CSS (如果是首次)
                if (!doc.getElementById(styleId)) {{
                    const style = doc.createElement('style');
                    style.id = styleId;
                    style.innerHTML = `{css_content}`;
                    doc.head.appendChild(style);
                }}
                
                // 2. 注入 HTML (如果是首次)
                let nav = doc.getElementById(navId);
                if (!nav) {{
                    nav = doc.createElement('div');
                    nav.id = navId;
                    nav.innerHTML = `{html_content}`;
                    doc.body.appendChild(nav);
                }}
                
                // 3. 高亮当前页面
                const currentPath = decodeURIComponent(window.parent.location.pathname);
                
                const links = nav.querySelectorAll('.nav-link');
                links.forEach(link => {{
                    const href = link.getAttribute('data-href');
                    
                    if (currentPath.includes(href)) {{
                        link.classList.add('active');
                    }} else {{
                        link.classList.remove('active');
                    }}
                }});
                
            }} catch (e) {{
                console.error("Navbar injection failed:", e);
            }}
        }})();
    </script>
    """
    
    # 替换变量
    js_script = js_template.format(
        css_content=css_content_minified,
        html_content=full_html_minified
    )
    
    # 执行 JS
    components.html(js_script, height=0, width=0)
