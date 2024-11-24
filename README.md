# Superset 汉化/中文版

![Version](https://img.shields.io/docker/v/lutinglt/superset-zh/latest?arch=amd64&sort=semver&color=066da5) ![Docker Pulls](https://img.shields.io/docker/pulls/lutinglt/superset-zh.svg?style=flat&label=pulls&logo=docker) ![Docker Size](https://img.shields.io/docker/image-size/lutinglt/superset-zh/latest?color=066da5&label=size) ![License](https://img.shields.io/github/license/lutinglt/superset-zh)

## 简介

[PR: 29476](https://github.com/apache/superset/pull/29476) 这个提交中删除了大量的中文翻译，导致 Superset 的中文翻译质量大幅下降, 在这次提交后便没有人再对中文翻译进行维护。

本项目基于 [PR: 27922](https://github.com/apache/superset/pull/27922) 的最后一次中文翻译提交，为了方便维护翻译, 用 Python 构建了翻译脚本, 改变了汉化步骤, 先生成 messages.json, 再通过 json 生成 messages.po 和 messages.mo, 此过程修复了一些翻译文件无法正常生效的问题.

## 部署

### Docker 镜像

#### 开箱即用

基于官方镜像生成, 修复了汉化问题, 仅保留中文和英文两种语言并且默认显示中文, 默认时区上海, 并添加了 PostgreSQL 和 MySQL 数据库驱动.
为了做到开箱即用, 修改了以下默认配置 (不推荐生产使用):

```python
SECRET_KEY = 'superset'
WTF_CSRF_ENABLED = False
TALISMAN_ENABLED = False
```

一键启动体验汉化版 Superset, (http://localhost:8080)

```bash
docker run -d --name superset -p 8080:8088 lutinglt/superset-zh
```

登录仍需执行以下命令 (命令创建一个管理员账户, 用户名密码均为 `admin`)

```bash
docker exec -it superset superset fab create-admin \
              --username admin \
              --firstname 'admin' \
              --lastname 'admin' \
              --email admin@superset.apache.org \
              --password 'admin'
docker exec -it superset superset db upgrade
docker exec -it superset superset init
```

#### 自定义配置

参考配置 docker-compose.yml

```yml
services:
  superset:
    image: lutinglt/superset-zh
    container_name: superset
    hostname: superset
    restart: always
    ports:
      - 8080:8088
    volumes:
    # sqlite 存储持久化
      - ./superset:~/.superset
    # 导入配置文件
      - ./superset_config.py:/app/pythonpath/superset_config.py
```

参考配置 superset_config.py (PostgreSQL 数据库)

> [!NOTE]
>
> superset_config.py 会覆盖 config.py 里的配置, 优先级更高.
> SECRET_KEY 会用来签名 cookie 和加密 Superset 存储在数据库中的敏感数据
> 推荐使用 `openssl rand -base64 42` 命令生成一个足够复杂的安全密钥

```python
SECRET_KEY = 'superset'
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@postgres/database'
```

#### 手动构建

```bash
git clone https://github.com/lutinglt/superset-zh.git
cd superset-zh
docker build -t lutinglt/superset-zh .
```

> [!TIP]
>
> 4.1.1 有两个 Python 版本, 官方默认的基于 3.10, 无明显 BUG 的情况下本仓库将仅更新最新的稳定版镜像, 可以根据需要替换 Dockerfile 中 FROM 关键字后的基础镜像.
>
> 推荐使用最新的 Python 版本, 以提高性能和安全性, 但可能存在一些未知的 BUG, 请自行测试.

### 手动汉化

找到 Superset 安装目录下的 `translations` 目录, 找到 `zh/LC_MESSAGES` 目录

下载最新版本的 `messages.json` 和 `messages.mo` 文件复制到 `zh/LC_MESSAGES` 目录下

重启 Superset 查看汉化效果.

> [!IMPORTANT]
>
> config.py 里的 `LANGUAGES` 变量为空会关闭语言选择框, 默认为空, 参考配置:
>
>```python
>LANGUAGES = {
>    "zh": {"flag": "cn", "name": "简体中文"},
>    "en": {"flag": "us", "name": "English"},
>}
>```

> [!NOTE]
>
> superset_config.py 会覆盖 config.py 里的配置, 优先级更高.

> [!TIP]
>
> config.py 里的 `BABEL_DEFAULT_LOCALE` 变量可能会影响标题栏的汉化, 默认为 `en`, 如果标题栏没有汉化修改为 `zh` 下载最新的 `messages.po` 到 `zh/LC_MESSAGES` 目录下重新编译即可.
>
>```python
># 替换成自己的安装目录下的 translations 目录
># 编译报错请无视
>pybabel compile -d superset/translations
>```

> [!TIP]
>
> 官方镜像 Superset 2.1.0 之后安装的默认安全选项更为严格, 部署后登录不上, 或无法启动推荐添加以下配置(汉化版默认添加了这些配置):
>
> ```python
> SECRET_KEY = 'superset' # 安全密钥, 启动必须进行配置
> WTF_CSRF_ENABLED = False # 关闭 CSRF 验证
> TALISMAN_ENABLED = False  # 关闭 TALISMAN 安全选项
> CONTENT_SECURITY_POLICY_WARNING = False  # 关闭内容安全策略警告
> ```

## 脚本

> [!IMPORTANT]
>
> 脚本基于 Python 3.12 构建, 其中使用了一些类型注解可能会影响兼容性, 如有报错请自行删除, Python >= 3.8 理论上都可以直接运行, 安装依赖运行命令:
>
>```bash
>pip install -r requirements.txt
>```

脚本主要改变了汉化步骤, json 更有利于定位和修改翻译内容, 脚本另一个功能是筛选出没有翻译的部分, 直接补充即可, 不需要手动浏览或者使用一些翻译软件进行翻译.(例如: poedit)

### `generate_locales.py`

基于 Superset 项目下的 `superset/translations/messages.pot` 和 `superset/translations/zh/LC_MESSAGES/messages.po` 生成最新的需要翻译的内容, 然后取本项目下 `messages.json` 已翻译的部分, 覆盖需要翻译的内容, 生成全部翻译条目(包含未翻译)和筛选出未翻译的条目的 json 文件, 进行手动校验翻译过程, 方便补充新翻译和修改已翻译内容, 具体查看脚本中的文档注释内容.

### `generate_messages.py`

根据已经翻译的内容生成 Superset 前端需要的 `messages.json` 和 `messages.mo`, 具体查看脚本中的文档注释内容.

> [!NOTE]
>
> 如果只是少量的纠正和补充(可以直接定位的), 只修改 `messages.json` 文件即可
>
> 然后运行 `generate_locales.py` 和 `generate_messages.py` 生成 `messages.mo` 文件, 供自己立即查看效果

## 贡献

欢迎提交 PR, 修复汉化问题, 补充汉化内容或者优化翻译脚本.

汉化贡献仅需提交最新的 `messages.json` 文件即可.