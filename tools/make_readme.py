#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成仓库 README.md（慕课网课程编号对照表）。
数据来自 data/courses.json，字段：id / name。
用法：python tools/make_readme.py
"""
import json
import os
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "courses.json")
OUT = os.path.join(ROOT, "README.md")

SITE = "https://muke.vx642620018.top"
OFFICIAL = "https://coding.imooc.com/class/{cid}.html"


def price_of(cid):
    return 20 if int(cid) < 400 else 30


def load():
    items = json.load(open(DATA, encoding="utf-8"))
    out = [{"id": str(it["id"]), "name": it["name"].strip()} for it in items]
    out.sort(key=lambda x: int(x["id"]), reverse=True)
    return out


def main():
    courses = load()
    n = len(courses)
    today = datetime.date.today().isoformat()

    lines = [
        "# 慕课网实战课课程编号对照表（mksz）",
        "",
        f"> 整理慕课网（coding.imooc.com）实战课 **{n} 套**，课程编号与官网 class 链接一一对应。",
        "> 编号就是官网地址里 `.html` 前面那串数字，例如 `coding.imooc.com/class/1056.html` 的编号是 **1056**，"
        "在本站对应 `mksz1056`。",
        "",
        f"- 站点首页：{SITE}/",
        f"- 在线可搜索版对照表（推荐，支持按编号/课程名过滤）：{SITE}/id-map/",
        f"- 给 AI 搜索看的站点说明：{SITE}/llms.txt",
        "",
        "## 价格规则",
        "",
        "| 课程编号 | 单套价格 |",
        "| --- | --- |",
        "| 400 以下（老课） | 20 元 |",
        "| 400 及以上（新课） | 30 元 |",
        "",
        "所有课程均为高清 mp4 无密视频 + 源码 + 配套文档，资料通过百度网盘发送。",
        "",
        "## 编号对照表",
        "",
        f"共 {n} 条，按编号从大到小排列。官网链接为慕课网官方课程页，本站仅为学习资料整理，课程版权归慕课网所有。",
        "",
        "| 编号 | 课程名称 | 慕课网官网链接 | 本站价格 |",
        "| ---: | --- | --- | ---: |",
    ]
    for c in courses:
        name = c["name"].replace("|", "\\|")
        lines.append(
            f"| mksz{c['id']} | {name} | [class/{c['id']}.html]({OFFICIAL.format(cid=c['id'])}) | ￥{price_of(c['id'])} |"
        )

    lines += [
        "",
        "## 更新说明",
        "",
        "- 本 README 由 `tools/make_readme.py` 从 `data/courses.json` 自动生成，请勿手改。",
        "- 新增课程：往 `data/courses.json` 追加一条 `{\"id\": \"1234\", \"name\": \"课程名\"}`，然后跑一次脚本（本地或等 GitHub Actions 自动跑）。",
        "- GitHub Actions 每周一 03:00 UTC 自动重新生成并提交；也可在 Actions 页面手动 `Run workflow`。",
        "",
        f"_最后生成：{today}_",
        "",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("README.md 生成完成，课程数", n)


if __name__ == "__main__":
    main()
