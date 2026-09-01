"""
Retail Sales Data Pipeline
Clean, transform, and aggregate retail sales transactions using Pandas.
"""

import numpy as np
import pandas as pd


def load_datasets():
    """Load raw CSV files into DataFrames."""
    df_customer = pd.read_csv("customer_data.csv")
    df_product = pd.read_csv("product_data.csv")
    df_store = pd.read_csv("store_data.csv")
    df_sales = pd.read_csv("sales_datas.csv")
    return df_customer, df_product, df_store, df_sales


def clean_and_transform(df_customer, df_product, df_store, df_sales):
    """Normalize headers, filter invalid records, and compute net revenue."""
    # Standardize column headers across datasets
    for df in [df_customer, df_product, df_store, df_sales]:
        df.columns = df.columns.str.strip().str.lower()

    # Parse date strings to datetime and extract year-month period
    df_sales["date"] = pd.to_datetime(df_sales["date"], errors="coerce")
    df_sales["year_month"] = df_sales["date"].dt.to_period("M")

    # Clean catalog placeholders
    df_product_clean = df_product[df_product["category"] != "???"].copy()

    # Filter out returns and invalid transaction quantities
    df_sales_clean = df_sales[
        (df_sales["returned"] == 0) & (df_sales["quantity"] > 0)
    ].copy()

    # Merge sales with product catalog
    df_merged = pd.merge(
        df_sales_clean,
        df_product_clean[["product_id", "list_price"]],
        on="product_id",
        how="inner",
    )

    # Calculate net revenue formula: list_price * quantity * (1 - discount)
    df_merged["net_revenue"] = (
        df_merged["list_price"]
        * df_merged["quantity"]
        * (1 - df_merged["discount"])
    )

    return df_merged


def calculate_aggregations(df_merged):
    """Aggregate net revenue by month and customer ID."""
    monthly_revenue = (
        df_merged.groupby("year_month")["net_revenue"].sum().reset_index()
    )
    customer_revenue = (
        df_merged.groupby("customer_id")["net_revenue"].sum().reset_index()
    )
    return monthly_revenue, customer_revenue


if __name__ == "__main__":
    # Execute ETL steps
    df_cust, df_prod, df_st, df_sl = load_datasets()
    df_transformed = clean_and_transform(df_cust, df_prod, df_st, df_sl)
    monthly_summary, customer_summary = calculate_aggregations(df_transformed)

    # Display results
    print("=== Monthly Revenue Summary ===")
    print(monthly_summary.head())

    print("\n=== Top 5 Customers by Revenue ===")
    print(
        customer_summary.sort_values(by="net_revenue", ascending=False).head()
    )