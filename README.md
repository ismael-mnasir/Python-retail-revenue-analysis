# Python Retail Sales Revenue Analysis & ETL Pipeline

An end-to-end Python data engineering and exploratory data analysis (EDA) pipeline that cleans, transforms, merges, and aggregates retail sales transaction datasets, producing business insights and key visualizations.

---

## 📌 Project Overview

This project ingests raw transactional CSV data across sales, customer profiles, product catalogs, and store locations. It cleans invalid and duplicate entries, standardizes column headers, merges datasets, computes transaction-level net revenue after discounts, and outputs key analytical visualizations.

---

## 🛠️ Data Pipeline Architecture & ETL Steps

1. **Data Ingestion**: Loads four core CSV tables (`sales_datas.csv`, `product_data.csv`, `customer_data.csv`, `store_data.csv`).
2. **Standardization**: Converts all column headers to uniform `snake_case`.
3. **Data Cleaning**:
   * Drops incomplete transactions missing key IDs or dates.
   * Filters out returned orders (`returned == 0`) and zero/negative quantities.
   * Removes placeholder categories (`???`) and zero-value list prices in the catalog.
   * Imputes missing discount rates to zero.
4. **Calculated Metric**: Computes net revenue per transaction:
   $$\text{Net Revenue} = \text{Quantity} \times \text{List Price} \times (1 - \text{Discount})$$
5. **Aggregation & Visualization**: Outputs summary reports and exports Seaborn chart figures.

---

## 📊 Key Visualizations

The pipeline automatically generates four image artifacts:

* **`monthly_revenue_trend.png`**: Line plot showcasing net revenue performance over time with adjusted x-axis tick frequency to avoid overlap.
* **`top_customers.png`**: Bar chart detailing the top 5 revenue-generating customer IDs annotated with exact dollar totals.
* **`category_revenue.png`**: Horizontal bar chart highlighting revenue share across product categories.
* **`discount_impact.png`**: Box plot examining transaction revenue distribution across different discount levels.

---

## 🚀 How to Run

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/ismael-mnasir/Python-retail-revenue-analysis.git](https://github.com/ismael-mnasir/Python-retail-revenue-analysis.git)
   cd Python-retail-revenue-analysis
   ```

2. **Install required dependencies**:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```

3. **Execute the pipeline**:
   ```bash
   python main.py
   ```