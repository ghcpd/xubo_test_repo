# xubo_test_repo

This repository includes a simple Python script to clean, transform, and analyze sales data from a JSON file.

Usage:
- Ensure you have Python 3 installed.
- Prepare an input JSON file that contains a list of sales records.

Run the script:

```
python3 sales_processor.py <input_json_path> --output-dir .
```

Outputs:
- cleaned_sales.json: Cleaned dataset with total_value per record.
- category_sales.json: Total sales aggregated by category.
- top_products.json: Top 5 products by total sales value.
- monthly_sales.json: Monthly sales summary grouped by YYYY-MM.
