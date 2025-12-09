# HotPulse

🔥 热点新闻监控推送工具

通过 NewsNow API 获取多平台热点数据，支持关键词过滤，推送到 Telegram。

## 特性

- 📡 支持多平台热点数据获取（微博、知乎、今日头条等）
- 🔍 高级关键词过滤（必须包含、排除、数量限制）
- 📱 Telegram 推送通知（支持异步 API）
- ⚙️ 三部署方式：GitHub Actions / Docker / 本地运行
- 🔧 灵活配置（配置文件 + 环境变量）
- 🐛 自动处理 API 兼容性问题
- 📊 详细的日志输出和故障排除

## 快速开始

### 方式一：GitHub Actions（推荐新手）

1. **Fork 本项目**

2. **配置 Secrets**
   - 进入 `Settings` → `Secrets and variables` → `Actions`
   - 点击 `New repository secret` 添加以下 secrets：
     - `TELEGRAM_BOT_TOKEN`: 你的 Telegram Bot Token
     - `TELEGRAM_CHAT_ID`: 你的 Chat ID

3. **配置关键词过滤（可选）**
   - 编辑 `config/config.yaml` 中的 `keywords` 字段
   - 或者直接在代码中修改（非敏感信息，可以提交）

4. **启用 Actions**
   - 进入 `Actions` 标签
   - 点击 "I understand my workflows, go ahead and enable them"

5. **手动测试**
   - Actions → HotPulse News Crawler → Run workflow

### 方式二：Docker（推荐长期使用）

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/hotpulse.git
   cd hotpulse
   ```

2. **配置环境变量**
   ```bash
   cd docker
   cp .env.example .env
   # 编辑 .env 填入你的配置
   ```

3. **启动容器**
   ```bash
   docker-compose up -d
   ```

4. **查看日志**
   ```bash
   docker logs -f hotpulse
   ```

### 方式三：本地运行（开发调试）

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置 Telegram**
   - 创建 `.env` 文件或设置环境变量：
   ```bash
   export TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
   export TELEGRAM_CHAT_ID="123456789"
   export KEYWORDS="+AI 科技 !广告 @20"  # 可选
   ```

3. **运行程序**
   ```bash
   python main.py
   ```

## 配置说明

### 获取 Telegram 配置

**1. 创建 Telegram Bot：**
- 在 Telegram 搜索 `@BotFather`
- 发送 `/newbot` 命令
- 按提示创建 Bot，获得 `bot_token`（格式：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

**2. 获取 Chat ID：**
- 给你的 Bot 发送一条消息
- 浏览器访问：`https://api.telegram.org/bot<你的bot_token>/getUpdates`
- 在返回的 JSON 中找到 `"chat":{"id":123456789}`，这就是你的 `chat_id`

### 配置文件方式
编辑 `config/config.yaml`：

```yaml
# 关键词过滤（支持高级语法）
keywords: "+AI 科技 !广告 @20"

# Telegram 配置（建议使用环境变量）
telegram:
  bot_token: ""   # 建议使用环境变量 TELEGRAM_BOT_TOKEN
  chat_id: ""     # 建议使用环境变量 TELEGRAM_CHAT_ID
```

### 环境变量方式（推荐）
支持通过环境变量覆盖配置文件：

| 环境变量 | 说明 | 示例 | 使用场景 |
|---------|------|------|----------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token（敏感） | `123456789:ABCdefGHIjklMNOpqrsTUVwxyz` | GitHub Secrets / Docker .env |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID（敏感） | `123456789` | GitHub Secrets / Docker .env |
| `KEYWORDS` | 关键词过滤规则（非敏感） | `"+AI 科技 !广告 @20"` | 本地测试临时覆盖 |

**优先级**：环境变量 > 配置文件

**注意**：
- ✅ `KEYWORDS` 可以直接在 `config.yaml` 中配置（非敏感信息）
- ❌ `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID` 不要写在配置文件中

### 关键词语法

| 语法 | 含义 | 示例 |
|------|------|------|
| `词语` | 包含该词 | `苹果` |
| `+词语` | 必须包含 | `+AI` |
| `!词语` | 排除 | `!广告` |
| `@数量` | 限制数量 | `@10` |

### 平台配置

默认支持平台：微博、知乎、今日头条、百度热搜、B站、抖音

可在 `config/config.yaml` 中自定义添加/删除平台。

参考 [NewsNow 支持的平台](https://github.com/ourongxing/newsnow/tree/main/server/sources)

## 定时设置

### GitHub Actions
编辑 `.github/workflows/crawler.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: "0 * * * *"  # 每小时
  - cron: "0 */2 * * *"  # 每2小时
  - cron: "0 9,21 * * *"  # 每天9点和21点
```

### Docker
编辑 `docker/crontab`：

```
0 * * * * cd /app && /usr/local/bin/python main.py
```

## 故障排除

### 常见问题

1. **程序运行显示"暂无热点新闻"**
   - 原因：NewsNow API 可能返回 403 错误或字段不匹配
   - 解决：程序已自动处理，确保网络正常访问 NewsNow API

2. **Telegram 推送显示成功但未收到消息**
   - 原因：python-telegram-bot 20.x 使用异步 API
   - 解决：程序已修复异步调用问题，确保使用最新版本

3. **关键词过滤不生效**
   - 检查关键词语法是否正确
   - 确保配置文件中 `keywords` 字段格式正确

4. **Docker 容器启动失败**
   - 检查 `.env` 文件配置是否正确
   - 查看日志：`docker logs -f hotpulse`

### API 兼容性说明

- NewsNow API 返回字段为 `"items"` 而不是 `"data"`
- API 状态可能返回 `"success"` 或 `"cache"`，程序都已支持
- 使用 python-telegram-bot 20.x 异步 API

## 开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest

# 运行程序
python main.py
```

## 致谢

- [NewsNow](https://github.com/ourongxing/newsnow) - 数据来源
- [TrendRadar](https://github.com/sansan0/TrendRadar) - 设计参考

## License

MIT
