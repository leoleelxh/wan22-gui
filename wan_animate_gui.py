#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wan2.2-Animate Gradio GUI
支持角色动画和替换的Web界面
"""

import os
import sys
import tempfile
import shutil
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Tuple
import gradio as gr

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入模型管理器
try:
    from model_manager import ModelManager
except ImportError:
    # 如果无法导入，创建一个简单的占位符
    class ModelManager:
        def __init__(self, base_dir="."):
            self.base_dir = base_dir
        def check_model_exists(self, model_name):
            return False, "Model manager not available"
        def download_model(self, model_name, progress_callback=None):
            return False, "Model manager not available"

class LanguageManager:
    """多语言管理器"""

    LANGUAGES = {
        'zh': '中文',
        'en': 'English'
    }

    TRANSLATIONS = {
        'zh': {
            'title': 'Wan2.2-Animate: 角色动画与替换',
            'subtitle': '使用Wan2.2-Animate模型进行角色动画生成和角色替换',
            'mode_label': '生成模式',
            'animation_mode': '动画模式',
            'replacement_mode': '替换模式',
            'video_input_label': '输入视频',
            'image_input_label': '角色图像',
            'resolution_label': '输出分辨率',
            'ckpt_path_label': '模型检查点路径',
            'process_btn': '开始预处理',
            'generate_btn': '生成视频',
            'clear_btn': '清空',
            'output_video_label': '生成的视频',
            'progress_label': '处理进度',
            'processing': '处理中...',
            'preprocessing_complete': '预处理完成',
            'generation_complete': '视频生成完成',
            'error_occurred': '发生错误',
            'invalid_inputs': '请上传视频和角色图像',
            'model_not_found': '未找到模型检查点，请检查路径',
            'language_label': '界面语言',
            'advanced_settings': '高级设置',
            'refert_num_label': '参考帧数量',
            'refert_num_info': '用于时序引导的帧数，推荐1或5',
            'use_relighting_label': '使用重新光照LoRA',
            'use_relighting_info': '仅在替换模式下可用',
            'animation_help': '动画模式：模型生成一个角色图像的视频，模仿输入视频中的人体动作',
            'replacement_help': '替换模式：模型将角色图像替换到输入视频中',
            'gpu_memory_warning': '注意：此操作需要大量GPU内存。24GB显存可运行（速度较慢），建议80GB+',
            'install_notice': '确保已安装所有依赖项和模型检查点',
            'model_download': '模型下载',
            'download_model_btn': '下载模型',
            'model_status': '模型状态',
            'model_found': '模型已就绪',
            'model_missing': '模型未找到',
            'downloading_model': '正在下载模型...',
            'download_complete': '模型下载完成',
            'download_failed': '模型下载失败',
            'auto_download_info': '系统将自动检测并下载所需模型',
            'disk_space_warning': '下载需要约30GB磁盘空间',
            'model_path_auto': '将自动设置为下载的模型路径'
        },
        'en': {
            'title': 'Wan2.2-Animate: Character Animation & Replacement',
            'subtitle': 'Generate character animations and replacements using Wan2.2-Animate model',
            'mode_label': 'Generation Mode',
            'animation_mode': 'Animation Mode',
            'replacement_mode': 'Replacement Mode',
            'video_input_label': 'Input Video',
            'image_input_label': 'Character Image',
            'resolution_label': 'Output Resolution',
            'ckpt_path_label': 'Model Checkpoint Path',
            'process_btn': 'Start Preprocessing',
            'generate_btn': 'Generate Video',
            'clear_btn': 'Clear',
            'output_video_label': 'Generated Video',
            'progress_label': 'Processing Progress',
            'processing': 'Processing...',
            'preprocessing_complete': 'Preprocessing completed',
            'generation_complete': 'Video generation completed',
            'error_occurred': 'An error occurred',
            'invalid_inputs': 'Please upload both video and character image',
            'model_not_found': 'Model checkpoint not found, please check the path',
            'language_label': 'Interface Language',
            'advanced_settings': 'Advanced Settings',
            'refert_num_label': 'Reference Frame Count',
            'refert_num_info': 'Number of frames for temporal guidance, recommended 1 or 5',
            'use_relighting_label': 'Use Relighting LoRA',
            'use_relighting_info': 'Only available in replacement mode',
            'animation_help': 'Animation Mode: Generate a video of the character image mimicking human motion in the input video',
            'replacement_help': 'Replacement Mode: Replace the character in the input video with the provided character image',
            'gpu_memory_warning': 'Note: This operation requires significant GPU memory. 24GB VRAM works (slower), 80GB+ recommended',
            'install_notice': 'Ensure all dependencies and model checkpoints are installed',
            'model_download': 'Model Download',
            'download_model_btn': 'Download Model',
            'model_status': 'Model Status',
            'model_found': 'Model Ready',
            'model_missing': 'Model Not Found',
            'downloading_model': 'Downloading model...',
            'download_complete': 'Model download completed',
            'download_failed': 'Model download failed',
            'auto_download_info': 'System will automatically detect and download required models',
            'disk_space_warning': 'Download requires approximately 30GB disk space',
            'model_path_auto': 'Will be automatically set to downloaded model path'
        }
    }

    @classmethod
    def get_text(cls, lang: str, key: str) -> str:
        return cls.TRANSLATIONS.get(lang, cls.TRANSLATIONS['en']).get(key, key)

class WanAnimateProcessor:
    """Wan2.2-Animate处理器"""

    def __init__(self):
        self.temp_dir = None
        self.processed_path = None

    def create_temp_dir(self) -> str:
        """创建临时目录"""
        if self.temp_dir is None:
            self.temp_dir = tempfile.mkdtemp(prefix="wan_animate_")
        return self.temp_dir

    def cleanup_temp_dir(self):
        """清理临时目录"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
            self.processed_path = None

    def preprocess(self, video_path: str, image_path: str, mode: str,
                  ckpt_path: str, resolution: str) -> Tuple[bool, str]:
        """预处理步骤"""
        try:
            temp_dir = self.create_temp_dir()
            self.processed_path = os.path.join(temp_dir, "process_results")

            # 解析分辨率
            width, height = map(int, resolution.split('x'))

            # 构建预处理命令
            cmd = [
                'python', './wan/modules/animate/preprocess/preprocess_data.py',
                '--ckpt_path', f'{ckpt_path}/process_checkpoint',
                '--video_path', video_path,
                '--refer_path', image_path,
                '--save_path', self.processed_path,
                '--resolution_area', str(width), str(height)
            ]

            if mode == 'animation':
                cmd.extend(['--retarget_flag', '--use_flux'])
            else:  # replacement
                cmd.extend([
                    '--iterations', '3',
                    '--k', '7',
                    '--w_len', '1',
                    '--h_len', '1',
                    '--replace_flag'
                ])

            # 执行预处理
            result = subprocess.run(cmd, capture_output=True, text=True, cwd='/root/Wan2.2')

            if result.returncode != 0:
                return False, f"Preprocessing failed: {result.stderr}"

            return True, "Preprocessing completed successfully"

        except Exception as e:
            return False, f"Preprocessing error: {str(e)}"

    def generate(self, mode: str, ckpt_path: str, refert_num: int,
                use_relighting: bool) -> Tuple[bool, str, Optional[str]]:
        """生成视频"""
        try:
            if not self.processed_path or not os.path.exists(self.processed_path):
                return False, "Please run preprocessing first", None

            # 输出文件路径
            output_path = os.path.join(self.temp_dir, "output_video.mp4")

            # 构建生成命令
            cmd = [
                'python', 'generate.py',
                '--task', 'animate-14B',
                '--ckpt_dir', ckpt_path,
                '--src_root_path', self.processed_path,
                '--refert_num', str(refert_num),
                '--offload_model', 'True',
                '--convert_model_dtype'
            ]

            if mode == 'replacement':
                cmd.append('--replace_flag')
                if use_relighting:
                    cmd.append('--use_relighting_lora')

            # 执行生成
            result = subprocess.run(cmd, capture_output=True, text=True, cwd='/root/Wan2.2')

            if result.returncode != 0:
                return False, f"Generation failed: {result.stderr}", None

            # 查找生成的视频文件
            for file in os.listdir('/root/Wan2.2'):
                if file.startswith('animate-14B_') and file.endswith('.mp4'):
                    generated_video = os.path.join('/root/Wan2.2', file)
                    # 复制到临时目录
                    shutil.copy2(generated_video, output_path)
                    # 删除原文件
                    os.remove(generated_video)
                    return True, "Video generation completed", output_path

            return False, "Generated video not found", None

        except Exception as e:
            return False, f"Generation error: {str(e)}", None

