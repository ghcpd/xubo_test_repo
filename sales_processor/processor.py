
"""Sales data processing utilities."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ISO_Z_SUFFIX = "Z"


def _parse_timestamp(raw_value: Any) -> datetime:
    """Return a timezone-aware datetime when possible.

    Raises ValueError when the value cannot be parsed.
    """

    if raw_value is None:
        raise ValueError("timestamp is missing")

    if not isinstance(raw_value, str):
        raise ValueError("timestamp must be a string")

    value = raw_value.strip()
    if not value:
        raise ValueError("timestamp is empty")

    if value.endswith(ISO_Z_SUFFIX):
        # Handle trailing Z by converting to UTC offset
        value = f"{value[:-1]}+00:00"

    return datetime.fromisoformat(value)


def _coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _clean_record(record: Dict[str, Any]) -> Tuple[Dict[str, Any], datetime]:
    """Clean a single sales record, returning the cleaned mapping and timestamp.

    Raises ValueError if the record should be discarded due to invalid timestamp.
    """

    parsed_ts = _parse_timestamp(record.get("timestamp"))

    cleaned: Dict[str, Any] = {
        "id": record.get("id"),
        "product": record.get("product") or "",
        "category": record.get("category") or "",
    }

    price = _coerce_float(record.get("price"))
    quantity = _coerce_int(record.get("quantity"))
    total_value = round(price * quantity, 2)

    cleaned.update(
        {
            "price": price,
            "quantity": quantity,
            "timestamp": parsed_ts.isoformat(),
            "total_value": total_value,
        }
    )

    return cleaned, parsed_ts


def _clean_records(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []

    for record in records:
        try:
            cleaned_record, _ = _clean_record(record)
        except ValueError:
            continue
        cleaned.append(cleaned_record)

    return cleaned


def _aggregate_category(cleaned: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    totals: Dict[str, float] = defaultdict(float)

    for row in cleaned:
        totals[row["category"]] += row["total_value"]

    return [
        {"category": category, "total_sales": round(total, 2)}
        for category, total in sorted(totals.items())
    ]


def _aggregate_product(cleaned: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    totals: Dict[str, float] = defaultdict(float)

    for row in cleaned:
        totals[row["product"]] += row["total_value"]

    top_items = sorted(
        (
            {"product": product, "total_sales": round(total, 2)}
            for product, total in totals.items()
        ),
        key=lambda item: item["total_sales"],
        reverse=True,
    )

    return top_items[:5]


def _aggregate_monthly(cleaned: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    totals: Dict[str, float] = defaultdict(float)

    for row in cleaned:
        timestamp = datetime.fromisoformat(row["timestamp"])
        key = timestamp.strftime("%Y-%m")
        totals[key] += row["total_value"]

    return [
        {"month": month, "total_sales": round(total, 2)}
        for month, total in sorted(totals.items())
    ]


def process_sales_data(input_path: Path | str, output_dir: Path | str) -> Dict[str, Any]:
    """Process sales data and persist the requested artefacts.

    Returns a mapping with the computed artefacts for convenience/testing.
    """

    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    if not isinstance(payload, list):
        raise ValueError("input JSON must be a list of records")

    cleaned = _clean_records(payload)

    category_summary = _aggregate_category(cleaned)
    top_products = _aggregate_product(cleaned)
    monthly_summary = _aggregate_monthly(cleaned)

    artefacts = {
        "cleaned": cleaned,
        "category_summary": category_summary,
        "top_products": top_products,
        "monthly_summary": monthly_summary,
    }

    _persist_json(output_dir / "cleaned_sales.json", artefacts["cleaned"])
    _persist_json(output_dir / "category_sales.json", artefacts["category_summary"])
    _persist_json(output_dir / "top_products.json", artefacts["top_products"])
    _persist_json(output_dir / "monthly_sales.json", artefacts["monthly_summary"])

    return artefacts


def _persist_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
