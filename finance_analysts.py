import streamlit as st
import pandas as pd
import plotly.express as px

# Step 3: Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("European_Bank (2).csv")
    return df

df = load_data()

# Step 4: Data Cleaning
df = df.drop(columns=["Surname"], errors='ignore')

# Create Age Groups
df['AgeGroup'] = pd.cut(df['Age'], bins=[0,30,45,60,100], labels=["<30","30-45","46-60","60+"])

# Credit Score Segments
df['CreditScoreBand'] = pd.cut(df['CreditScore'], bins=[0,500,700,900], labels=["Low","Medium","High"])

# Balance Segments
df['BalanceSegment'] = pd.cut(df['Balance'], bins=[-1,0,100000,1000000], labels=["Zero","Low","High"])

# Tenure Segments
df['TenureGroup'] = pd.cut(df['Tenure'], bins=[-1,3,7,10], labels=["New","Mid","Long"])

# Step 5: Sidebar Filters
st.sidebar.header("Filters")
geo = st.sidebar.multiselect("Geography", df['Geography'].unique(), default=df['Geography'].unique())
age = st.sidebar.multiselect("Age Group", df['AgeGroup'].unique(), default=df['AgeGroup'].unique())

filtered_df = df[(df['Geography'].isin(geo)) & (df['AgeGroup'].isin(age))]

# Step 6: KPIs
st.title("Customer Churn Dashboard")

total_customers = len(filtered_df)
churn_rate = filtered_df['Exited'].mean() * 100

col1, col2 = st.columns(2)
col1.metric("Total Customers", total_customers)
col2.metric("Churn Rate (%)", round(churn_rate,2))

# Step 7: Geography-wise churn
st.subheader("Geography-wise Churn")
geo_churn = filtered_df.groupby('Geography')['Exited'].mean().reset_index()
fig1 = px.bar(geo_churn, x='Geography', y='Exited', title="Churn Rate by Geography")
st.plotly_chart(fig1)

# Step 8: Age-wise churn
st.subheader("Age Group Churn")
age_churn = filtered_df.groupby('AgeGroup')['Exited'].mean().reset_index()
fig2 = px.bar(age_churn, x='AgeGroup', y='Exited', title="Churn Rate by Age Group")
st.plotly_chart(fig2)

# Step 9: High-value churn
st.subheader("High Balance Customer Churn")
high_value = filtered_df[filtered_df['BalanceSegment'] == 'High']
high_churn = high_value['Exited'].mean() * 100
st.metric("High Value Churn (%)", round(high_churn,2))

# Step 10: Tenure vs churn
st.subheader("Tenure vs Churn")
tenure_churn = filtered_df.groupby('TenureGroup')['Exited'].mean().reset_index()
fig3 = px.line(tenure_churn, x='TenureGroup', y='Exited', title="Churn by Tenure")
st.plotly_chart(fig3)


