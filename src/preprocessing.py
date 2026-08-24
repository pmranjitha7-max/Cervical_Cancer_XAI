import pandas as pd

# ============================================================
# DATA PREPROCESSING
# Project: XAI Automated Classification of Cervical Cancer
# ============================================================

# Load Dataset
df = pd.read_csv("dataset/risk_factors_cervical_cancer.csv")

print("=" * 70)
print("DATA PREPROCESSING")
print("=" * 70)

# ------------------------------------------------------------
# Step 1 : Replace '?' with missing values
# ------------------------------------------------------------
df.replace("?", pd.NA, inplace=True)

print("\nStep 1 Completed")
print("'?' replaced with missing values.")

# ------------------------------------------------------------
# Step 2 : Display dataset information
# ------------------------------------------------------------
print("\nDataset Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum().sum())
# ------------------------------------------------------------
# Step 2 : Convert all columns to numeric
# ------------------------------------------------------------

print("\nConverting columns to numeric...")

for column in df.columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

print("Step 2 Completed")

print("\nData Types After Conversion:")
print(df.dtypes)
# ------------------------------------------------------------
# Step 3 : Drop columns with too many missing values
# ------------------------------------------------------------

print("\nDropping columns with excessive missing values...")

columns_to_drop = [
    "STDs: Time since first diagnosis",
    "STDs: Time since last diagnosis"
]

df.drop(columns=columns_to_drop, inplace=True)

print("Step 3 Completed")
print("\nDataset Shape After Dropping Columns:")
print(df.shape)


# ------------------------------------------------------------
# Step 4 : Fill missing values
# ------------------------------------------------------------

print("\nFilling missing values with median...")

for column in df.columns:
    if df[column].isnull().sum() > 0:
        df[column] = df[column].fillna(df[column].median())

print("Step 4 Completed")

print("\nRemaining Missing Values:")
print(df.isnull().sum().sum())


# ------------------------------------------------------------
# Step 5 : Save cleaned dataset
# ------------------------------------------------------------

df.to_csv("dataset/cleaned_cervical_cancer.csv", index=False)

print("\nCleaned dataset saved successfully!")
print("Location: dataset/cleaned_cervical_cancer.csv")