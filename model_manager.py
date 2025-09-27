#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wan2.2-Animate Model Manager
自动下载和管理Wan2.2-Animate模型
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Tuple, Optional
import logging

class ModelManager:
    """模型管理器 - 负责自动下载和验证模型"""

    # 模型配置
    MODEL_CONFIG = {
        "animate-14B": {
            "repo_id": "Wan-AI/Wan2.2-Animate-14B",
            "local_dir": "Wan2.2-Animate-14B",
            "required_files": [
                "config.json",
                "model_index.json",
                "diffusion_pytorch_model.safetensors",
                "process_checkpoint"
            ],
            "size_gb": 28,  # 大约28GB
            "description": "Wan2.2-Animate 14B model for character animation and replacement"
        }
    }

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("ModelManager")
        logger.setLevel(logging.INFO)

        # 避免重复添加处理器
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def check_model_exists(self, model_name: str) -> Tuple[bool, str]:
        """
        检查模型是否存在并完整

        Args:
            model_name: 模型名称

        Returns:
            (是否存在, 模型路径或错误信息)
        """
        if model_name not in self.MODEL_CONFIG:
            return False, f"Unsupported model: {model_name}"

        config = self.MODEL_CONFIG[model_name]
        model_path = self.base_dir / config["local_dir"]

        if not model_path.exists():
            return False, f"Model directory not found: {model_path}"

        # 检查必要文件
        missing_files = []
        for required_file in config["required_files"]:
            file_path = model_path / required_file
            if not file_path.exists():
                missing_files.append(required_file)

        if missing_files:
            return False, f"Missing files: {', '.join(missing_files)}"

        return True, str(model_path)

    def get_available_disk_space(self) -> float:
        """获取可用磁盘空间 (GB)"""
        try:
            stat = shutil.disk_usage(self.base_dir)
            return stat.free / (1024**3)  # 转换为GB
        except Exception as e:
            self.logger.warning(f"无法获取磁盘空间信息: {e}")
            return float('inf')  # 假设有足够空间

    def check_system_requirements(self, model_name: str) -> Tuple[bool, str]:
        """
        检查系统要求

        Args:
            model_name: 模型名称

        Returns:
            (是否满足要求, 检查结果信息)
        """
        if model_name not in self.MODEL_CONFIG:
            return False, f"Unknown model: {model_name}"

        config = self.MODEL_CONFIG[model_name]
        issues = []

        # 检查磁盘空间
        available_space = self.get_available_disk_space()
        required_space = config["size_gb"] * 1.2  # 预留20%空间

        if available_space < required_space:
            issues.append(f"Insufficient disk space: {available_space:.1f}GB available, {required_space:.1f}GB required")

        # 检查是否安装了必要的工具
        try:
            subprocess.run(["huggingface-cli", "--version"],
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            issues.append("huggingface-cli not found. Install with: pip install 'huggingface_hub[cli]'")

        if issues:
            return False, "\n".join(issues)

        return True, "System requirements met"

    def download_model(self, model_name: str, progress_callback=None) -> Tuple[bool, str]:
        """
        下载模型

        Args:
            model_name: 模型名称
            progress_callback: 进度回调函数

        Returns:
            (是否成功, 结果信息)
        """
        if model_name not in self.MODEL_CONFIG:
            return False, f"Unsupported model: {model_name}"

        config = self.MODEL_CONFIG[model_name]
        model_path = self.base_dir / config["local_dir"]

        # 检查系统要求
        req_ok, req_msg = self.check_system_requirements(model_name)
        if not req_ok:
            return False, f"System requirements not met:\n{req_msg}"

        # 如果模型已存在且完整，跳过下载
        exists, msg = self.check_model_exists(model_name)
        if exists:
            return True, f"Model already exists at: {msg}"

        try:
            self.logger.info(f"开始下载模型: {config['repo_id']}")
            self.logger.info(f"目标目录: {model_path}")
            self.logger.info(f"预计大小: {config['size_gb']}GB")

            if progress_callback:
                progress_callback(0.1, "Preparing download...")

            # 构建下载命令
            cmd = [
                "huggingface-cli", "download",
                config["repo_id"],
                "--local-dir", str(model_path),
                "--local-dir-use-symlinks", "False"  # 避免符号链接问题
            ]

            if progress_callback:
                progress_callback(0.2, "Starting download...")

            # 执行下载
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=self.base_dir
            )

            # 监控下载进度
            progress = 0.2
            for line in process.stdout:
                self.logger.info(line.strip())

                # 简单的进度估算
                if "Downloading" in line:
                    progress = min(progress + 0.01, 0.8)
                elif "fetching" in line:
                    progress = min(progress + 0.05, 0.9)

                if progress_callback:
                    progress_callback(progress, f"Downloading... {line.strip()[:50]}...")

            process.wait()

            if process.returncode != 0:
                return False, f"Download failed with return code: {process.returncode}"

            if progress_callback:
                progress_callback(0.95, "Verifying download...")

            # 验证下载的模型
            exists, msg = self.check_model_exists(model_name)
            if not exists:
                return False, f"Download incomplete: {msg}"

            if progress_callback:
                progress_callback(1.0, "Download completed!")

            self.logger.info(f"模型下载完成: {model_path}")
            return True, f"Model downloaded successfully to: {model_path}"

        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg

    def list_models(self) -> dict:
        """列出所有支持的模型及其状态"""
        models_status = {}

        for model_name, config in self.MODEL_CONFIG.items():
            exists, path_or_msg = self.check_model_exists(model_name)
            models_status[model_name] = {
                "config": config,
                "exists": exists,
                "path": path_or_msg if exists else None,
                "status_message": path_or_msg
            }

        return models_status

    def get_model_path(self, model_name: str) -> Optional[str]:
        """获取模型路径（如果存在）"""
        exists, path_or_msg = self.check_model_exists(model_name)
        return path_or_msg if exists else None

    def estimate_download_time(self, model_name: str, speed_mbps: float = 100) -> str:
        """估算下载时间"""
        if model_name not in self.MODEL_CONFIG:
            return "Unknown"

        size_gb = self.MODEL_CONFIG[model_name]["size_gb"]
        size_mb = size_gb * 1024
        time_seconds = size_mb * 8 / speed_mbps  # 转换为秒

        if time_seconds < 60:
            return f"{time_seconds:.0f} seconds"
        elif time_seconds < 3600:
            return f"{time_seconds/60:.0f} minutes"
        else:
            return f"{time_seconds/3600:.1f} hours"


