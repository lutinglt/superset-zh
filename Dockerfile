# 构建翻译文件(请勿替换FROM)
FROM python:3.12.6-slim-bookworm AS builder
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt &&\
    python generate_locales.py && python generate_messages.py

# 将翻译导入镜像(此处替换所需的官方版本)
FROM apache/superset:4.1.1-py311
COPY --from=builder /app/messages.json /app/superset/translations/zh/LC_MESSAGES/messages.json
COPY --from=builder /app/target/messages.mo /app/superset/translations/zh/LC_MESSAGES/messages.mo
USER root
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    export DEBIAN_FRONTEND=noninteractive &&\
    apt-get update &&\
    apt-get -y install --no-install-recommends --no-install-suggests wget pkg-config gcc &&\
    apt-get -y clean && rm -rf /var/lib/apt/lists/* &&\
    # 安装数据库驱动
    pip install psycopg2 mysqlclient &&\
    # 默认语言
    sed -i "s/BABEL_DEFAULT_LOCALE = \"en\"/BABEL_DEFAULT_LOCALE = \"zh\"/" /app/superset/config.py &&\
    # 打开语言切换
    sed -i "s/LANGUAGES = {}/LANGUAGES = {\"zh\": {\"flag\": \"cn\", \"name\": \"简体中文\"}, \"en\": {\"flag\": \"us\", \"name\": \"English\"}}/" /app/superset/config.py

USER superset
