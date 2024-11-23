#!/bin/python
# -*- coding:utf-8 -*-
"""
所有文件统一使用 utf-8 编码, 行尾统一使用 LF
运行前请下载最新的 messages.pot 和 zh/messages.po 文件, 并放置在 translations 目录下
(鉴于网络原因, 不使用脚本请手动下载) (不需最新无需下载, 直接使用项目中的文件即可)
https://github.com/apache/superset/blob/master/superset/translations/messages.pot
https://github.com/apache/superset/blob/master/superset/translations/zh/LC_MESSAGES/messages.po
先在项目的当前目录运行该脚本, 生成 target 待翻译目录
target/tmp/messages.json : 保存所有翻译, 用于修改现有翻译(如果补充翻译会被filter_messages.json覆盖)
target/tmp/filter_messages.json : 保存未翻译的, 用于补充翻译
target/tmp/plural_messages.json : 保存复数翻译, 标记文件, 请勿修改
target/tmp/messages.po : 翻译模版, 用于核对参考
完善翻译后, 在项目的当前目录运行 generate_messages.py
"""

import json
import os

import polib

if __name__ == "__main__":
    os.makedirs("target/tmp", exist_ok=True)
    # 根据最新的翻译模版 messages.pot 生成新的 messages.po
    pot_file = polib.pofile("translations/messages.pot")
    pot_file.save("target/tmp/messages.po")

    # 读取旧的 messages.json
    with open("messages.json", "r", encoding="utf-8") as f:
        old_trans = json.load(f)["locale_data"]["superset"]
        del old_trans[""]

    # 读取新的 messages.po
    po = polib.pofile("target/tmp/messages.po")
    new_trans = {entry.msgid: entry.msgstr for entry in po}
    plural_trans = {entry.msgid: entry.msgid_plural for entry in po if entry.msgstr_plural}

    # 新的 messages.po 合并新的中文 messages.po 和旧的 messages.json
    zh_po = polib.pofile("translations/zh/LC_MESSAGES/messages.po")
    new_trans.update({zh_entry.msgid: zh_entry.msgstr for zh_entry in zh_po})
    new_trans.update(old_trans)

    # 生成新的 messages.json
    with open("target/tmp/messages.json", "w", encoding="utf-8") as f:
        json.dump(new_trans, f, ensure_ascii=False, indent=2, sort_keys=True)

    with open("target/tmp/filter_messages.json", "w", encoding="utf-8") as f:
        filter_trans = {k: v for k, v in new_trans.items() if v == "" or v == [""]}
        json.dump(filter_trans, f, ensure_ascii=False, indent=2, sort_keys=True)

    with open("target/tmp/plural_messages.json", "w", encoding="utf-8") as f:
        json.dump(plural_trans, f, ensure_ascii=False, indent=2, sort_keys=True)
