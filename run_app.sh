#!/bin/bash

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "👔 正在启动个人穿搭衣橱..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3。请先安装 Python。"
    exit 1
fi

# 创建虚拟环境 (可选，这里为了极简直接用系统 pip 或者用户已有的环境，
# 但为了不污染环境，建议检查一下 venv。为了极简，我们直接 pip install)
# 如果用户想用 venv，可以手动创建。这里为了“脚本式运行”，直接 install

echo "📦 正在安装/更新依赖..."
pip3 install -r requirements.txt -q -i https://pypi.tuna.tsinghua.edu.cn/simple

if [ $? -ne 0 ]; then
    echo "⚠️ 依赖安装可能出现问题 (尝试切换回官方源)..."
    pip3 install -r requirements.txt -q
fi

echo "🚀 启动 Streamlit 服务..."
# 强制禁用统计收集
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 在后台启动 Streamlit，并记录 PID
python3 -m streamlit run app.py --server.headless true > /dev/null 2>&1 &
STREAMLIT_PID=$!

# 等待服务启动
echo "⏳ 等待服务就绪..."
sleep 3

# 尝试以“应用模式”打开 (无地址栏，独立窗口)
URL="http://localhost:8501"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
EDGE="/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"

if [ -f "$CHROME" ]; then
    "$CHROME" --app="$URL"
elif [ -f "$EDGE" ]; then
    "$EDGE" --app="$URL"
else
    # 如果没有 Chrome/Edge，使用默认浏览器打开
    open "$URL"
fi

# 等待 Streamlit 进程结束 (保持脚本运行)
wait $STREAMLIT_PID
