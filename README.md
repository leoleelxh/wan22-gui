# Wan2.2-Animate Gradio GUI

[English](#english) | [中文](#中文)

## English

### Overview

A user-friendly Gradio web interface for Wan2.2-Animate model, supporting character animation generation and character replacement with bilingual support (Chinese/English).

### Features

- 🎭 **Two Generation Modes**
  - Animation Mode: Generate character animations mimicking human motions
  - Replacement Mode: Replace characters in videos with provided images
- 🌍 **Bilingual Support**: Chinese and English interfaces
- 🎛️ **Advanced Settings**: Resolution selection, reference frame count, relighting LoRA
- 🚀 **Easy to Use**: Web-based interface with drag-and-drop functionality
- ⚡ **Real-time Progress**: Live progress tracking and error handling
- 📦 **Auto Model Download**: Automatic Wan2.2-Animate-14B model download
- 💾 **Smart Model Management**: Model status checking and validation

### Quick Start

1. **Install Dependencies**
   ```bash
   # In your Wan2.2 project directory
   conda activate wan
   pip install gradio huggingface_hub[cli]
   pip install -r requirements.txt
   pip install -r requirements_animate.txt
   ```

2. **Download Model (Optional - Auto Download Available)**
   ```bash
   # Manual download (optional - GUI can auto-download)
   huggingface-cli download Wan-AI/Wan2.2-Animate-14B --local-dir ./Wan2.2-Animate-14B
   ```

3. **Start GUI**
   ```bash
   python wan_animate_gui.py --host 0.0.0.0 --port 7860 --lang en
   ```

4. **Access Interface**
   - Open browser and go to `http://localhost:7860`

### System Requirements

- **GPU**: 24GB+ VRAM (RTX 4090 works, slower) or 80GB+ VRAM (recommended for optimal performance)
- **CPU**: Multi-core processor
- **RAM**: 32GB+
- **Storage**: 100GB+ available space (30GB for model download)
- **OS**: Linux (Ubuntu 20.04+ recommended)

### Files

- `wan_animate_gui.py` - Main GUI application with auto-download
- `model_manager.py` - Automatic model download and management
- `start_gui.sh` - Startup script
- `demo_gui.py` - Demo and test script
- `GUI_README.md` - Detailed usage guide
- `WAN_ANIMATE_GUI_SUMMARY.md` - Project summary

### Usage

1. Select generation mode (Animation/Replacement)
2. Upload input video and character image
3. Configure output settings
4. Click "Generate Video" button
5. Download the generated result

### License

This project follows the Apache 2.0 License, same as the original Wan2.2 project.

---

## 中文

### 概述

为Wan2.2-Animate模型提供的用户友好的Gradio Web界面，支持角色动画生成和角色替换，提供中英文双语支持。

### 功能特点

- 🎭 **两种生成模式**
  - 动画模式：生成模仿人体动作的角色动画
  - 替换模式：将提供的角色图像替换到视频中
- 🌍 **双语支持**：中文和英文界面
- 🎛️ **高级设置**：分辨率选择、参考帧数量、重新光照LoRA
- 🚀 **易于使用**：基于Web的界面，支持拖拽功能
- ⚡ **实时进度**：实时进度追踪和错误处理

### 快速开始

1. **安装依赖**
   ```bash
   # 在您的Wan2.2项目目录中
   conda activate wan
   pip install gradio
   pip install -r requirements.txt
   pip install -r requirements_animate.txt
   ```

2. **下载模型**
   ```bash
   huggingface-cli download Wan-AI/Wan2.2-Animate-14B --local-dir ./Wan2.2-Animate-14B
   ```

3. **启动GUI**
   ```bash
   python wan_animate_gui.py --host 0.0.0.0 --port 7860 --lang zh
   ```

4. **访问界面**
   - 打开浏览器访问 `http://localhost:7860`

### 系统要求

- **GPU**：24GB+显存 (RTX 4090可用，速度较慢) 或 80GB+显存 (推荐最佳性能)
- **CPU**：多核处理器
- **内存**：32GB+
- **存储**：100GB+可用空间 (模型下载需要30GB)
- **操作系统**：Linux (推荐Ubuntu 20.04+)

### 文件说明

- `wan_animate_gui.py` - 主GUI应用（支持自动下载）
- `model_manager.py` - 自动模型下载和管理
- `start_gui.sh` - 启动脚本
- `demo_gui.py` - 演示和测试脚本
- `GUI_README.md` - 详细使用指南
- `WAN_ANIMATE_GUI_SUMMARY.md` - 项目总结

### 使用方法

1. 选择生成模式（动画/替换）
2. 上传输入视频和角色图像
3. 配置输出设置
4. 点击"生成视频"按钮
5. 下载生成的结果

### 许可证

本项目遵循Apache 2.0许可证，与原Wan2.2项目相同。

---

## Related Projects

- [Wan2.2](https://github.com/Wan-Video/Wan2.2) - Original Wan2.2 project
- [Wan2.2-Animate](https://humanaigc.github.io/wan-animate) - Character animation and replacement

## Support

For issues and questions, please refer to:
- [Wan2.2 GitHub Issues](https://github.com/Wan-Video/Wan2.2/issues)
- [Wan2.2 Documentation](https://github.com/Wan-Video/Wan2.2)

## Citation

If you use this GUI in your research, please cite the original Wan2.2 paper:

```bibtex
@article{wan2025,
    title={Wan: Open and Advanced Large-Scale Video Generative Models},
    author={Team Wan and ...},
    journal={arXiv preprint arXiv:2503.20314},
    year={2025}
}
```