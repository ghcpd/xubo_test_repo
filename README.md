# xubo_test_repo

## Sales Data Processing Script

This repository contains a Python script that cleans, transforms, and analyzes sales data from JSON files.

### Quick Start

```bash
python3 process_sales_data.py sample_sales.json
```

This will generate four output files:
- `cleaned_sales.json` - Cleaned and transformed sales records
- `category_sales.json` - Total sales by category
- `top_products.json` - Top 5 products by sales value
- `monthly_sales.json` - Monthly sales summary

### Features

✓ **Data Cleaning**: Validates prices, quantities, and timestamps  
✓ **Data Transformation**: Adds calculated `total_value` field  
✓ **Data Aggregation**: Category sales, top products, monthly summaries  
✓ **Robust Error Handling**: Invalid data is cleaned or removed appropriately  

### Documentation

See [USAGE.md](USAGE.md) for detailed documentation and examples.

### Files

- `process_sales_data.py` - Main processing script
- `sample_sales.json` - Sample input data for testing
- `USAGE.md` - Detailed usage documentation