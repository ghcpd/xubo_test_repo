#!/usr/bin/env python3
"""
Sales Data Processor

This script cleans, transforms, and analyzes sales data from a JSON file.
It handles data cleaning, transformation, aggregation, and exports results to multiple JSON files.

Usage:
    python sales_data_processor.py <input_file>
    
Output files:
    - cleaned_sales.json: Cleaned and transformed sales data
    - category_sales.json: Total sales per category
    - top_products.json: Top 5 products by total sales value
    - monthly_sales.json: Monthly sales summary
"""

import json
import sys
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any, Optional


class SalesDataProcessor:
    """Processes sales data with cleaning, transformation, and analysis capabilities."""
    
    def __init__(self):
        self.cleaned_data = []
        self.category_sales = {}
        self.top_products = []
        self.monthly_sales = {}
    
    def clean_price(self, price: Any) -> float:
        """Clean and validate price field."""
        try:
            return float(price) if price is not None else 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def clean_quantity(self, quantity: Any) -> int:
        """Clean and validate quantity field."""
        try:
            return int(quantity) if quantity is not None else 0
        except (ValueError, TypeError):
            return 0
    
    def clean_timestamp(self, timestamp: Any) -> Optional[datetime]:
        """Clean and validate timestamp field."""
        if not timestamp:
            return None
        
        try:
            # Try common ISO formats
            for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%SZ', 
                       '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f',
                       '%Y-%m-%dT%H:%M:%S.%fZ']:
                try:
                    return datetime.strptime(str(timestamp), fmt)
                except ValueError:
                    continue
            
            # If none of the formats work, return None (will be filtered out)
            return None
        except Exception:
            return None
    
    def clean_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean the raw sales data according to requirements."""
        cleaned = []
        
        for record in raw_data:
            # Clean individual fields
            price = self.clean_price(record.get('price'))
            quantity = self.clean_quantity(record.get('quantity'))
            timestamp_obj = self.clean_timestamp(record.get('timestamp'))
            
            # Skip records with invalid timestamps
            if timestamp_obj is None:
                continue
            
            # Create cleaned record
            cleaned_record = {
                'id': record.get('id'),
                'product': record.get('product', ''),
                'category': record.get('category', ''),
                'price': price,
                'quantity': quantity,
                'timestamp': record.get('timestamp'),  # Keep original timestamp string
                'datetime': timestamp_obj.isoformat(),  # Add parsed datetime
                'total_value': price * quantity  # Data transformation: add total_value
            }
            
            cleaned.append(cleaned_record)
        
        return cleaned
    
    def aggregate_category_sales(self, data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Compute total sales per category."""
        category_totals = defaultdict(float)
        
        for record in data:
            category = record.get('category', 'Unknown')
            total_value = record.get('total_value', 0.0)
            category_totals[category] += total_value
        
        return dict(category_totals)
    
    def get_top_products(self, data: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """Compute top products by total sales value."""
        product_totals = defaultdict(float)
        
        # Aggregate by product
        for record in data:
            product = record.get('product', 'Unknown')
            total_value = record.get('total_value', 0.0)
            product_totals[product] += total_value
        
        # Sort by total value and get top N
        sorted_products = sorted(product_totals.items(), key=lambda x: x[1], reverse=True)
        
        top_products = []
        for i, (product, total_value) in enumerate(sorted_products[:limit]):
            top_products.append({
                'rank': i + 1,
                'product': product,
                'total_sales': total_value
            })
        
        return top_products
    
    def compute_monthly_sales(self, data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Compute monthly sales summary (group by year-month)."""
        monthly_totals = defaultdict(lambda: {'total_sales': 0.0, 'transaction_count': 0})
        
        for record in data:
            try:
                # Use the parsed datetime
                dt = datetime.fromisoformat(record['datetime'].replace('Z', '+00:00'))
                year_month = dt.strftime('%Y-%m')
                
                monthly_totals[year_month]['total_sales'] += record.get('total_value', 0.0)
                monthly_totals[year_month]['transaction_count'] += 1
            except Exception:
                # Skip records with invalid datetime
                continue
        
        return dict(monthly_totals)
    
    def process_file(self, input_file: str) -> bool:
        """Process the input JSON file and generate all outputs."""
        try:
            # Load raw data
            with open(input_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # Ensure raw_data is a list
            if not isinstance(raw_data, list):
                print(f"Error: Expected a list of records, got {type(raw_data)}")
                return False
            
            print(f"Loaded {len(raw_data)} records from {input_file}")
            
            # Step 1: Clean and transform data
            self.cleaned_data = self.clean_data(raw_data)
            print(f"Cleaned data: {len(self.cleaned_data)} valid records")
            
            # Step 2: Aggregate data
            self.category_sales = self.aggregate_category_sales(self.cleaned_data)
            self.top_products = self.get_top_products(self.cleaned_data)
            self.monthly_sales = self.compute_monthly_sales(self.cleaned_data)
            
            # Step 3: Export results
            self.export_results()
            
            print("Processing completed successfully!")
            return True
            
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in file '{input_file}': {e}")
            return False
        except Exception as e:
            print(f"Error processing file: {e}")
            return False
    
    def export_results(self):
        """Export all results to JSON files."""
        outputs = [
            ('cleaned_sales.json', self.cleaned_data),
            ('category_sales.json', self.category_sales),
            ('top_products.json', self.top_products),
            ('monthly_sales.json', self.monthly_sales)
        ]
        
        for filename, data in outputs:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"Exported {filename}")
            except Exception as e:
                print(f"Error exporting {filename}: {e}")


def main():
    """Main function to run the sales data processor."""
    if len(sys.argv) != 2:
        print("Usage: python sales_data_processor.py <input_file>")
        print("Example: python sales_data_processor.py sales_data.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    processor = SalesDataProcessor()
    
    success = processor.process_file(input_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()