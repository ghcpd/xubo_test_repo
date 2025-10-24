#!/usr/bin/env python3
"""
Sales Data Processing Script

This script processes sales data from a JSON file, performing:
1. Data cleaning (validate price, quantity, timestamp)
2. Data transformation (add total_value field)
3. Data aggregation (category sales, top products, monthly summary)
4. Export results to JSON files
"""

import json
import sys
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any


def clean_price(price: Any) -> float:
    """
    Ensure price is a valid float. If missing or invalid, return 0.0.
    
    Args:
        price: The price value to clean
        
    Returns:
        float: Cleaned price value
    """
    try:
        return float(price)
    except (ValueError, TypeError):
        return 0.0


def clean_quantity(quantity: Any) -> int:
    """
    Ensure quantity is a valid integer. If missing or invalid, return 0.
    
    Args:
        quantity: The quantity value to clean
        
    Returns:
        int: Cleaned quantity value
    """
    try:
        return int(quantity)
    except (ValueError, TypeError):
        return 0


def parse_timestamp(timestamp: Any) -> datetime:
    """
    Convert timestamp into a standard datetime object.
    
    Args:
        timestamp: The timestamp string to parse
        
    Returns:
        datetime: Parsed datetime object
        
    Raises:
        ValueError: If timestamp cannot be parsed
    """
    if not isinstance(timestamp, str):
        raise ValueError("Invalid timestamp format")
    
    # Try ISO format parsing
    try:
        return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        # Fallback to other common formats
        for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
            try:
                return datetime.strptime(timestamp, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse timestamp: {timestamp}")


def clean_data(sales_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Clean the sales data by validating and fixing fields.
    
    Args:
        sales_data: List of sale records
        
    Returns:
        List[Dict[str, Any]]: Cleaned sale records (invalid timestamps removed)
    """
    cleaned = []
    
    for record in sales_data:
        # Try to parse timestamp, skip if invalid
        try:
            timestamp = parse_timestamp(record.get('timestamp'))
        except (ValueError, AttributeError):
            # Skip records with invalid timestamps
            continue
        
        # Create cleaned record
        cleaned_record = {
            'id': record.get('id'),
            'product': record.get('product', ''),
            'category': record.get('category', ''),
            'price': clean_price(record.get('price')),
            'quantity': clean_quantity(record.get('quantity')),
            'timestamp': timestamp.isoformat()
        }
        
        cleaned.append(cleaned_record)
    
    return cleaned


def transform_data(sales_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Add total_value field to each record.
    
    Args:
        sales_data: List of cleaned sale records
        
    Returns:
        List[Dict[str, Any]]: Transformed sale records with total_value
    """
    for record in sales_data:
        record['total_value'] = record['price'] * record['quantity']
    
    return sales_data


def compute_category_sales(sales_data: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Compute total sales per category.
    
    Args:
        sales_data: List of sale records with total_value
        
    Returns:
        Dict[str, float]: Category sales summary
    """
    category_sales = defaultdict(float)
    
    for record in sales_data:
        category = record['category']
        total_value = record['total_value']
        category_sales[category] += total_value
    
    return dict(category_sales)


def compute_top_products(sales_data: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Compute top N products by total sales value.
    
    Args:
        sales_data: List of sale records with total_value
        top_n: Number of top products to return (default: 5)
        
    Returns:
        List[Dict[str, Any]]: Top products sorted by total sales
    """
    product_sales = defaultdict(float)
    
    for record in sales_data:
        product = record['product']
        total_value = record['total_value']
        product_sales[product] += total_value
    
    # Sort by total sales in descending order and take top N
    sorted_products = sorted(
        product_sales.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]
    
    return [
        {'product': product, 'total_sales': total_sales}
        for product, total_sales in sorted_products
    ]


def compute_monthly_sales(sales_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Compute monthly sales summary (group by year-month).
    
    Args:
        sales_data: List of sale records with total_value
        
    Returns:
        List[Dict[str, Any]]: Monthly sales summary sorted by year-month
    """
    monthly_sales = defaultdict(float)
    
    for record in sales_data:
        timestamp = datetime.fromisoformat(record['timestamp'])
        year_month = timestamp.strftime('%Y-%m')
        total_value = record['total_value']
        monthly_sales[year_month] += total_value
    
    # Sort by year-month
    sorted_monthly = sorted(monthly_sales.items())
    
    return [
        {'year_month': year_month, 'total_sales': total_sales}
        for year_month, total_sales in sorted_monthly
    ]


def save_json(data: Any, filename: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        filename: Output filename
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {filename}")


def process_sales_data(input_file: str) -> None:
    """
    Main function to process sales data from input file.
    
    Args:
        input_file: Path to input JSON file
    """
    # Load input data
    print(f"Loading data from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        sales_data = json.load(f)
    
    print(f"Loaded {len(sales_data)} records")
    
    # Step 1: Clean data
    print("Cleaning data...")
    cleaned_data = clean_data(sales_data)
    print(f"Cleaned: {len(cleaned_data)} valid records (removed {len(sales_data) - len(cleaned_data)} invalid)")
    
    # Step 2: Transform data
    print("Transforming data...")
    transformed_data = transform_data(cleaned_data)
    
    # Step 3: Aggregate data
    print("Computing aggregations...")
    category_sales = compute_category_sales(transformed_data)
    top_products = compute_top_products(transformed_data, top_n=5)
    monthly_sales = compute_monthly_sales(transformed_data)
    
    # Step 4: Export results
    print("Exporting results...")
    save_json(transformed_data, 'cleaned_sales.json')
    save_json(category_sales, 'category_sales.json')
    save_json(top_products, 'top_products.json')
    save_json(monthly_sales, 'monthly_sales.json')
    
    print("\nProcessing complete!")
    print(f"  - {len(transformed_data)} records in cleaned_sales.json")
    print(f"  - {len(category_sales)} categories in category_sales.json")
    print(f"  - {len(top_products)} products in top_products.json")
    print(f"  - {len(monthly_sales)} months in monthly_sales.json")


def main():
    """Entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python process_sales_data.py <input_file.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        process_sales_data(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{input_file}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
