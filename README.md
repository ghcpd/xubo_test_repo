# xubo_test_repo

## Sales Data Processor

This repository contains a Python script to clean, transform, and analyze sales data from JSON files.

### Usage

```bash
python3 sales_data_processor.py <input_file.json>
```

Example:
```bash
python3 sales_data_processor.py sample_sales_data.json
```

### Features

1. **Data Cleaning**
   - Validates and converts price values to floats (invalid → 0.0)
   - Validates and converts quantity values to integers (invalid → 0)
   - Parses timestamps and removes records with invalid timestamps

2. **Data Transformation**
   - Adds `total_value` field calculated as `price × quantity`

3. **Data Aggregation**
   - Computes total sales per category
   - Identifies top 5 products by total sales value
   - Generates monthly sales summary (grouped by year-month)

4. **Export Results**
   - `cleaned_sales.json`: Cleaned and transformed sales data
   - `category_sales.json`: Total sales per category
   - `top_products.json`: Top 5 products by total sales value
   - `monthly_sales.json`: Monthly sales summary

### Sample Data Format

The input JSON should contain an array of sales records with the following structure:

```json
[
  {
    "id": 1,
    "product": "Product Name",
    "category": "Category Name",
    "price": 99.99,
    "quantity": 2,
    "timestamp": "2023-01-15T10:30:00"
  }
]
```

### Error Handling

- Invalid timestamps: Records are excluded from output
- Invalid prices: Converted to 0.0
- Invalid quantities: Converted to 0
- Missing values: Handled gracefully with default values