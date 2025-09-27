#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wan2.2-Animate Gradio GUI 演示脚本
Demo script for Wan2.2-Animate Gradio GUI
"""

import os
import sys

# 确保在正确的目录中运行
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("="*50)
print("🎭 Wan2.2-Animate Gradio GUI 演示")
print("🎭 Wan2.2-Animate Gradio GUI Demo")
print("="*50)

# 检查依赖
print("🔍 检查依赖项...")
print("🔍 Checking dependencies...")

try:
    import gradio as gr
    import wan
    from wan_animate_gui import WanAnimateGUI
    print("✅ 所有依赖项就绪")
    print("✅ All dependencies ready")
except ImportError as e:
    print(f"❌ 缺少依赖项: {e}")
    print(f"❌ Missing dependency: {e}")
    print("请运行以下命令安装:")
    print("Please run the following to install:")
    print("pip install gradio -r requirements.txt -r requirements_animate.txt")
    sys.exit(1)

# 检查模型目录（可选）
model_paths = [
    "./Wan2.2-Animate-14B",
    "/models/Wan2.2-Animate-14B",
    "../models/Wan2.2-Animate-14B"
]

print("\n📁 检查模型目录...")
print("📁 Checking model directories...")

found_model = False
for path in model_paths:
    if os.path.exists(path):
        print(f"✅ 找到模型: {path}")
        print(f"✅ Found model: {path}")
        found_model = True
        break

if not found_model:
    print("⚠️  未找到预训练模型目录")
    print("⚠️  No pre-trained model directory found")
    print("请下载 Wan2.2-Animate-14B 模型")
    print("Please download Wan2.2-Animate-14B model")
    print("提示: 您仍可以启动GUI并手动指定模型路径")
    print("Tip: You can still start the GUI and specify model path manually")

# 创建GUI实例
print("\n🚀 启动Gradio界面...")
print("🚀 Starting Gradio interface...")

try:
    # 创建GUI
    gui = WanAnimateGUI()
    demo = gui.create_interface()

    print("\n" + "="*50)
    print("🎉 GUI启动成功！")
    print("🎉 GUI started successfully!")
    print("="*50)
    print("📱 访问地址: http://localhost:7860")
    print("📱 Access URL: http://localhost:7860")
    print("🌍 支持语言: 中文 / English")
    print("🌍 Supported languages: Chinese / English")
    print("⚡ 功能: 角色动画生成 / 角色替换")
    print("⚡ Features: Character Animation / Character Replacement")
    print("="*50)
    print("💡 使用提示:")
    print("💡 Usage Tips:")
    print("   1. 上传视频和角色图像")
    print("   1. Upload video and character image")
    print("   2. 选择生成模式（动画/替换）")
    print("   2. Select generation mode (Animation/Replacement)")
    print("   3. 点击生成视频按钮")
    print("   3. Click generate video button")
    print("="*50)
    print("按 Ctrl+C 停止服务器")
    print("Press Ctrl+C to stop the server")
    print("="*50)

    # 启动服务器
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
        show_error=True,
        show_tips=False,
        quiet=False
    )

except KeyboardInterrupt:
    print("\n🛑 用户中断，正在停止服务器...")
    print("🛑 User interrupted, stopping server...")
except Exception as e:
    print(f"\n❌ 启动失败: {e}")
    print(f"❌ Startup failed: {e}")
    import traceback
    traceback.print_exc()
finally:
    print("\n👋 GUI已停止")
    print("👋 GUI stopped")