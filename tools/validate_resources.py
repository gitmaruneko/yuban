#!/usr/bin/env python3
"""Validate the generated YuBan resource index before deployment."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse


RESOURCE_PATH = Path("website/data/sample-resources.json")
ALLOWED_TYPES = {"文章", "影片", "工具／用品", "混合型內容", "連結入口"}
ALLOWED_STATUSES = {"verified", "ai_draft"}
ALLOWED_AGE_STAGES = {"孕期", "0-1歲", "1-3歲", "3-6歲", "全齡"}
ALLOWED_AGE_GROUPS = {"學齡前", "國小", "國中", "高中", "全齡"}
ALLOWED_RESOURCE_CATEGORIES = {"學習教材", "課程", "活動", "補助", "政策", "機構"}
ALLOWED_AUDIENCES = {"兒童", "家長", "教師", "學校"}
REQUIRED_TEXT_FIELDS = {
    "id",
    "title",
    "summary",
    "type",
    "type_label",
    "age_label",
    "topic",
    "topic_group",
    "ai_summary_status",
    "credibility_note",
    "notice",
    "url",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate_http_url(url: str, resource_id: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        fail(f"{resource_id}: invalid HTTP(S) URL: {url}")


def validate_optional_taxonomy(resource: dict, resource_id: str) -> None:
    taxonomy_rules = {
        "age_groups": ALLOWED_AGE_GROUPS,
        "resource_categories": ALLOWED_RESOURCE_CATEGORIES,
        "audiences": ALLOWED_AUDIENCES,
    }
    for field, allowed_values in taxonomy_rules.items():
        if field not in resource:
            continue
        values = resource[field]
        if not isinstance(values, list) or not values or not all(
            isinstance(value, str) and value.strip() for value in values
        ):
            fail(f"{resource_id}: {field} must be a non-empty string array")
        unknown_values = set(values) - allowed_values
        if unknown_values:
            fail(f"{resource_id}: unsupported {field}: {sorted(unknown_values)}")

    for field in ("regions", "languages"):
        if field not in resource:
            continue
        values = resource[field]
        if not isinstance(values, list) or not values or not all(
            isinstance(value, str) and value.strip() for value in values
        ):
            fail(f"{resource_id}: {field} must be a non-empty string array")
    if "origin_region" in resource and (
        not isinstance(resource["origin_region"], str) or not resource["origin_region"].strip()
    ):
        fail(f"{resource_id}: origin_region must be a non-empty string")


def validate_resources(resources: object) -> None:
    if not isinstance(resources, list):
        fail("Resource index must contain a JSON array")
    ids: set[str] = set()
    urls: set[str] = set()
    for index, resource in enumerate(resources, start=1):
        label = resource.get("id") or f"row {index}"
        missing = [
            field
            for field in REQUIRED_TEXT_FIELDS
            if not isinstance(resource.get(field), str) or not resource[field].strip()
        ]
        if missing:
            fail(f"{label}: missing text fields: {', '.join(sorted(missing))}")
        if resource["id"] in ids:
            fail(f"Duplicate resource ID: {resource['id']}")
        if resource["url"] in urls:
            fail(f"Duplicate resource URL: {resource['url']}")
        ids.add(resource["id"])
        urls.add(resource["url"])

        validate_http_url(resource["url"], resource["id"])
        if resource["type"] not in ALLOWED_TYPES:
            fail(f"{label}: unsupported content type: {resource['type']}")
        if resource["ai_summary_status"] not in ALLOWED_STATUSES:
            fail(f"{label}: unsupported review status: {resource['ai_summary_status']}")
        if not isinstance(resource.get("tags"), list) or not resource["tags"]:
            fail(f"{label}: tags must be a non-empty array")
        if not isinstance(resource.get("age_ranges"), list) or not resource["age_ranges"]:
            fail(f"{label}: age_ranges must be a non-empty array")
        unknown_ages = set(resource["age_ranges"]) - ALLOWED_AGE_STAGES
        if unknown_ages:
            fail(f"{label}: unsupported age stages: {sorted(unknown_ages)}")

        source = resource.get("source")
        if not isinstance(source, dict):
            fail(f"{label}: source must be an object")
        for field in ("name", "type", "url"):
            if not isinstance(source.get(field), str) or not source[field].strip():
                fail(f"{label}: source.{field} is required")
        if source["url"] != resource["url"]:
            fail(f"{label}: source URL does not match resource URL")
        validate_optional_taxonomy(resource, resource["id"])


def main() -> None:
    resources = json.loads(RESOURCE_PATH.read_text(encoding="utf-8"))
    validate_resources(resources)

    print(f"Validated {len(resources)} resources in {RESOURCE_PATH}")


if __name__ == "__main__":
    main()
