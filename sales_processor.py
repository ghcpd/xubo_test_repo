#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def parse_iso_timestamp(ts: str):
    if not isinstance(ts, str):
        return None
    # Handle 'Z' timezone
    candidate = ts.strip()
    try:
        if candidate.endswith('Z'):
            candidate = candidate[:-1] + '+00:00'
        return datetime.fromisoformat(candidate)
    except Exception:
        pass
    # Fallback common formats
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(candidate, fmt)
        except Exception:
            continue
    return None


def clean_record(rec: dict):
    cleaned = dict(rec)
    # price
    try:
        cleaned['price'] = float(cleaned.get('price', 0.0))
    except Exception:
        cleaned['price'] = 0.0
    # quantity
    try:
        cleaned['quantity'] = int(cleaned.get('quantity', 0))
    except Exception:
        cleaned['quantity'] = 0
    # timestamp
    ts = parse_iso_timestamp(cleaned.get('timestamp'))
    if ts is None:
        return None
    cleaned['timestamp'] = ts.isoformat()
    # derived
    cleaned['total_value'] = cleaned['price'] * cleaned['quantity']
    # normalise missing text fields for grouping
    if not cleaned.get('category'):
        cleaned['category'] = 'Unknown'
    if not cleaned.get('product'):
        cleaned['product'] = 'Unknown'
    return cleaned


def process(input_path: Path, out_dir: Path):
    data = json.loads(Path(input_path).read_text())
    if not isinstance(data, list):
        raise ValueError('Input JSON must be a list of sale records')

    cleaned_records = []
    for rec in data:
        if not isinstance(rec, dict):
            continue
        c = clean_record(rec)
        if c is not None:
            cleaned_records.append(c)

    # Aggregations
    category_sales = defaultdict(float)
    product_sales = defaultdict(float)
    monthly_sales = defaultdict(float)

    for r in cleaned_records:
        category_sales[r['category']] += r['total_value']
        product_sales[r['product']] += r['total_value']
        dt = datetime.fromisoformat(r['timestamp'])
        key = f"{dt.year:04d}-{dt.month:02d}"
        monthly_sales[key] += r['total_value']

    # Prepare outputs
    category_sales_list = [
        {'category': k, 'total_sales': round(v, 2)} for k, v in category_sales.items()
    ]
    category_sales_list.sort(key=lambda x: (-x['total_sales'], x['category']))

    top_products_list = [
        {'product': k, 'total_sales': round(v, 2)} for k, v in product_sales.items()
    ]
    top_products_list.sort(key=lambda x: -x['total_sales'])
    top_products_list = top_products_list[:5]

    monthly_sales_list = [
        {'month': k, 'total_sales': round(v, 2)} for k, v in monthly_sales.items()
    ]
    monthly_sales_list.sort(key=lambda x: x['month'])

    # Write outputs
    (out_dir / 'cleaned_sales.json').write_text(json.dumps(cleaned_records, indent=2))
    (out_dir / 'category_sales.json').write_text(json.dumps(category_sales_list, indent=2))
    (out_dir / 'top_products.json').write_text(json.dumps(top_products_list, indent=2))
    (out_dir / 'monthly_sales.json').write_text(json.dumps(monthly_sales_list, indent=2))


def main(argv):
    if len(argv) < 2:
        print('Usage: python sales_processor.py <input_json> [output_dir]')
        return 1
    in_path = Path(argv[1])
    if not in_path.exists():
        print(f'Input file not found: {in_path}')
        return 1
    out_dir = Path(argv[2]) if len(argv) > 2 else in_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    process(in_path, out_dir)
    print(f'Processed {in_path} -> outputs in {out_dir}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
