# Wan2.2-Animate Gradio GUI使用指南

## 简介 / Introduction

本项目为Wan2.2-Animate模型提供了一个友好的Gradio Web界面，支持中英文操作，让您可以轻松进行角色动画生成和角色替换。

This project provides a user-friendly Gradio Web interface for the Wan2.2-Animate model, supporting both Chinese and English, allowing you to easily generate character animations and character replacements.

## 功能特点 / Features

### 🎭 两种生成模式 / Two Generation Modes
- **动画模式 (Animation Mode)**: 让角色图像模仿输入视频中的人体动作
- **替换模式 (Replacement Mode)**: 将角色图像替换到输入视频中

### 🌍 多语言支持 / Multi-language Support
- 中文界面 (Chinese Interface)
- English Interface

### 🎛️ 高级设置 / Advanced Settings
- 可调节参考帧数量
- 重新光照LoRA支持（替换模式）
- 多种输出分辨率选择

## 系统要求 / System Requirements

### 硬件要求 / Hardware Requirements
- **GPU**: 建议80GB+显存 (Recommended 80GB+ VRAM)
- **CPU**: 现代多核处理器 (Modern multi-core processor)
- **内存**: 32GB+ RAM
- **存储**: 100GB+可用空间 (Available storage)

### 软件要求 / Software Requirements
- Linux系统 (Linux OS)
- CUDA 12.x
- Python 3.10
- Conda环境管理器

## 安装指南 / Installation Guide

### 1. 克隆仓库 / Clone Repository
```bash
git clone https://github.com/Wan-Video/Wan2.2.git
cd Wan2.2
```

### 2. 创建Conda环境 / Create Conda Environment
```bash
conda create -n wan python=3.10
conda activate wan
```

### 3. 安装依赖 / Install Dependencies
```bash
# 基础依赖 / Basic dependencies
pip install -r requirements.txt

# Animate特定依赖 / Animate-specific dependencies
pip install -r requirements_animate.txt

# Gradio界面 / Gradio interface
pip install gradio
```

### 4. 下载模型 / Download Models
```bash
# 使用huggingface-cli下载 / Download using huggingface-cli
pip install "huggingface_hub[cli]"
huggingface-cli download Wan-AI/Wan2.2-Animate-14B --local-dir ./Wan2.2-Animate-14B

# 或使用modelscope-cli / Or use modelscope-cli
pip install modelscope
modelscope download Wan-AI/Wan2.2-Animate-14B --local_dir ./Wan2.2-Animate-14B
```

## 使用方法 / Usage

### 启动GUI / Start GUI

#### 方法1：使用启动脚本 / Method 1: Use startup script
```bash
./start_gui.sh
```

#### 方法2：直接运行 / Method 2: Direct run
```bash
conda activate wan
python wan_animate_gui.py --host 0.0.0.0 --port 7860 --lang zh
```

### 命令行参数 / Command Line Arguments
- `--host`: 服务器地址 (Server host, default: 0.0.0.0)
- `--port`: 端口号 (Port number, default: 7860)
- `--lang`: 默认语言 (Default language, zh/en, default: zh)
- `--share`: 启用Gradio共享 (Enable Gradio sharing)

### 操作步骤 / Operation Steps

1. **打开浏览器 / Open Browser**
   - 访问 `http://localhost:7860`

2. **选择模式 / Select Mode**
   - 动画模式：生成角色动画
   - 替换模式：替换视频中的角色

3. **上传文件 / Upload Files**
   - 选择输入视频文件
   - 上传角色图像

4. **配置设置 / Configure Settings**
   - 设置输出分辨率
   - 指定模型检查点路径
   - 调整高级参数（可选）

5. **生成视频 / Generate Video**
   - 点击"生成视频"按钮
   - 等待处理完成
   - 下载生成的视频

## 界面功能说明 / Interface Features

### 基本设置 / Basic Settings
- **生成模式**: 选择动画或替换模式
- **输入视频**: 上传要处理的视频文件
- **角色图像**: 上传角色图像文件
- **输出分辨率**: 选择生成视频的分辨率
- **模型路径**: 指定Wan2.2-Animate-14B模型路径

### 高级设置 / Advanced Settings
- **参考帧数量**: 用于时序引导的帧数（推荐1或5）
- **重新光照LoRA**: 仅在替换模式下可用，改善光照效果

## 故障排除 / Troubleshooting

### 常见问题 / Common Issues

#### 1. 模型未找到 / Model Not Found
```
错误：未找到模型检查点
解决：确保已下载Wan2.2-Animate-14B模型并正确设置路径
```

#### 2. 内存不足 / Out of Memory
```
错误：CUDA out of memory
解决：
- 使用更高显存的GPU
- 降低输出分辨率
- 启用模型卸载选项
```

#### 3. 依赖包缺失 / Missing Dependencies
```
错误：ModuleNotFoundError
解决：
pip install -r requirements.txt
pip install -r requirements_animate.txt
pip install gradio librosa
```

#### 4. 预处理失败 / Preprocessing Failed
```
错误：预处理过程中出错
解决：
- 检查输入视频格式（支持mp4, mov, avi等）
- 确保图像格式正确（jpg, png等）
- 检查文件路径中是否包含特殊字符
```

### 性能优化 / Performance Optimization

#### GPU内存优化 / GPU Memory Optimization
- 使用较低的输出分辨率进行测试
- 启用模型卸载功能
- 关闭其他占用GPU的程序

#### 处理速度优化 / Processing Speed Optimization
- 使用SSD存储减少I/O延迟
- 确保CUDA和驱动程序是最新版本
- 使用专用GPU而非集成显卡

## 技术支持 / Technical Support

### 日志查看 / View Logs
GUI运行时会在终端显示详细的处理日志，有助于诊断问题。

### 联系方式 / Contact
- GitHub Issues: [Wan2.2 Issues](https://github.com/Wan-Video/Wan2.2/issues)
- 官方文档: [Wan2.2 Documentation](https://github.com/Wan-Video/Wan2.2)

## 注意事项 / Important Notes

⚠️ **资源消耗警告 / Resource Usage Warning**
- 此应用需要大量GPU内存，建议在配置充足的服务器上运行
- 首次运行可能需要下载额外的模型文件
- 生成过程可能需要几分钟到几十分钟，取决于视频长度和硬件配置

🎯 **最佳实践 / Best Practices**
- 建议先用短视频（5-10秒）进行测试
- 使用高质量的角色图像获得更好效果
- 在正式处理前确保有足够的存储空间

## 许可证 / License

本项目遵循Apache 2.0许可证。详见[LICENSE](LICENSE.txt)文件。

This project is licensed under the Apache 2.0 License. See [LICENSE](LICENSE.txt) for details.