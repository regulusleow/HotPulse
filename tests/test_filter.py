import pytest
from src.filter import KeywordFilter


@pytest.fixture
def sample_news():
    """测试数据"""
    return [
        {"title": "苹果发布新款 iPhone AI 功能", "url": "https://example.com/1"},
        {"title": "特斯拉推出新车型", "url": "https://example.com/2"},
        {"title": "苹果广告推广活动", "url": "https://example.com/3"},
        {"title": "AI 技术突破性进展", "url": "https://example.com/4"},
    ]


def test_filter_no_keywords(sample_news):
    """测试无关键词时返回全部"""
    filter = KeywordFilter("")
    result = filter.apply(sample_news)
    assert len(result) == 4


def test_filter_with_simple_keyword(sample_news):
    """测试简单关键词匹配"""
    filter = KeywordFilter("苹果")
    result = filter.apply(sample_news)
    assert len(result) == 2
    assert all("苹果" in item["title"] for item in result)


def test_filter_with_required_keyword(sample_news):
    """测试必须包含关键词 +"""
    filter = KeywordFilter("+AI")
    result = filter.apply(sample_news)
    assert len(result) == 2
    assert all("AI" in item["title"] for item in result)


def test_filter_with_exclude_keyword(sample_news):
    """测试排除关键词 !"""
    filter = KeywordFilter("苹果 !广告")
    result = filter.apply(sample_news)
    assert len(result) == 1
    assert "广告" not in result[0]["title"]


def test_filter_with_limit(sample_news):
    """测试数量限制 @"""
    filter = KeywordFilter("@2")
    result = filter.apply(sample_news)
    assert len(result) == 2


def test_filter_complex(sample_news):
    """测试复杂过滤"""
    filter = KeywordFilter("+苹果 !广告 @1")
    result = filter.apply(sample_news)
    assert len(result) == 1
    assert "苹果" in result[0]["title"]
    assert "广告" not in result[0]["title"]
