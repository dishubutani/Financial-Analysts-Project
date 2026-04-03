import pandas as pd
import numpy as np



# 1. DATA INGESTION & VALIDATION
df = pd.read_csv('European_Bank (1).csv')

print("Dataset Shape:", df.shape)
print("\nColumns:\n", df.columns)

# Validate key fields
required_cols = ['Tenure', 'NumOfProducts', 'IsActiveMember',
                 'Balance', 'CreditScore', 'EstimatedSalary', 'Exited']

for col in required_cols:
    print(f"{col} missing values:", df[col].isnull().sum())

# Check binary consistency
binary_cols = ['IsActiveMember', 'HasCrCard', 'Exited']
for col in binary_cols:
    print(f"\n{col} unique values:", df[col].unique())

# Confirm churn labeling
print("\nChurn Distribution:\n", df['Exited'].value_counts())


# 2. DATA CLEANING & PREPARATION
# Remove irrelevant columns
df.drop(['Surname', 'CustomerId'], axis=1, inplace=True, errors='ignore')

# Handle missing values
df.ffill(inplace=True)

# 3. FEATURE ENGINEERING
# Age Groups
df['AgeGroup'] = pd.cut(df['Age'],
                       bins=[0, 30, 45, 60, 100],
                       labels=['<30', '30-45', '46-60', '60+'])

# Credit Score Bands
df['CreditBand'] = pd.cut(df['CreditScore'],
                         bins=[0, 500, 700, 1000],
                         labels=['Low', 'Medium', 'High'])

# Tenure Groups
df['TenureGroup'] = pd.cut(df['Tenure'],
                          bins=[-1, 3, 7, 20],
                          labels=['New', 'Mid-term', 'Long-term'])

# Balance Segments
df['BalanceSegment'] = pd.cut(df['Balance'],
                             bins=[-1, 1, 100000, 300000],
                             labels=['Zero', 'Low', 'High'])



# 4. CHURN DISTRIBUTION ANALYSIS
# Overall churn rate
overall_churn = df['Exited'].mean()
print("\nOverall Churn Rate:", round(overall_churn, 3))

# Segment-wise churn
def segment_churn(col):
    result = df.groupby(col,observed=False)['Exited'].mean().sort_values(ascending=False)
    print(f"\nChurn Rate by {col}:\n", result)

segment_churn('Geography')
segment_churn('AgeGroup')
segment_churn('CreditBand')
segment_churn('TenureGroup')
segment_churn('BalanceSegment')

# Churn contribution by segment size
segment_size = df.groupby('Geography')['Exited'].agg(['count', 'sum'])
segment_size['Contribution'] = segment_size['sum'] / df['Exited'].sum()
print("\nChurn Contribution by Geography:\n", segment_size)

# Compare churned vs retained
churned = df[df['Exited'] == 1]
retained = df[df['Exited'] == 0]

print("\nAvg Balance (Churned vs Retained):",
      churned['Balance'].mean(), retained['Balance'].mean())



# 5. COMPARATIVE DEMOGRAPHIC ANALYSIS
# Gender churn
gender_churn = df.groupby('Gender')['Exited'].mean()
print("\nGender Churn:\n", gender_churn)

# Geography vs Age interaction
geo_age = df.groupby(['Geography', 'AgeGroup'],observed=False)['Exited'].mean().unstack()
print("\nGeography vs Age Churn:\n", geo_age)

# Financial stability vs churn
financial = df.groupby('Exited')[['Balance', 'EstimatedSalary', 'CreditScore']].mean()
print("\nFinancial Comparison:\n", financial)


# 6. HIGH-VALUE CUSTOMER CHURN ANALYSIS
# High-value customers
high_value = df[df['BalanceSegment'] == 'High']

# High-value churn rate
hv_churn = high_value['Exited'].mean()
print("\nHigh Value Churn Rate:", hv_churn)

# Salary vs Balance
hv_stats = high_value.groupby('Exited')[['Balance', 'EstimatedSalary']].mean()
print("\nHigh Value Stats:\n", hv_stats)

# Revenue at risk
revenue_risk = high_value[high_value['Exited'] == 1]['Balance'].sum()
print("\nRevenue at Risk:", revenue_risk)



# 7. KPI CALCULATIONS
kpis = {}

# Overall Churn Rate
kpis['Overall Churn Rate'] = df['Exited'].mean()

# Segment Churn Rate (example: Geography)
kpis['Segment Churn Rate'] = df.groupby('Geography')['Exited'].mean().to_dict()

# High Value Churn Ratio
kpis['High Value Churn Ratio'] = high_value['Exited'].mean()

# Geographic Risk Index (weighted churn)
geo_risk = df.groupby('Geography')['Exited'].mean() * df['Geography'].value_counts(normalize=True)
kpis['Geographic Risk Index'] = geo_risk.to_dict()

# Engagement Drop Indicator
inactive_churn = df[df['IsActiveMember'] == 0]['Exited'].mean()
active_churn = df[df['IsActiveMember'] == 1]['Exited'].mean()
kpis['Engagement Drop Indicator'] = inactive_churn - active_churn

print("\n--- KPI SUMMARY ---")
for k, v in kpis.items():
    print(f"{k}: {v}")
