import pandas as pd

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_cervical_cancer.csv")

print("=" * 60)
print("HPV TARGET ANALYSIS")
print("=" * 60)

targets = ["STDs:HPV", "Dx:HPV"]

for target in targets:
    print(f"\nTarget Column: {target}")
    print("-" * 40)

    print("Value Counts:")
    print(df[target].value_counts())

    print("\nPercentage:")
    print(df[target].value_counts(normalize=True) * 100)

    print("\nMissing Values:")
    print(df[target].isnull().sum())

print("\n" + "=" * 60)