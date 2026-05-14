"""
配置加载模块。

从项目根目录的 config.ini 读取 Spark / DeepSeek API 密钥、
Prompt 模板和保存路径等配置。禁用插值以避免与 Markdown 或
代码片段中的 % 格式冲突。
"""

from __future__ import annotations

import configparser
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config.ini"


def create_config_parser() -> configparser.ConfigParser:
    """创建禁用插值的 ConfigParser，避免 Markdown 内容中的 % 被误解析。"""
    return configparser.ConfigParser(
        interpolation=None,
        comment_prefixes=(";",),
        inline_comment_prefixes=(";",),
    )


def load_config(config_path: Path | None = None) -> configparser.ConfigParser:
    """加载配置文件，返回 ConfigParser 实例。"""

    config = create_config_parser()
    target = config_path or CONFIG_PATH
    config.read(target, encoding="utf-8")
    return config
