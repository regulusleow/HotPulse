import os
import pytest
from src.config import load_config


def test_load_config_from_file():
    """测试从文件加载配置"""
    config = load_config("config/config.yaml")

    assert "crawler" in config
    assert "platforms" in config
    assert config["crawler"]["request_interval"] == 1000
    assert len(config["platforms"]) == 6


def test_load_config_with_env_override():
    """测试环境变量覆盖配置"""
    os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
    os.environ["TELEGRAM_CHAT_ID"] = "test_chat_id"
    os.environ["KEYWORDS"] = "+AI !广告 @10"

    config = load_config("config/config.yaml")

    assert config["telegram"]["bot_token"] == "test_token"
    assert config["telegram"]["chat_id"] == "test_chat_id"
    assert config["keywords"] == "+AI !广告 @10"

    # 清理
    del os.environ["TELEGRAM_BOT_TOKEN"]
    del os.environ["TELEGRAM_CHAT_ID"]
    del os.environ["KEYWORDS"]
