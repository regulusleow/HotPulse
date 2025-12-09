from typing import List, Dict, Any, Optional


class KeywordFilter:
    """关键词过滤器"""

    def __init__(self, keywords: str):
        """
        初始化

        Args:
            keywords: 关键词字符串，支持: +必须 !排除 @数量限制 普通词
        """
        self.keywords = keywords.strip()
        self.required = []  # 必须包含
        self.exclude = []   # 排除
        self.normal = []    # 普通关键词
        self.limit = None   # 数量限制

        self._parse_keywords()

    def _parse_keywords(self):
        """解析关键词字符串"""
        if not self.keywords:
            return

        parts = self.keywords.split()

        for part in parts:
            if part.startswith('+'):
                self.required.append(part[1:])
            elif part.startswith('!'):
                self.exclude.append(part[1:])
            elif part.startswith('@'):
                try:
                    self.limit = int(part[1:])
                except ValueError:
                    pass
            else:
                self.normal.append(part)

    def apply(self, news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        应用过滤规则

        Args:
            news_list: 新闻列表

        Returns:
            过滤后的新闻列表
        """
        if not self.keywords:
            return news_list

        filtered = []

        for news in news_list:
            title = news.get("title", "")

            # 检查排除词
            if any(exclude in title for exclude in self.exclude):
                continue

            # 检查必须包含
            if self.required and not all(req in title for req in self.required):
                continue

            # 检查普通关键词（至少包含一个）
            if self.normal and not any(kw in title for kw in self.normal):
                continue

            filtered.append(news)

        # 应用数量限制
        if self.limit and self.limit > 0:
            filtered = filtered[:self.limit]

        return filtered
