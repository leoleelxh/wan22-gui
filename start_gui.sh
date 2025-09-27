#!/bin/bash

# Wan2.2-Animate Gradio GUI启动脚本
# Wan2.2-Animate Gradio GUI Startup Script

echo "==================================="
echo "Wan2.2-Animate Gradio GUI"
echo "角色动画与替换工具"
echo "==================================="

# 检查conda环境
source /root/miniconda3/etc/profile.d/conda.sh

if ! conda info --envs | grep -q "wan"; then
    echo "❌ 错误：未找到wan conda环境"
    echo "❌ Error: wan conda environment not found"
    echo "请先创建并配置wan环境"
    echo "Please create and configure the wan environment first"
    exit 1
fi

# 激活wan环境
echo "🔧 激活wan环境..."
echo "🔧 Activating wan environment..."
conda activate wan

# 检查依赖
echo "🔍 检查依赖项..."
echo "🔍 Checking dependencies..."

python -c "
import sys
sys.path.append('.')
try:
    import gradio
    import wan
    print('✓ 所有依赖项已就绪')
    print('✓ All dependencies ready')
except ImportError as e:
    print('❌ 缺少依赖项:', e)
    print('❌ Missing dependency:', e)
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "请运行以下命令安装依赖项："
    echo "Please run the following commands to install dependencies:"
    echo "pip install gradio"
    echo "pip install -r requirements.txt"
    echo "pip install -r requirements_animate.txt"
    exit 1
fi

# 启动GUI
echo "🚀 启动Gradio界面..."
echo "🚀 Starting Gradio interface..."
python wan_animate_gui.py --host 0.0.0.0 --port 7860 --lang zh

echo "✅ GUI已停止运行"
echo "✅ GUI stopped running"