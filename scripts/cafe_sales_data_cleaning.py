import pandas as pd

df = pd.read_csv("dirty_cafe_sales.csv")

print("Before:", df.columns.tolist())

df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_"))

print("After:", df.columns.tolist())

import numpy as np
print(df.isna().sum())
placeholders = ["UNKNOWN", "Unknown", "unknown", "ERROR", "Error", "error", ""]
df = df.replace(placeholders, np.nan)
print(df.isna().sum())

print(df[["item", "payment_method", "location"]].isna().sum())

item_mode = df["item"].mode(dropna=True)[0]     
df["item"] = df["item"].fillna(item_mode)

df["payment_method"] = df["payment_method"].fillna("unknown")
df["location"] = df["location"].fillna("unknown")

print(item_mode)
print(df[["item", "payment_method", "location"]].isna().sum())

numeric_cols = ["quantity", "price_per_unit", "total_spent"]

print(df[numeric_cols].isna().sum())

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print(df[numeric_cols].dtypes)
print(df[numeric_cols].isna().sum())

for col in numeric_cols:
    median_val = df[col].median()
    df[col] = df[col].fillna(median_val)
    print(f"Filled {col} NaNs with median =", median_val)

print(df[numeric_cols].isna().sum())

df["expected_total_spent"] = df["quantity"] * df["price_per_unit"]

df["is_total_spent_valid"] = (
    df["total_spent"].round(2) == df["expected_total_spent"].round(2)
)

invalid_count = (df["is_total_spent_valid"]).sum()
print(invalid_count)
print(df.loc[~df["is_total_spent_valid"],
             ["transaction_id", "quantity", "price_per_unit", "total_spent", "expected_total_spent"]].head(10)
)

df.loc[df["is_total_spent_valid"], "total_spent"] = df.loc[df["is_total_spent_valid"], "expected_total_spent"]

df["is_total_spent_valid_after_fix"] = (
    df["total_spent"].round(2) == df["expected_total_spent"].round(2)
)

print((df["is_total_spent_valid_after_fix"]).sum())

print(df["transaction_date"].isna().sum())

df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

print(df["transaction_date"].isna().sum())

date_mode = df["transaction_date"].mode(dropna=True)[0]
df["transaction_date"] = df["transaction_date"].fillna(date_mode)

print(date_mode)
print(df["transaction_date"].isna().sum())
print(df["transaction_date"].min(), "to", df["transaction_date"].max())

full_dup_count = df.duplicated().sum()
print(full_dup_count)

df = df.drop_duplicates()
print(df.shape)

txn_dup_count = df["transaction_id"].duplicated().sum()
print(txn_dup_count)

df = df.drop_duplicates(subset=["transaction_id"], keep="first")
print(df.shape)

print(df.shape)

print(df.isna().sum())

final_invalid = (df["total_spent"].round(2) != df["expected_total_spent"].round(2)).sum()
print(final_invalid)

neg_qty = (df["quantity"] < 0).sum()
neg_price = (df["price_per_unit"] < 0).sum()
neg_total = (df["total_spent"] < 0).sum()
print(neg_qty,neg_price,neg_total)

df_export = df.drop(columns=["expected_total_spent"])

df_export.to_csv(index=False)
print("cleaned_cafe_sales.csv")


import matplotlib.pyplot as plt

item_sales = df.groupby("item")["total_spent"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
item_sales.plot(kind="bar")
plt.title("Total Sales (Total Spent) by Item")
plt.xlabel("Item")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Line Chart: Monthly total sales trend
df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
df["month"] = df["transaction_date"].dt.to_period("M").astype(str)

monthly_sales = df.groupby("month")["total_spent"].sum().sort_index()

plt.figure(figsize=(10, 5))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o")
plt.title("Monthly Total Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales (Total Spent)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
plt.hist(df["total_spent"], bins=30)
plt.title("Distribution of Total Spent")
plt.xlabel("Total Spent")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 2.5))
plt.boxplot(df["total_spent"], vert=False)
plt.title("Outliers in Total Spent (Box Plot)")
plt.xlabel("Total Spent")
plt.tight_layout()
plt.show()

import seaborn as sns
numeric_df = df[["quantity", "price_per_unit", "total_spent"]]

plt.figure(figsize=(6, 4))
sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap (Numeric Variables)")
plt.tight_layout()
plt.show()
