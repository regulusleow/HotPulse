FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 复制 crontab 文件
COPY docker/crontab /etc/cron.d/hotpulse
RUN chmod 0644 /etc/cron.d/hotpulse
RUN crontab /etc/cron.d/hotpulse

# 创建日志文件
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
