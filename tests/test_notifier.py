import pytest
from unittest.mock import Mock, patch
from src.notifier import TelegramNotifier


@pytest.fixture
def sample_results():
    """测试数据"""
    return {
        "weibo": {
            "status": "success",
            "data": [
                {"title": "新闻1", "url": "https://example.com/1"},
                {"title": "新闻2", "url": "https://example.com/2"}
            ]
        },
        "zhihu": {
            "status": "success",
            "data": [
                {"title": "新闻3", "url": "https://example.com/3"}
            ]
        }
    }


def test_format_message(sample_results):
    """测试消息格式化"""
    platforms = {
        "weibo": "微博",
        "zhihu": "知乎"
    }

    notifier = TelegramNotifier("fake_token", "fake_chat_id")
    message = notifier.format_message(sample_results, platforms)

    assert "微博" in message
    assert "知乎" in message
    assert "新闻1" in message
    assert "新闻3" in message


@patch('src.notifier.Bot')
def test_send_message(mock_bot, sample_results):
    """测试发送消息"""
    platforms = {"weibo": "微博"}

    # 创建 mock 的异步 send_message 方法
    mock_async_send = Mock()
    mock_bot.return_value.send_message = mock_async_send

    notifier = TelegramNotifier("fake_token", "fake_chat_id")
    notifier.send(sample_results, platforms)

    # 验证 bot.send_message 被调用
    assert mock_async_send.called