class WanAnimateGUI:
    """Wan2.2-Animate GUI主类"""

    def __init__(self):
        self.processor = WanAnimateProcessor()
        self.current_lang = 'zh'
        self.model_manager = ModelManager(".")
        self.auto_download_enabled = True

    def get_text(self, key: str) -> str:
        return LanguageManager.get_text(self.current_lang, key)

    def change_language(self, lang: str):
        """切换语言"""
        self.current_lang = lang
        return self.create_interface()

    def check_and_download_model(self, ckpt_path: str, progress=None) -> Tuple[bool, str, str]:
        """检查模型是否存在，如果不存在则尝试下载"""
        # 如果用户指定了自定义路径且存在，直接使用
        if ckpt_path and ckpt_path != "./Wan2.2-Animate-14B" and os.path.exists(ckpt_path):
            return True, ckpt_path, self.get_text('model_found')

        # 检查默认模型是否存在
        exists, msg = self.model_manager.check_model_exists("animate-14B")
        if exists:
            return True, msg, self.get_text('model_found')

        # 如果启用自动下载，尝试下载模型
        if self.auto_download_enabled:
            if progress:
                progress(0.1, self.get_text('downloading_model'))

            def download_progress(percent, message):
                if progress:
                    progress(0.1 + percent * 0.4, f"{self.get_text('downloading_model')} {percent*100:.1f}%")

            success, result_msg = self.model_manager.download_model("animate-14B", download_progress)

            if success:
                # 重新检查模型路径
                exists, model_path = self.model_manager.check_model_exists("animate-14B")
                if exists:
                    return True, model_path, self.get_text('download_complete')

            return False, "", f"{self.get_text('download_failed')}: {result_msg}"

        return False, "", self.get_text('model_missing')

    def validate_inputs(self, video, image, ckpt_path):
        """验证输入"""
        if video is None or image is None:
            return False, self.get_text('invalid_inputs')

        # 使用新的模型检查逻辑
        model_ok, _, msg = self.check_and_download_model(ckpt_path)
        if not model_ok:
            return False, msg

        return True, ""

    def process_and_generate(self, video, image, mode, resolution, ckpt_path,
                           refert_num, use_relighting, progress=gr.Progress()):
        """完整的处理和生成流程"""
        try:
            # 验证基本输入
            if video is None or image is None:
                return None, self.get_text('invalid_inputs')

            # 检查和下载模型
            progress(0.05, desc="Checking model...")
            model_ok, actual_ckpt_path, model_msg = self.check_and_download_model(ckpt_path, progress)

            if not model_ok:
                return None, model_msg

            # 使用实际的模型路径
            ckpt_path = actual_ckpt_path

            # 预处理
            progress(0.5, desc=self.get_text('processing'))
            success, msg = self.processor.preprocess(
                video, image, mode, ckpt_path, resolution
            )

            if not success:
                return None, f"{self.get_text('error_occurred')}: {msg}"

            progress(0.7, desc=self.get_text('preprocessing_complete'))

            # 生成视频
            progress(0.8, desc=self.get_text('processing'))
            success, msg, output_video = self.processor.generate(
                mode, ckpt_path, refert_num, use_relighting
            )

            if not success:
                return None, f"{self.get_text('error_occurred')}: {msg}"

            progress(1.0, desc=self.get_text('generation_complete'))
            return output_video, self.get_text('generation_complete')

        except Exception as e:
            return None, f"{self.get_text('error_occurred')}: {str(e)}"

    def download_model_only(self, progress=gr.Progress()):
        """仅下载模型"""
        try:
            progress(0.1, self.get_text('downloading_model'))

            def download_progress(percent, message):
                progress(0.1 + percent * 0.9, f"{self.get_text('downloading_model')} {percent*100:.1f}%")

            success, msg = self.model_manager.download_model("animate-14B", download_progress)

            if success:
                progress(1.0, self.get_text('download_complete'))
                return self.get_text('download_complete')
            else:
                return f"{self.get_text('download_failed')}: {msg}"

        except Exception as e:
            return f"{self.get_text('download_failed')}: {str(e)}"

    def check_model_status(self):
        """检查模型状态"""
        exists, msg = self.model_manager.check_model_exists("animate-14B")
        if exists:
            return f"✅ {self.get_text('model_found')}: {msg}"
        else:
            return f"❌ {self.get_text('model_missing')}: {msg}"

    def clear_all(self):
        """清空所有内容"""
        self.processor.cleanup_temp_dir()
        return None, None, None, ""

    def create_interface(self):
        """创建Gradio界面"""
        with gr.Blocks(
            title=self.get_text('title'),
            theme=gr.themes.Soft(),
            css="""
            .main-container { max-width: 1200px; margin: 0 auto; }
            .warning-box { background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 10px; margin: 10px 0; }
            .help-box { background-color: #e7f3ff; border: 1px solid #b3d9ff; border-radius: 5px; padding: 10px; margin: 10px 0; }
            """
        ) as demo:

            # 标题和说明
            gr.Markdown(f"# {self.get_text('title')}")
            gr.Markdown(f"*{self.get_text('subtitle')}*")

            # 警告信息
            with gr.Row():
                gr.HTML(f"""
                <div class="warning-box">
                    <strong>⚠️ {self.get_text('gpu_memory_warning')}</strong><br>
                    💡 {self.get_text('install_notice')}
                </div>
                """)

            with gr.Row():
                with gr.Column(scale=2):
                    # 语言选择
                    lang_dropdown = gr.Dropdown(
                        choices=list(LanguageManager.LANGUAGES.values()),
                        value=LanguageManager.LANGUAGES[self.current_lang],
                        label=self.get_text('language_label'),
                        interactive=True
                    )

                    # 模式选择
                    mode_radio = gr.Radio(
                        choices=[
                            (self.get_text('animation_mode'), 'animation'),
                            (self.get_text('replacement_mode'), 'replacement')
                        ],
                        value='animation',
                        label=self.get_text('mode_label')
                    )

                    # 模式说明
                    gr.HTML(f"""
                    <div class="help-box">
                        <strong>{self.get_text('animation_mode')}:</strong> {self.get_text('animation_help')}<br><br>
                        <strong>{self.get_text('replacement_mode')}:</strong> {self.get_text('replacement_help')}
                    </div>
                    """)

                    # 输入文件
                    with gr.Row():
                        video_input = gr.Video(
                            label=self.get_text('video_input_label'),
                            show_download_button=False
                        )
                        image_input = gr.Image(
                            label=self.get_text('image_input_label'),
                            type="filepath"
                        )

                    # 基本设置
                    with gr.Row():
                        resolution_dropdown = gr.Dropdown(
                            choices=['1280x720', '1920x1080', '720x1280', '1080x1920'],
                            value='1280x720',
                            label=self.get_text('resolution_label')
                        )

                        ckpt_path_textbox = gr.Textbox(
                            value='./Wan2.2-Animate-14B',
                            label=self.get_text('ckpt_path_label'),
                            placeholder='/path/to/Wan2.2-Animate-14B',
                            info=self.get_text('model_path_auto')
                        )

                    # 模型下载区域
                    with gr.Accordion(self.get_text('model_download'), open=False):
                        gr.HTML(f"""
                        <div class="help-box">
                            💾 {self.get_text('auto_download_info')}<br>
                            💿 {self.get_text('disk_space_warning')}
                        </div>
                        """)

                        model_status_text = gr.Textbox(
                            label=self.get_text('model_status'),
                            value=self.check_model_status(),
                            interactive=False,
                            lines=2
                        )

                        with gr.Row():
                            check_model_btn = gr.Button(
                                "🔍 Check Model",
                                variant="secondary",
                                scale=1
                            )
                            download_model_btn = gr.Button(
                                f"⬇️ {self.get_text('download_model_btn')}",
                                variant="primary",
                                scale=2
                            )

                    # 高级设置
                    with gr.Accordion(self.get_text('advanced_settings'), open=False):
                        refert_num_slider = gr.Slider(
                            minimum=1,
                            maximum=10,
                            value=1,
                            step=1,
                            label=self.get_text('refert_num_label'),
                            info=self.get_text('refert_num_info')
                        )

                        use_relighting_checkbox = gr.Checkbox(
                            label=self.get_text('use_relighting_label'),
                            info=self.get_text('use_relighting_info'),
                            value=False,
                            interactive=True
                        )

                    # 按钮
                    with gr.Row():
                        generate_btn = gr.Button(
                            self.get_text('generate_btn'),
                            variant="primary",
                            size="lg"
                        )
                        clear_btn = gr.Button(
                            self.get_text('clear_btn'),
                            variant="secondary"
                        )

                with gr.Column(scale=1):
                    # 输出
                    output_video = gr.Video(
                        label=self.get_text('output_video_label'),
                        show_download_button=True
                    )

                    # 状态信息
                    status_textbox = gr.Textbox(
                        label=self.get_text('progress_label'),
                        interactive=False,
                        lines=3
                    )

            # 事件绑定
            generate_btn.click(
                fn=self.process_and_generate,
                inputs=[
                    video_input, image_input, mode_radio, resolution_dropdown,
                    ckpt_path_textbox, refert_num_slider, use_relighting_checkbox
                ],
                outputs=[output_video, status_textbox],
                show_progress=True
            )

            clear_btn.click(
                fn=self.clear_all,
                outputs=[video_input, image_input, output_video, status_textbox]
            )

            # 模型管理事件
            check_model_btn.click(
                fn=self.check_model_status,
                outputs=[model_status_text]
            )

            download_model_btn.click(
                fn=self.download_model_only,
                outputs=[model_status_text],
                show_progress=True
            )

            # 语言切换 (暂时禁用，因为需要重新创建界面)
            # lang_dropdown.change(
            #     fn=lambda x: self.change_language('zh' if x == '中文' else 'en'),
            #     inputs=[lang_dropdown],
            #     outputs=[]
            # )

            # 模式切换时更新重新光照选项的可见性
            def update_relighting_visibility(mode):
                return gr.update(interactive=(mode == 'replacement'))

            mode_radio.change(
                fn=update_relighting_visibility,
                inputs=[mode_radio],
                outputs=[use_relighting_checkbox]
            )

        return demo

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Wan2.2-Animate Gradio GUI')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=7860, help='Port number')
    parser.add_argument('--lang', type=str, default='zh', choices=['zh', 'en'], help='Default language')
    parser.add_argument('--share', action='store_true', help='Enable Gradio sharing')

    args = parser.parse_args()

    # 检查是否在正确的目录中
    if not os.path.exists('./wan'):
        print("错误：请在Wan2.2项目根目录中运行此脚本")
        print("Error: Please run this script in the Wan2.2 project root directory")
        sys.exit(1)

    # 创建GUI
    gui = WanAnimateGUI()
    gui.current_lang = args.lang

    # 启动界面
    demo = gui.create_interface()
    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        inbrowser=True,
        show_error=True
    )

if __name__ == "__main__":
    main()