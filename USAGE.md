# Sales Data Processing Script

## Overview

This Python script processes sales data from a JSON file, performing data cleaning, transformation, aggregation, and exports the results to multiple JSON files.

## Features

### 1. Data Cleaning
- Validates and fixes price values (invalid → 0.0)
- Validates and fixes quantity values (invalid → 0)
- Parses and validates timestamps (removes records with invalid timestamps)

### 2. Data Transformation
- Adds `total_value` field (price × quantity) to each record

### 3. Data Aggregation
- Computes total sales per category
- Identifies top 5 products by total sales value
- Generates monthly sales summary (grouped by year-month)

### 4. Export Results
- `cleaned_sales.json`: All cleaned and transformed records
- `category_sales.json`: Total sales by category
- `top_products.json`: Top 5 products by sales value
- `monthly_sales.json`: Monthly sales summary

## Usage

### Basic Usage

```bash
python3 process_sales_data.py <input_file.json>
```

### Example

```bash
python3 process_sales_data.py sample_sales.json
```

## Input Data Format

The input JSON file should contain an array of sales records with the following structure:

```json
[
  {
    "id": 1,
    "product": "Apple",
    "category": "Fruit",
    "price": 1.5,
    "quantity": 10,
    "timestamp": "2024-01-15T10:30:00"
  }
]
```

### Field Descriptions

- `id` (integer): Unique sale ID
- `product` (string): Product name
- `category` (string): Product category (e.g., Fruit, Electronics, Furniture, Books)
- `price` (float): Unit price
- `quantity` (integer): Quantity sold
- `timestamp` (string): Sale time in ISO format (e.g., "2024-01-15T10:30:00")

## Output Files

### cleaned_sales.json
Contains all valid records with cleaned data and added `total_value` field:

```json
[
  {
    "id": 1,
    "product": "Apple",
    "category": "Fruit",
    "price": 1.5,
    "quantity": 10,
    "timestamp": "2024-01-15T10:30:00",
    "total_value": 15.0
  }
]
```

### category_sales.json
Total sales by category:

```json
{
  "Fruit": 106.5,
  "Electronics": 11399.86,
  "Furniture": 1400.0,
  "Books": 429.90
}
```

### top_products.json
Top 5 products by total sales:

```json
[
  {
    "product": "Laptop",
    "total_sales": 5899.95
  }
]
```

### monthly_sales.json
Monthly sales summary:

```json
[
  {
    "year_month": "2024-01",
    "total_sales": 2782.95
  }
]
```

## Error Handling

- **Invalid price values**: Set to 0.0
- **Invalid quantity values**: Set to 0
- **Invalid timestamps**: Record is removed from the dataset
- **Missing fields**: Set to appropriate defaults (empty string for text, 0/0.0 for numbers)

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Sample Data

A sample input file (`sample_sales.json`) is provided for testing. It contains:
- 18 records (including some with intentionally invalid data)
- Multiple product categories
- Sales across 3 months
- Examples of data quality issues to demonstrate cleaning capabilities

## Testing

Run the script with the sample data:

```bash
python3 process_sales_data.py sample_sales.json
```

Expected output:
- 17 valid records (1 removed due to invalid timestamp)
- 4 product categories
- Top 5 products identified
- 3 months of sales data

## License

This script is provided as-is for data processing purposes.
