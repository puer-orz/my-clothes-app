import streamlit as st
import os
from PIL import Image
from utils.database import get_all_clothes, delete_clothes, update_clothes
from utils.style import apply_global_style
from utils.navbar import render_navbar

st.set_page_config(page_title="我的衣橱", page_icon=None, layout="wide", initial_sidebar_state="collapsed")
apply_global_style()

# 颜色选项 (需要与录入页保持一致)
COLOR_OPTIONS_ALL = ["其他", "黑色", "白色", "灰色", "米色", "卡其色", "棕色", "红色", "粉色", "橙色", "黄色", "绿色", "蓝色", "紫色", "花色"]

@st.dialog("编辑衣物信息")
def edit_dialog(item):
    # 表单回显
    new_category = st.selectbox(
        "分类",
        ["上衣", "裤子", "裙子", "外套", "鞋子", "包袋", "配饰", "其他"],
        index=["上衣", "裤子", "裙子", "外套", "鞋子", "包袋", "配饰", "其他"].index(item['category']) if item['category'] in ["上衣", "裤子", "裙子", "外套", "鞋子", "包袋", "配饰", "其他"] else 0
    )
    
    # 颜色
    current_color = item.get('color')
    color_index = 0
    if current_color in COLOR_OPTIONS_ALL:
        color_index = COLOR_OPTIONS_ALL.index(current_color)
    else:
        # 尝试模糊匹配或默认
        pass
        
    new_color = st.selectbox(
        "颜色",
        COLOR_OPTIONS_ALL,
        index=color_index
    )
    
    # 季节 (string -> list)
    current_seasons = item['season'].split(',') if item['season'] else []
    # 过滤掉非标准季节 (防止报错)
    valid_seasons = ["春", "夏", "秋", "冬"]
    current_seasons = [s for s in current_seasons if s in valid_seasons]
    
    new_season = st.multiselect(
        "适用季节",
        valid_seasons,
        default=current_seasons
    )
    
    # 根据分类动态调整尺码选项
    size_options = ["XS", "S", "M", "L", "XL", "XXL", "均码", "其他"] # 默认衣服尺码
    if new_category == "鞋子":
        size_options = [str(i) for i in range(34, 47)] + ["其他"]
    elif new_category in ["包袋", "配饰", "其他"]:
        size_options = ["均码", "其他"]
    
    # 尝试回显旧尺码
    current_size = item['size']
    size_index = 0
    if current_size in size_options:
        size_index = size_options.index(current_size)
    else:
        # 如果旧尺码不在列表中（比如是旧的手填数据），默认选第一个或 "其他"
        # 这里我们尝试选 "其他"，或者如果是空值则选默认
        if "其他" in size_options:
            size_index = size_options.index("其他")
            
    new_size = st.selectbox("尺码", size_options, index=size_index)
    
    # 描述 (去除自动生成的后缀)
    desc_val = item['description']
    if desc_val == f"{item['category']} (未填写描述)":
        desc_val = ""
        
    new_description = st.text_area("描述", value=desc_val)
    
    if st.button("保存修改", type="primary"):
        # 构造保存数据
        final_desc = new_description if new_description else f"{new_category} (未填写描述)"
        season_str = ",".join(new_season)
        
        update_clothes(
            item['id'],
            new_category,
            final_desc,
            new_size,
            season_str,
            new_color
        )
        st.success("修改成功！")
        st.rerun()

# 顶部筛选和排序栏
col_filter1, col_filter2, col_filter3, col_sort = st.columns(4)

with col_filter1:
    filter_category = st.selectbox(
        "分类",
        ["全部", "上衣", "裤子", "裙子", "外套", "鞋子", "包袋", "配饰", "其他"],
        index=0
    )

with col_filter2:
    filter_season = st.selectbox(
        "季节",
        ["全部", "春", "夏", "秋", "冬"],
        index=0
    )

with col_filter3:
    # 颜色筛选
    COLOR_OPTIONS = ["全部", "其他", "黑色", "白色", "灰色", "米色", "卡其色", "棕色", "红色", "粉色", "橙色", "黄色", "绿色", "蓝色", "紫色", "花色"]
    filter_color = st.selectbox(
        "颜色",
        COLOR_OPTIONS,
        index=0
    )

