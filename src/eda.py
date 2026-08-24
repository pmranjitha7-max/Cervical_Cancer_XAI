import pandas as pd

# ============================================================
# EXPLORATORY DATA ANALYSIS (EDA)
# Project: XAI Automated Classification of Cervical Cancer
# ============================================================

# Load Dataset
df = pd.read_csv("dataset/risk_factors_cervical_cancer.csv")

# Replace '?' with missing values
df.replace("?", pd.NA, inplace=True)

print("=" * 70)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 70)

# ============================================================
# 1. Dataset Shape
# ============================================================
print("\n1. DATASET SHAPE")
print(df.shape)

# ============================================================
# 2. Column Names
# ============================================================
print("\n2. COLUMN NAMES")
print(df.columns.tolist())

# ============================================================
# 3. Data Types
# ============================================================
print("\n3. DATA TYPES")
print(df.dtypes)

# ============================================================
# 4. Missing Values
# ============================================================
print("\n4. MISSING VALUES")
print(df.isnull().sum())

print("\nTotal Missing Values:")
print(df.isnull().sum().sum())

# ============================================================
# 5. Basic Statistics
# ============================================================
print("\n5. BASIC STATISTICS")
print(df.describe(include="all"))

# ============================================================
# 6. First Five Records
# ============================================================
print("\n6. FIRST FIVE RECORDS")
print(df.head())

print("\n")
print("=" * 70)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 70)