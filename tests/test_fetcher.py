import pytest
from unittest.mock import Mock, patch
from src.fetcher import NewsFetcher


@pytest.fixture
def mock_response():
    """模拟 NewsNow API 响应"""
    return {
        "status": "success",
        "data": [
            {"title": "测试新闻1", "url": "https://example.com/1"},
            {"title": "测试新闻2", "url": "https://example.com/2"},
        ]
    }


def test_fetch_platform_success(mock_response):
    """测试成功获取单个平台数据"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        fetcher = NewsFetcher("https://api.test.com")
        result = fetcher.fetch_platform("weibo")

        assert result["status"] == "success"
        assert len(result["data"]) == 2
        assert result["data"][0]["title"] == "测试新闻1"


def test_fetch_all_platforms(mock_response):
    """测试获取所有平台数据"""
    platforms = [
        {"id": "weibo", "name": "微博"},
        {"id": "zhihu", "name": "知乎"}
    ]

    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        fetcher = NewsFetcher("https://api.test.com")
        results = fetcher.fetch_all(platforms)

        assert len(results) == 2
        assert "weibo" in results
        assert "zhihu" in results
