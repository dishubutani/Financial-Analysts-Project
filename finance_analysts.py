import pandas as pd
import matplotlib.pyplot as plt

# 1. Load Data
df = pd.read_csv("European_Bank.csv")

# 2. Basic Info
print("Dataset Shape:", df.shape)
print("\nFirst 5 rows:\n", df.head())

# 3. Overall Churn Rate
churn_rate = df["Exited"].mean() * 100
print(f"\nOverall Churn Rate: {churn_rate:.2f}%")

# 4. Geography-wise Churn
geo_churn = df.groupby("Geography")["Exited"].mean() * 100
print("\nChurn by Geography:\n", geo_churn)

# 5. Age Segmentation
def age_group(age):
    if age < 30:
        return "<30"
    elif age <= 45:
        return "30-45"
    elif age <= 60:
        return "46-60"
    else:
        return "60+"

df["AgeGroup"] = df["Age"].apply(age_group)

age_churn = df.groupby("AgeGroup")["Exited"].mean() * 100
print("\nChurn by Age Group:\n", age_churn)

# 6. High Value Customers
df["HighValue"] = df["Balance"] > 100000

high_value_churn = df[df["HighValue"]]["Exited"].mean() * 100
print(f"\nHigh Value Customer Churn Rate: {high_value_churn:.2f}%")

# 7. Credit Score Segmentation
def credit_group(score):
    if score < 500:
        return "Low"
    elif score < 700:
        return "Medium"
    else:
        return "High"

df["CreditGroup"] = df["CreditScore"].apply(credit_group)

credit_churn = df.groupby("CreditGroup")["Exited"].mean() * 100
print("\nChurn by Credit Score:\n", credit_churn)

# 8. Activity Analysis
activity_churn = df.groupby("IsActiveMember")["Exited"].mean() * 100
print("\nChurn by Activity:\n", activity_churn)

# 9. Visualization

# Geography Bar Chart
geo_churn.plot(kind="bar")
plt.title("Churn Rate by Geography")
plt.ylabel("Churn %")
plt.show()

# Age Group Chart
age_churn.plot(kind="bar")
plt.title("Churn Rate by Age Group")
plt.ylabel("Churn %")
plt.show()

# Pie Chart (Churn vs Retained)
df["Exited"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Churn vs Retained")
plt.ylabel("")
plt.show()
