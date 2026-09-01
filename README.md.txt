# Python Retail Revenue Analysis

Automated Python & Jupyter ETL pipeline using Pandas to clean transactional retail datasets, process discounts and returns, and calculate net revenue aggregations.

## Features

- **Schema Normalization**: Strips spaces and standardizes header casing across all incoming datasets.
- **Data Hygiene**: Removes missing date values, returns (`returned == 0`), negative quantities, and placeholder categories (`???`).
- **Revenue Calculation**: Derives true net revenue using product list price, purchase quantity, and discount percentages.
- **Aggregation Engine**: Groups revenue trends by year-month periods and calculates customer lifetime value metrics.

## File Structure

```text
.
├── customer_data.csv       # Customer demographic master records
├── product_data.csv        # Product catalog & pricing data
├── store_data.csv          # Store location master table
├── sales_datas.csv         # Raw sales transactions log
├── main.py                 # Core ETL processing script
└── README.md               # Project documentation