with col_sort:
    sort_by = st.selectbox(
        "排序",
        ["添加时间 (新到旧)", "添加时间 (旧到新)", "分类"],
        index=0
    )

# 自定义优雅分割线
st.markdown('<hr style="border: 0; border-top: 1px solid #808080; opacity: 0.5; margin-top: 0px; margin-bottom: 12px;">', unsafe_allow_html=True)

# 获取数据
clothes = get_all_clothes()

# 转换 row 为 dict 以便排序
clothes_list = [dict(row) for row in clothes]

# 排序逻辑
if sort_by == "添加时间 (新到旧)":
    # 默认就是 created_at DESC
    pass
elif sort_by == "添加时间 (旧到新)":
    clothes_list.reverse()
elif sort_by == "分类":
    clothes_list.sort(key=lambda x: x['category'])

# 过滤逻辑
filtered_clothes = []
for item in clothes_list:
    match_category = True
    match_season = True
    match_color = True
    
    # 分类筛选：如果有 "全部" 或为空，则不过滤
    if filter_category and filter_category != "全部":
        if item['category'] != filter_category:
            match_category = False
            
    # 季节筛选
    if filter_season and filter_season != "全部":
        item_seasons = item['season'].split(',')
        if filter_season not in item_seasons:
            match_season = False
            
    # 颜色筛选
    if filter_color and filter_color != "全部":
        # 兼容旧数据没有 color 字段的情况
        item_color = item.get('color')
        if not item_color or item_color != filter_color:
            match_color = False
            
    if match_category and match_season and match_color:
        filtered_clothes.append(item)

# 图片处理函数：裁剪为固定比例 (3:4)
def crop_image_to_aspect_ratio(image_path, target_ratio=0.75):
    """
    将图片裁剪为目标宽高比 (width/height)，居中裁剪
    例如 3:4 = 0.75
    """
    try:
        img = Image.open(image_path)
        img_w, img_h = img.size
        current_ratio = img_w / img_h
        
        if current_ratio > target_ratio:
            # 图片太宽，需要裁剪两边
            new_w = int(img_h * target_ratio)
            left = (img_w - new_w) // 2
            img = img.crop((left, 0, left + new_w, img_h))
        elif current_ratio < target_ratio:
            # 图片太高，需要裁剪上下
            new_h = int(img_w / target_ratio)
            top = (img_h - new_h) // 2
            img = img.crop((0, top, img_w, top + new_h))
            
        return img
    except Exception as e:
        return None

if not filtered_clothes:
    st.info("衣橱里还没有符合条件的衣服，快去录入吧！")
else:
    st.caption(f"共找到 {len(filtered_clothes)} 件单品")
    
    # CSS Grid 样式优化
    # 我们使用 columns，但为了对齐，我们需要确保每张图片的高度一致。
    # Streamlit 的 st.image 如果 use_container_width=True，高度会随宽度变化。
    # 为了视觉整齐，我们已经在 Python 层面对图片进行了裁剪，使其宽高比一致。
    
    # 宽屏适配：一行 8 列
    cols = st.columns(8)
    for idx, item in enumerate(filtered_clothes):
        col = cols[idx % 8]
        with col:
            img_path = os.path.join(os.getcwd(), item['image_path'])
            
            if os.path.exists(img_path):
                # 实时裁剪并显示
                cropped_img = crop_image_to_aspect_ratio(img_path)
                if cropped_img:
                    st.image(cropped_img, use_container_width=True)
                else:
                    st.error("图片损坏")
            else:
                st.error("图片丢失")
                
            # 操作按钮区域
            col_edit, col_del = st.columns(2)
            with col_edit:
                if st.button("", key=f"edit_{item['id']}", use_container_width=True, icon=":material/mode_edit:", help="编辑"):
                    edit_dialog(item)
            
            with col_del:
                if st.button("", key=f"del_{item['id']}", use_container_width=True, icon=":material/delete:", help="删除"):
                    delete_clothes(item['id'])
                    if os.path.exists(img_path):
                        try:
                            os.remove(img_path)
                        except:
                            pass
                    st.rerun()            
render_navbar()
