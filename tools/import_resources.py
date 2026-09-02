#!/usr/bin/env python3
"""Convert the YuBan resource workbook into the website JSON index."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from openpyxl import load_workbook


REQUIRED_HEADERS = (
    "資源名稱",
    "連結",
    "摘要",
    "內容類型",
    "提供方／來源類型",
    "原始來源",
    "是否為入口型資源",
    "年齡階段",
    "主題",
    "關鍵標籤",
    "審核狀態",
    "可信度備註",
    "注意事項",
)

TYPE_MAP = {
    "電子手冊": "文章",
    "資訊專區／文件下載": "文章",
    "政策／服務說明": "文章",
    "政策專頁": "文章",
    "衛教文章／門診資訊": "文章",
    "圖表／衛教說明": "文章",
    "影音／宣導教材": "影片",
    "影音／衛教專區": "混合型內容",
    "查詢工具": "工具／用品",
    "保護專線／線上服務": "工具／用品",
    "網安資源／申訴入口": "工具／用品",
    "連結入口": "連結入口",
    "資源入口": "連結入口",
    "線上課程入口": "連結入口",
    "查詢入口": "連結入口",
    "醫院衛教專區": "連結入口",
    "專業衛教專區": "連結入口",
    "資訊入口": "連結入口",
    "專業資訊平台": "連結入口",
    "專業資源入口": "連結入口",
    "親職內容專區": "連結入口",
}

AGE_STAGE_MAP = {
    "全齡": ["全齡"],
    "孕前–2歲": ["孕期", "0-1歲", "1-3歲"],
    "孕前–6歲": ["孕期", "0-1歲", "1-3歲", "3-6歲"],
    "孕期–2歲以上": ["孕期", "0-1歲", "1-3歲", "3-6歲"],
    "孕期–學齡前": ["孕期", "0-1歲", "1-3歲", "3-6歲"],
    "孕期–6歲": ["孕期", "0-1歲", "1-3歲", "3-6歲"],
    "0–1歲": ["0-1歲"],
    "0–3歲": ["0-1歲", "1-3歲"],
    "0–6歲": ["0-1歲", "1-3歲", "3-6歲"],
    "0–7歲": ["0-1歲", "1-3歲", "3-6歲"],
    "0–18歲": ["0-1歲", "1-3歲", "3-6歲"],
    "0–18歲及照顧者": ["0-1歲", "1-3歲", "3-6歲"],
    "0歲–學齡前": ["0-1歲", "1-3歲", "3-6歲"],
    "2–6歲": ["1-3歲", "3-6歲"],
    "6–12歲": ["3-6歲"],
    "6–18歲及照顧者": ["3-6歲"],
}

TOPIC_GROUPS = {
    "孕產與嬰幼兒照護": "健康與照護",
    "健康與生活照護": "健康與照護",
    "預防接種": "健康與照護",
    "兒童預防保健": "健康與照護",
    "新生兒照護": "健康與照護",
    "兒童健康": "健康與照護",
    "母乳哺育": "健康與照護",
    "兒童就醫資源": "健康與照護",
    "生長發育": "健康與照護",
    "視力保健": "健康與照護",
    "兒童口腔保健": "健康與照護",
    "兒科疾病與照護": "健康與照護",
    "兒科疾病衛教": "健康與照護",
    "早產兒照護": "健康與照護",
    "兒童發展篩檢": "發展與學習",
    "早期療育": "發展與學習",
    "幼兒園與學前教保": "發展與學習",
    "課後照顧": "發展與學習",
    "兒童發展與早療": "發展與學習",
    "親子共讀": "發展與學習",
    "親職知能": "親職與家庭",
    "補助與家庭支持": "親職與家庭",
    "親職與家庭關係": "親職與家庭",
    "親職教養與家庭支持": "親職與家庭",
    "兒童事故傷害預防": "安全與保護",
    "兒少保護": "安全與保護",
    "兒童權利": "安全與保護",
    "兒少網路安全": "安全與保護",
    "托育媒合": "托育與服務",
    "兒童青少年心理健康": "情緒與心理",
}


def split_tags(value: str) -> list[str]:
    return [tag.strip() for tag in re.split(r"[,，、;；]", value) if tag.strip()]


def make_resource_id(url: str) -> str:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    return f"resource-{digest}"


def parse_review_status(value: str) -> tuple[str, str | None]:
    reviewed_at = None
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", value)
    if date_match:
        reviewed_at = date_match.group(1)
    status = "verified" if value.startswith("人工核實") else "ai_draft"
    return status, reviewed_at


def validate_url(url: str, row_number: int) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"第 {row_number} 列不是有效的 HTTP(S) 網址：{url}")


def convert_row(row: dict[str, str], row_number: int) -> dict[str, object]:
    raw_type = row["內容類型"]
    age_label = row["年齡階段"]
    topic = row["主題"]
    url = row["連結"]

    if raw_type not in TYPE_MAP:
        raise ValueError(f"第 {row_number} 列有未定義的內容類型：{raw_type}")
    if age_label not in AGE_STAGE_MAP:
        raise ValueError(f"第 {row_number} 列有未定義的年齡階段：{age_label}")
    if topic not in TOPIC_GROUPS:
        raise ValueError(f"第 {row_number} 列有未定義的主題：{topic}")

    validate_url(url, row_number)
    review_status, reviewed_at = parse_review_status(row["審核狀態"])

    return {
        "id": make_resource_id(url),
        "title": row["資源名稱"],
        "summary": row["摘要"],
        "type": TYPE_MAP[raw_type],
        "type_label": raw_type,
        "source": {
            "name": row["原始來源"],
            "type": row["提供方／來源類型"],
            "url": url,
        },
        "is_hub": row["是否為入口型資源"] == "是",
        "age_label": age_label,
        "age_ranges": AGE_STAGE_MAP[age_label],
        "topic": topic,
        "topic_group": TOPIC_GROUPS[topic],
        "tags": split_tags(row["關鍵標籤"]),
        "ai_summary_status": review_status,
        "reviewed_at": reviewed_at,
        "credibility_note": row["可信度備註"],
        "notice": row["注意事項"],
        "url": url,
    }


def load_resources(workbook_path: Path) -> list[dict[str, object]]:
    workbook = load_workbook(workbook_path, read_only=True, data_only=True)
    worksheet = workbook.active
    rows = worksheet.iter_rows(values_only=True)

    try:
        headers = tuple(str(value).strip() if value is not None else "" for value in next(rows))
    except StopIteration as exc:
        raise ValueError("工作簿沒有任何資料") from exc

    if headers != REQUIRED_HEADERS:
        raise ValueError(
            "工作簿欄位與預期不符。\n"
            f"預期：{REQUIRED_HEADERS}\n"
            f"實際：{headers}"
        )

    resources: list[dict[str, object]] = []
    for row_number, values in enumerate(rows, start=2):
        if all(value in (None, "") for value in values):
            continue
        if any(value in (None, "") for value in values):
            missing = [headers[index] for index, value in enumerate(values) if value in (None, "")]
            raise ValueError(f"第 {row_number} 列缺少欄位：{', '.join(missing)}")

        row = {headers[index]: str(value).strip() for index, value in enumerate(values)}
        resources.append(convert_row(row, row_number))

    ids = [resource["id"] for resource in resources]
    urls = [resource["url"] for resource in resources]
    if len(ids) != len(set(ids)) or len(urls) != len(set(urls)):
        raise ValueError("工作簿包含重複網址")
    if len(resources) != 30:
        raise ValueError(f"MVP 預期 30 筆資源，目前讀到 {len(resources)} 筆")

    return resources


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("docs/resource_v0.2.xlsx"),
        help="來源 Excel 工作簿",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("website/data/sample-resources.json"),
        help="網站 JSON 輸出位置",
    )
    args = parser.parse_args()

    resources = load_resources(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(resources, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Imported {len(resources)} resources into {args.output}")


if __name__ == "__main__":
    main()