def main():
    """测试模型管理器"""
    import argparse

    parser = argparse.ArgumentParser(description="Wan2.2-Animate Model Manager")
    parser.add_argument("--download", choices=["animate-14B"], help="Download specified model")
    parser.add_argument("--check", choices=["animate-14B"], help="Check if model exists")
    parser.add_argument("--list", action="store_true", help="List all models")
    parser.add_argument("--dir", default=".", help="Base directory for models")

    args = parser.parse_args()

    manager = ModelManager(args.dir)

    if args.list:
        models = manager.list_models()
        print("\n=== Supported Models ===")
        for name, info in models.items():
            status = "✅ Available" if info["exists"] else "❌ Not found"
            print(f"{name}: {status}")
            print(f"  Description: {info['config']['description']}")
            print(f"  Size: {info['config']['size_gb']}GB")
            if info["exists"]:
                print(f"  Path: {info['path']}")
            print()

    elif args.check:
        exists, msg = manager.check_model_exists(args.check)
        if exists:
            print(f"✅ Model found: {msg}")
        else:
            print(f"❌ Model not found: {msg}")

    elif args.download:
        print(f"Downloading {args.download}...")

        def progress(percent, message):
            print(f"Progress: {percent*100:.1f}% - {message}")

        success, msg = manager.download_model(args.download, progress)
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()