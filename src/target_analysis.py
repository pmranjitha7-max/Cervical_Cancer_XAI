import pandas as pd

# Load dataset
df = pd.read_csv("dataset/risk_factors_cervical_cancer.csv")

# Replace '?' with missing values
df.replace("?", pd.NA, inplace=True)

print("=" * 50)
print("TARGET VARIABLE ANALYSIS")
print("=" * 50)

print("\nBiopsy Value Counts:")
print(df["Biopsy"].value_counts())

print("\nBiopsy Percentage:")
print(df["Biopsy"].value_counts(normalize=True) * 100)