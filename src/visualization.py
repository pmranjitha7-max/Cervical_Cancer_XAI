import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# DATA VISUALIZATION
# Project: XAI Automated Classification of Cervical Cancer
# ============================================================

# Load Cleaned Dataset
df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

print("=" * 70)
print("DATA VISUALIZATION")
print("=" * 70)

# ============================================================
# Visualization 1 : Age Distribution
# ============================================================

plt.figure(figsize=(8,5))

plt.hist(df["Age"], bins=15)

plt.title("Age Distribution of Patients")
plt.xlabel("Age")
plt.ylabel("Number of Patients")

plt.show()
# ============================================================
# Visualization 2 : Target Variable Distribution (Biopsy)
# ============================================================

plt.figure(figsize=(6,4))

df["Biopsy"].value_counts().plot(kind="bar")

plt.title("Biopsy Class Distribution")
plt.xlabel("Biopsy")
plt.ylabel("Number of Patients")

plt.show()