import pandas as pd

data = pd.read_csv(
    "news.csv",
)

print(data.head())
print("\nColumns in dataset:")
print(data.columns)
