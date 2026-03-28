# 👔 个人智能穿搭衣橱 (My Wardrobe)

这是一个专为 Mac 用户设计的本地化个人穿搭管理应用。它能够管理你的衣服，根据天气和你的风格，利用 AI 提供每日穿搭建议。

## ✨ 功能特点
*   **极简操作**: 专为 Mac 适配，脚本一键启动。
*   **本地数据**: 所有图片和数据存储在本地，保护隐私。
*   **AI 赋能**: 支持接入 DeepSeek / OpenAI，生成个性化穿搭文案和搭配建议。
*   **自动天气**: 自动获取当地天气，无需手动输入。

## 🚀 快速开始

### 1. 准备工作
确保你的 Mac 上安装了 Python 3。
打开终端，检查是否安装：
```bash
python3 --version
```

### 2. 启动应用
在终端中进入项目目录，然后运行：
```bash
./run_app.sh
```
或者手动运行：
```bash
pip3 install -r requirements.txt
streamlit run app.py
```

### 3. 配置 AI
应用启动后，浏览器会自动打开。
1.  进入左侧菜单的 **⚙️ 个人设置**。
2.  填写你的身高、体重、风格。
3.  **关键步骤**: 输入 API Key。
    *   推荐使用 **DeepSeek** (性价比极高) 或 **OpenAI**。
    *   DeepSeek Base URL: `https://api.deepseek.com`
    *   OpenAI Base URL: `https://api.openai.com/v1`
4.  保存设置。

### 4. 使用流程
1.  **录入**: 去 **👗 衣橱录入** 页面，上传你的衣服照片（建议白底或背景干净），填写分类。
2.  **查看**: 在 **👚 我的衣橱** 浏览已录入的单品。
3.  **穿搭**: 每天点击 **🪄 今日穿搭**，AI 会根据天气推荐一套搭配。

## 📁 数据存储
*   图片存储在 `assets/` 文件夹。
*   数据存储在 `data/wardrobe.db` (SQLite 数据库)。
*   如需备份，只需复制整个项目文件夹即可。

## 🛠️ 技术栈
*   Python + Streamlit
*   SQLite
*   OpenAI API Standard (兼容 DeepSeek, Moonshot 等)
