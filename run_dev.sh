#!/bin/bash

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🛠️ 正在启动开发模式..."
echo "应用启动后，您可以在浏览器中访问: http://localhost:8501"
echo "💡 提示: 修改代码后，直接在浏览器按 'R' 键或点击右上角 'Rerun' 即可看到变化。"

# 检查依赖
pip3 install -r requirements.txt -q

# 强制禁用统计收集
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 标准启动 (会调用默认浏览器，带有地址栏和开发者工具)
python3 -m streamlit run app.py
