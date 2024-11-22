FROM apache/superset:4.1.1-py311

COPY messages.json /app/superset/translations/zh/LC_MESSAGES/messages.json
COPY messages.po /app/superset/translations/zh/LC_MESSAGES/messages.po

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
    sed -i "s/LANGUAGES = {}/LANGUAGES = {\"zh\": {\"flag\": \"cn\", \"name\": \"简体中文\"}, \"en\": {\"flag\": \"us\", \"name\": \"English\"}}/" /app/superset/config.py &&\
    # 清理不需要的翻译
    cd /app/superset/translations &&\
    rm -rf ar de es fr it ja ko nl pt pt_BR ru sk sl tr uk zh-TW &&\
    # 翻译
    pybabel compile -d /app/superset/translations || true

USER superset
