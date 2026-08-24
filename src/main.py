import pandas as pd

# Load dataset
df = pd.read_csv("dataset/risk_factors_cervical_cancer.csv")

# Display information
print("Dataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())