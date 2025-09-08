#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from collections import defaultdict
from typing import Any, Dict, List


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process sales data JSON: clean, transform, aggregate, and export results."
    )
    parser.add_argument(
        "input",
        help="Path to input JSON file containing a list of sales records",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to write output JSON files (default: current directory)",
    )
    return parser.parse_args()


def to_float(value: Any) -> float:
    try:
        if value in (None, "", False):
            return 0.0
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def to_int(value: Any) -> int:
    try:
        if value in (None, "", False):
            return 0
        # Allow floats that are whole numbers
        if isinstance(value, float):
            return int(value)
        return int(str(value).strip())
    except (ValueError, TypeError):
        return 0


def parse_timestamp(value: Any) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    # Try ISO 8601 parsing; handle 'Z' suffix
    v = value.strip()
    try:
        if v.endswith("Z"):
            v = v[:-1] + "+00:00"
        return datetime.fromisoformat(v)
    except ValueError:
        return None


def process_sales(records: List[Dict[str, Any]]):
    cleaned: List[Dict[str, Any]] = []

    for rec in records:
        if not isinstance(rec, dict):
            continue

        price = to_float(rec.get("price"))
        quantity = to_int(rec.get("quantity"))
        ts = parse_timestamp(rec.get("timestamp"))
        if ts is None:
            # Invalid timestamp -> skip record entirely
            continue

        cleaned_rec = {
            "id": rec.get("id"),
            "product": rec.get("product"),
            "category": rec.get("category"),
            "price": price,
            "quantity": quantity,
            "timestamp": ts.isoformat(),
        }
        cleaned_rec["total_value"] = price * quantity
        cleaned.append(cleaned_rec)

    # Aggregations
    category_totals: Dict[str, float] = defaultdict(float)
    product_totals: Dict[str, float] = defaultdict(float)
    monthly_totals: Dict[str, float] = defaultdict(float)

    for rec in cleaned:
        cat = rec.get("category") or "Unknown"
        prod = rec.get("product") or "Unknown"
        tv = to_float(rec.get("total_value"))

        category_totals[cat] += tv
        product_totals[prod] += tv

        # YYYY-MM from timestamp
        try:
            month_key = rec["timestamp"][:7]
        except Exception:
            # Defensive fallback
            month_key = "Unknown"
        monthly_totals[month_key] += tv

    # Top 5 products by total sales value
    top_products = sorted(
        ({"product": p, "total_value": v} for p, v in product_totals.items()),
        key=lambda x: x["total_value"],
        reverse=True,
    )[:5]

    return cleaned, category_totals, top_products, monthly_totals


def write_json(path: str, data: Any):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    args = parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of records")

    cleaned, category_totals, top_products, monthly_totals = process_sales(data)

    # Prepare output paths
    base = args.output_dir.rstrip("/")
    cleaned_path = f"{base}/cleaned_sales.json"
    category_path = f"{base}/category_sales.json"
    top_products_path = f"{base}/top_products.json"
    monthly_path = f"{base}/monthly_sales.json"

    write_json(cleaned_path, cleaned)
    write_json(category_path, category_totals)
    write_json(top_products_path, top_products)
    write_json(monthly_path, monthly_totals)


if __name__ == "__main__":
    main()
