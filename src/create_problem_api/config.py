from __future__ import annotations

import configparser
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config.ini"


def create_config_parser() -> configparser.ConfigParser:
    """Create a parser that preserves markdown-style multiline values."""
    return configparser.ConfigParser(
        interpolation=None,
        comment_prefixes=(";",),
        inline_comment_prefixes=(";",),
    )


def load_config(config_path: Path | None = None) -> configparser.ConfigParser:
    config = create_config_parser()
    target = config_path or CONFIG_PATH
    config.read(target, encoding="utf-8")
    return config
