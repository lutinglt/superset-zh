# Superset 汉化/中文版

![Version](https://img.shields.io/docker/v/lutinglt/superset-zh/latest?arch=amd64&sort=semver&color=066da5) ![Docker Pulls](https://img.shields.io/docker/pulls/lutinglt/superset-zh.svg?style=flat&label=pulls&logo=docker) ![Docker Size](https://img.shields.io/docker/image-size/lutinglt/superset-zh/latest?color=066da5&label=size) ![License](https://img.shields.io/github/license/lutinglt/superset-zh)

## 简介

[PR: 29476](https://github.com/apache/superset/pull/29476) 这个提交中删除了大量的中文翻译，导致 Superset 的中文翻译质量大幅下降, 在这次提交后便没有人再对中文翻译进行维护。

本项目基于 [PR: 27922](https://github.com/apache/superset/pull/27922) 的最后一次中文翻译提交，用 Python 构建了翻译脚本, 脚本改变了汉化步骤, 先生成 messages.json, 再通过 json 生成 messages.po, 此过程修复了一些翻译文件无法正常生效的问题.

## 使用方法

### Docker 镜像

#### 下载镜像

基于官方镜像生成, 修复了汉化问题, 仅保留中文和英文两种语言并且默认显示中文, 默认时区上海, 并添加了 Postgres 和 MySQL 数据库驱动, 其他配置与官方镜像相同.

```bash
docker pull lutinglt/superset-zh
```

#### 手动构建

FROM 关键字后替换自己需要的官方镜像标签

```bash
git clone https://github.com/lutinglt/superset-zh.git
cd superset-zh
docker build -t lutinglt/superset-zh .
```

### 手动汉化

找到 Superset 安装目录下的 `translations` 目录, 找到 `zh/LC_MESSAGES` 目录, 直接将项目仓库里的 `messages.json` 和 `messages.po` 文件复制到 `zh/LC_MESSAGES` 目录下, 然后运行:

```bash
# 替换成自己的安装目录下的 translations 目录
pybabel compile -d superset/translations
```

重启 Superset 查看汉化效果.

> [!IMPORTANT]
>
> config.py 里的 `BABEL_DEFAULT_LOCALE` 变量会影响标题栏的汉化, 默认为 `en`, 修改为 `zh` 重新编译即可.

> [!IMPORTANT]
>
> config.py 里的 `LANGUAGES` 变量为空会关闭语言选择框, 默认为空, 参考配置:

```python
BABEL_DEFAULT_LOCALE = "zh"
LANGUAGES = {
    "zh": {"flag": "cn", "name": "简体中文"},
    "en": {"flag": "us", "name": "English"},
}
```

> [!NOTE]
>
> superset_config.py 会覆盖 config.py 里的配置, 优先级更高.

> [!TIP]
>
> Superset 2.1.0 之后安装的默认安全选项更为严格, 部署后登录不上, 或无法启动推荐添加以下配置
>
> ```python
> SECRET_KEY = 'superset' # 安全密钥, 启动必须进行配置
> WTF_CSRF_ENABLED = False # 关闭 CSRF 验证
> TALISMAN_ENABLED = False  # 关闭 TALISMAN 安全选项
> CONTENT_SECURITY_POLICY_WARNING = False  # 关闭内容安全策略警告
> ```

## 脚本说明

### `generate_locales.py`

基于 Superset 项目下的 `superset/translations/messages.pot` 和 `superset/translations/zh/LC_MESSAGES/messages.po` 生成最新的需要翻译的内容, 然后取本项目下 `messages.json` 已翻译的部分覆盖需要翻译的内容, 生成全部翻译条目(包含未翻译)和筛选出未翻译的条目的 json 文件, 进行手动校验翻译过程, 方便补充新翻译和修改已翻译内容, 具体查看脚本文档注释内容.

### `generate_messages.py`

根据已经翻译的内容生成 Superset 前端需要的 `messages.json` 和 `messages.po`, 具体查看脚本文档注释内容.

## 贡献

欢迎提交 PR, 修复汉化问题, 补充汉化内容或者优化翻译脚本.

汉化贡献仅需提交最新的 `messages.json` 文件即可