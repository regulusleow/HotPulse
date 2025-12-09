import time
import requests
from typing import Dict, List, Any


class NewsFetcher:
    """NewsNow API 数据获取器"""

    def __init__(self, api_base_url: str, request_interval: int = 1000):
        """
        初始化

        Args:
            api_base_url: API 基础 URL
            request_interval: 请求间隔(毫秒)
        """
        self.api_base_url = api_base_url
        self.request_interval = request_interval / 1000  # 转换为秒

    def fetch_platform(self, platform_id: str) -> Dict[str, Any]:
        """
        获取单个平台的热点数据

        Args:
            platform_id: 平台 ID

        Returns:
            API 响应数据
        """
        url = f"{self.api_base_url}?id={platform_id}&latest"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        return response.json()

    def fetch_all(self, platforms: List[Dict[str, str]]) -> Dict[str, Dict[str, Any]]:
        """
        获取所有平台的热点数据

        Args:
            platforms: 平台列表 [{"id": "weibo", "name": "微博"}, ...]

        Returns:
            {platform_id: response_data}
        """
        results = {}

        for platform in platforms:
            platform_id = platform["id"]
            print(f"正在获取 {platform['name']} 热点数据...")

            try:
                data = self.fetch_platform(platform_id)
                results[platform_id] = data
                print(f"✓ {platform['name']} 获取成功")
            except Exception as e:
                print(f"✗ {platform['name']} 获取失败: {e}")
                results[platform_id] = {"status": "error", "error": str(e)}

            # 请求间隔
            time.sleep(self.request_interval)

        return results
