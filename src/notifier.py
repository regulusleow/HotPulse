import asyncio
from typing import Dict, Any
from telegram import Bot
from telegram.constants import ParseMode


class TelegramNotifier:
    """Telegram 推送通知"""

    def __init__(self, bot_token: str, chat_id: str):
        """
        初始化

        Args:
            bot_token: Telegram Bot Token
            chat_id: Telegram Chat ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = Bot(token=bot_token) if bot_token else None

    def format_message(
        self,
        results: Dict[str, Dict[str, Any]],
        platforms: Dict[str, str]
    ) -> str:
        """
        格式化消息

        Args:
            results: {platform_id: response_data}
            platforms: {platform_id: platform_name}

        Returns:
            格式化后的消息文本
        """
        lines = ["🔥 *热点新闻推送*\n"]

        total_count = 0

        for platform_id, data in results.items():
            # 接受 "success" 或 "cache" 状态
            status = data.get("status", "")
            if status not in ["success", "cache"]:
                continue

            platform_name = platforms.get(platform_id, platform_id)
            # NewsNow API 返回的是 "items" 字段，不是 "data"
            news_list = data.get("items", data.get("data", []))

            if not news_list:
                continue

            lines.append(f"\n*📰 {platform_name}*")

            for i, news in enumerate(news_list[:10], 1):  # 最多显示10条
                title = news.get("title", "")
                url = news.get("url", "")

                if url:
                    lines.append(f"{i}. [{title}]({url})")
                else:
                    lines.append(f"{i}. {title}")

                total_count += 1

        if total_count == 0:
            return "暂无热点新闻"

        lines.append(f"\n_共 {total_count} 条热点_")

        return "\n".join(lines)

    def send(self, results: Dict[str, Dict[str, Any]], platforms: Dict[str, str]):
        """
        发送推送

        Args:
            results: {platform_id: response_data}
            platforms: {platform_id: platform_name}
        """
        if not self.bot:
            print("⚠️  未配置 Telegram，跳过推送")
            return

        message = self.format_message(results, platforms)

        try:
            # 使用 asyncio.run() 运行异步函数
            asyncio.run(self._async_send(message))
            print("✓ Telegram 推送成功")
        except Exception as e:
            print(f"✗ Telegram 推送失败: {e}")

    async def _async_send(self, message: str):
        """异步发送消息"""
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
