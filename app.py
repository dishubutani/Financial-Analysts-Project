import pandas as pd
import streamlit as st

# Load data
df = pd.read_csv("European_Bank (1).csv")

df = df.drop(columns=["Surname"], errors='ignore')

# Feature engineering
df['AgeGroup'] = pd.cut(df['Age'], bins=[0,30,45,60,100],
                        labels=['<30','30-45','46-60','60+'])

# Title
st.title("📊 Customer Churn Dashboard")

# -----------------------------
# Filters
# -----------------------------
geo = st.selectbox("Select Geography", df['Geography'].unique())

filtered_df = df[df['Geography'] == geo]

# -----------------------------
# KPIs
# -----------------------------
churn_rate = filtered_df['Exited'].mean() * 100

st.metric("Churn Rate (%)", f"{churn_rate:.2f}")

# -----------------------------
# Charts
# -----------------------------
st.subheader("Churn by Age Group")
st.bar_chart(filtered_df.groupby('AgeGroup', observed=False)['Exited'].mean())

st.subheader("Churn by Tenure")
st.bar_chart(filtered_df.groupby('Tenure')['Exited'].mean())

# -----------------------------
# High Value Customers
# -----------------------------
st.subheader("High Value Customers (Balance > 100K)")
hv = filtered_df[filtered_df['Balance'] > 100000]

st.write(hv[['Balance','EstimatedSalary','Exited']].head())
