import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("sales_data.csv")

# Preprocess
df["Sale_Date"] = pd.to_datetime(df["Sale_Date"])
df["Profit"] = (df["Unit_Price"] - df["Unit_Cost"]) * df["Quantity_Sold"]

# Dashboard title
st.title("📊 Interactive Sales Dashboard (2023)")

# Sidebar filters
st.sidebar.header("🔎 Filters")
region_filter = st.sidebar.multiselect("Select Region", df["Region"].unique())
rep_filter = st.sidebar.multiselect("Select Sales Rep", df["Sales_Rep"].unique())
category_filter = st.sidebar.multiselect("Select Product Category", df["Product_Category"].unique())

# Apply filters
filtered_df = df.copy()
if region_filter:
    filtered_df = filtered_df[filtered_df["Region"].isin(region_filter)]
if rep_filter:
    filtered_df = filtered_df[filtered_df["Sales_Rep"].isin(rep_filter)]
if category_filter:
    filtered_df = filtered_df[filtered_df["Product_Category"].isin(category_filter)]

# KPIs
st.subheader("Key Metrics")
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Revenue", f"${filtered_df['Sales_Amount'].sum():,.0f}")
with col2:
    st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")

# Monthly Sales Trend
st.subheader("📈 Monthly Sales Trend")
monthly_sales = filtered_df.groupby(filtered_df["Sale_Date"].dt.to_period("M"))["Sales_Amount"].sum()
monthly_sales.index = monthly_sales.index.to_timestamp()

fig, ax = plt.subplots()
monthly_sales.plot(kind="line", marker="o", ax=ax, color="green")
ax.set_title("Monthly Sales Trend")
ax.set_ylabel("Revenue")
st.pyplot(fig)

# Sales by Category
st.subheader("📊 Sales by Product Category")
fig, ax = plt.subplots()
filtered_df.groupby("Product_Category")["Sales_Amount"].sum().plot(
    kind="bar", ax=ax, color="skyblue"
)
ax.set_title("Sales by Category")
ax.set_ylabel("Revenue")
st.pyplot(fig)

# Sales by Region
st.subheader("🌍 Sales by Region")
fig, ax = plt.subplots()
filtered_df.groupby("Region")["Sales_Amount"].sum().plot(
    kind="pie", autopct="%1.1f%%", ax=ax, startangle=90
)
ax.set_ylabel("")
ax.set_title("Sales by Region")
st.pyplot(fig)
