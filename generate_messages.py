#!/bin/python
# -*- coding:utf-8 -*-
"""
该脚本运行后，会生成 target/messages.json, 并将 target/messages.json 转换为 target/messages.po
检查无误后, 请使用默认配置的 prettier 格式化 target/messages.json
手动覆盖根目录下的 messages.json 和 messages.po, 之后提交代码
"""

import json

import polib

if __name__ == "__main__":
    # 读取翻译文件
    with open("target/tmp/messages.json", "r", encoding="utf-8") as f:
        new_trans: dict[str, str | list[str]] = json.load(f)

    # 读取翻译补充文件
    with open("target/tmp/filter_messages.json", "r", encoding="utf-8") as f:
        new_trans.update(json.load(f))

    # 读取复数翻译标记文件
    with open("target/tmp/plural_messages.json", "r", encoding="utf-8") as f:
        plural_trans: dict[str, str] = json.load(f)

    # 读取现有的翻译文件
    with open("messages.json", "r", encoding="utf-8") as f:
        trans: dict = json.load(f)
        trans["locale_data"]["superset"].update(new_trans)
        # superset 前端翻译的值如果是字符串, 只会显示第一个字符, 所以需要转换为列表
        for k, v in trans["locale_data"]["superset"].items():
            if isinstance(v, str):
                trans["locale_data"]["superset"][k] = [v]

    # 生成 messages.json
    with open("target/messages.json", "w", encoding="utf-8") as f:
        json.dump(trans, f, ensure_ascii=False, indent=2, sort_keys=True)

    # 生成 messages.po
    zh_po = polib.pofile("locales/zh/LC_MESSAGES/messages.po")
    po = polib.POFile()
    po.metadata = zh_po.metadata
    po_trans = {k: v[0] if isinstance(v, list) else v for k, v in trans["locale_data"]["superset"].items()}
    del po_trans[""]
    for msgid, msgstr in po_trans.items():
        if msgid in plural_trans:
            entry = polib.POEntry(
                msgid=msgid,
                msgid_plural=plural_trans[msgid],
                msgstr_plural={0: msgstr},
            )
        else:
            entry = polib.POEntry(
                msgid=msgid,
                msgstr=msgstr,
            )
        po.append(entry)
    po.save("target/messages.po")
