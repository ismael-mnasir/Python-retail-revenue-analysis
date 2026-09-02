"""
Retail Sales Data Pipeline & Visualizations
Cleans, transforms, and aggregates retail sales transactions using Pandas,
and exports publication-ready data visualizations using Seaborn.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_datasets():
    """Load raw CSV files into DataFrames."""
    df_customer = pd.read_csv("customer_data.csv")
    df_product = pd.read_csv("product_data.csv")
    df_store = pd.read_csv("store_data.csv")
    df_sales = pd.read_csv("sales_datas.csv")
    return df_customer, df_product, df_store, df_sales


def clean_columns(df):
    """Standardize column headers to clean snake_case format."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def clean_and_transform(df_customer, df_product, df_store, df_sales):
    """Clean datasets, merge sales with product catalog, and calculate net revenue."""
    # Standardize column headers
    df_customer = clean_columns(df_customer)
    df_product = clean_columns(df_product)
    df_store = clean_columns(df_store)
    df_sales = clean_columns(df_sales)

    # Parse dates
    df_sales["date"] = pd.to_datetime(df_sales["date"], errors="coerce")
    df_sales["year_month"] = df_sales["date"].dt.to_period("M")

    # Clean sales records
    df_sales["discount"] = df_sales["discount"].fillna(0)
    df_sales_clean = df_sales.dropna(
        subset=["customer_id", "product_id", "date"]
    ).copy()
    df_sales_clean = df_sales_clean[
        (df_sales_clean["returned"] == 0) & (df_sales_clean["quantity"] > 0)
    ]

    # Clean catalog placeholders
    df_product_clean = df_product[
        (df_product["category"] != "???") & (df_product["list_price"] > 0)
    ].copy()

    # Merge sales with product catalog
    df_merged = pd.merge(
        df_sales_clean,
        df_product_clean[["product_id", "category", "list_price"]],
        on="product_id",
        how="inner",
    )

    # Calculate Net Revenue: Quantity * List Price * (1 - Discount)
    df_merged["net_revenue"] = (
        df_merged["quantity"]
        * df_merged["list_price"]
        * (1 - df_merged["discount"])
    )

    return df_merged


def calculate_aggregations(df_merged):
    """Aggregate net revenue across different analytical dimensions."""
    monthly_revenue = (
        df_merged.groupby("year_month")["net_revenue"].sum().reset_index()
    )
    customer_revenue = (
        df_merged.groupby("customer_id")["net_revenue"].sum().reset_index()
    )
    category_revenue = (
        df_merged.groupby("category")["net_revenue"].sum().reset_index()
    )
    store_revenue = (
        df_merged.groupby("store_id")["net_revenue"].sum().reset_index()
    )

    return monthly_revenue, customer_revenue, category_revenue, store_revenue


def generate_visualizations(
    df_merged, monthly_revenue, customer_revenue, category_revenue, store_revenue
):
    """Generate and save publication-quality visualization charts."""
    sns.set_theme(style="whitegrid")

    # 1. Monthly Revenue Trend Line Chart
    plt.figure(figsize=(12, 5))
    monthly_revenue["month_str"] = monthly_revenue["year_month"].astype(str)
    ax1 = sns.lineplot(
        data=monthly_revenue,
        x="month_str",
        y="net_revenue",
        marker="o",
        color="#1f77b4",
        linewidth=2.5,
    )
    plt.title("Total Monthly Net Revenue Trend", fontweight="bold", fontsize=14)
    plt.xlabel("Year-Month", fontweight="bold")
    plt.ylabel("Revenue ($)", fontweight="bold")
    for i, label in enumerate(ax1.get_xticklabels()):
        if i % 3 != 0:
            label.set_visible(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("monthly_revenue_trend.png")
    plt.close()

    # 2. Top 5 Customers Bar Chart
    plt.figure(figsize=(8, 5))
    top_5_cust = customer_revenue.sort_values(
        by="net_revenue", ascending=False
    ).head(5)
    ax2 = sns.barplot(
        data=top_5_cust, x="customer_id", y="net_revenue", palette="Blues_r"
    )
    plt.title("Top 5 Customers by Revenue", fontweight="bold", fontsize=14)
    plt.xlabel("Customer ID", fontweight="bold")
    plt.ylabel("Revenue ($)", fontweight="bold")
    for p in ax2.patches:
        ax2.annotate(
            f"${p.get_height():,.2f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(0, 6),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
        )
    plt.tight_layout()
    plt.savefig("top_customers.png")
    plt.close()

    # 3. Revenue by Product Category
    plt.figure(figsize=(9, 4.5))
    top_cats = category_revenue.sort_values(by="net_revenue", ascending=False)
    ax3 = sns.barplot(
        data=top_cats, x="net_revenue", y="category", palette="Blues_r"
    )
    plt.title("Total Revenue by Product Category", fontweight="bold", fontsize=14)
    plt.xlabel("Revenue ($)", fontweight="bold")
    plt.ylabel("Category", fontweight="bold")
    for p in ax3.patches:
        width = p.get_width()
        ax3.annotate(
            f"${width:,.0f}",
            (width, p.get_y() + p.get_height() / 2.0),
            ha="left",
            va="center",
            xytext=(5, 0),
            textcoords="offset points",
            fontsize=9,
        )
    plt.tight_layout()
    plt.savefig("category_revenue.png")
    plt.close()

    # 4. Revenue Distribution Across Discount Levels (Box Plot)
    plt.figure(figsize=(8, 4.5))
    sns.boxplot(data=df_merged, x="discount", y="net_revenue", palette="Set2")
    plt.title(
        "Transaction Revenue Across Discount Levels",
        fontweight="bold",
        fontsize=14,
    )
    plt.xlabel("Discount Rate", fontweight="bold")
    plt.ylabel("Revenue ($)", fontweight="bold")
    plt.tight_layout()
    plt.savefig("discount_impact.png")
    plt.close()

    print(
        "All 4 visualizations generated and saved successfully!"
    )


if __name__ == "__main__":
    df_cust, df_prod, df_st, df_sl = load_datasets()
    df_transformed = clean_and_transform(df_cust, df_prod, df_st, df_sl)
    monthly, customer, category, store = calculate_aggregations(df_transformed)

    print("=== Pipeline Summary ===")
    print(f"Total Transactions Processed: {len(df_transformed):,}")
    print(f"Total Net Revenue Generated: ${df_transformed['net_revenue'].sum():,.2f}\n")

    generate_visualizations(df_transformed, monthly, customer, category, store)