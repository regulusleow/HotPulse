#!/usr/bin/env python3
"""
HotPulse - 热点新闻监控推送工具
"""
import sys
from src.config import load_config
from src.fetcher import NewsFetcher
from src.filter import KeywordFilter
from src.notifier import TelegramNotifier


def main():
    """主函数"""
    print("=== HotPulse 热点新闻推送 ===\n")

    # 1. 加载配置
    print("📋 加载配置...")
    config = load_config()

    # 2. 初始化模块
    fetcher = NewsFetcher(
        api_base_url=config["crawler"]["api_base_url"],
        request_interval=config["crawler"]["request_interval"]
    )

    keyword_filter = KeywordFilter(config.get("keywords", ""))

    notifier = TelegramNotifier(
        bot_token=config["telegram"]["bot_token"],
        chat_id=config["telegram"]["chat_id"]
    )

    # 3. 获取数据
    print(f"\n🔍 开始获取 {len(config['platforms'])} 个平台的热点数据...\n")
    results = fetcher.fetch_all(config["platforms"])

    # 4. 应用关键词过滤
    if config.get("keywords"):
        print(f"\n🔎 应用关键词过滤: {config['keywords']}")
        for platform_id in results:
            status = results[platform_id].get("status", "")
            if status in ["success", "cache"]:
                # NewsNow API 返回的是 "items" 字段，不是 "data"
                news_list = results[platform_id].get("items", results[platform_id].get("data", []))
                original_count = len(news_list)
                filtered_list = keyword_filter.apply(news_list)
                results[platform_id]["items"] = filtered_list
                filtered_count = len(filtered_list)
                print(f"  {platform_id}: {original_count} -> {filtered_count} 条")

    # 5. 发送推送
    print("\n📤 发送 Telegram 推送...")
    platforms_map = {p["id"]: p["name"] for p in config["platforms"]}
    notifier.send(results, platforms_map)

    print("\n✅ 完成!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)
