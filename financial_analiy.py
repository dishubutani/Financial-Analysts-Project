import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_csv("European_Bank (1).csv")

# Preview
print(df.head())

# -----------------------------
# Data Cleaning
# -----------------------------
df = df.drop(columns=["Surname"], errors='ignore')

# -----------------------------
# Feature Engineering
# -----------------------------

# Age Groups
df['AgeGroup'] = pd.cut(df['Age'],
                       bins=[0, 30, 45, 60, 100],
                       labels=['<30', '30-45', '46-60', '60+'])

# Credit Score Bands
df['CreditBand'] = pd.cut(df['CreditScore'],
                         bins=[0,500,700,900],
                         labels=['Low','Medium','High'])

# Tenure Groups
df['TenureGroup'] = pd.cut(df['Tenure'],
                          bins=[-1,3,7,10],
                          labels=['New','Mid','Long'])

# Balance Segments
df['BalanceGroup'] = pd.cut(df['Balance'],
                           bins=[-1,0,100000,300000],
                           labels=['Zero','Low','High'])

# -----------------------------
# KPI Calculations
# -----------------------------

# Overall churn rate
churn_rate = df['Exited'].mean() * 100
print(f"\nOverall Churn Rate: {churn_rate:.2f}%")

# Segment churn
print("\nChurn by Geography:")
print(df.groupby('Geography')['Exited'].mean()*100)

print("\nChurn by Age Group:")
df.groupby('AgeGroup', observed=False)['Exited'].mean()*100

print("\nChurn by Credit Band:")
print(df.groupby('CreditBand')['Exited'].mean()*100)

# High-value churn
high_value = df[df['Balance'] > 100000]
hv_churn = high_value['Exited'].mean()*100
print(f"\nHigh Value Customer Churn: {hv_churn:.2f}%")
