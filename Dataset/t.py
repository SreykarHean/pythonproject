import pandas as pd

files = [
    "nike_data_2022_09.csv",
    "restaurant_sales_malaysian_data.csv",
    "starbucks_drinks.csv",
    "skincare.csv"
]

for file in files:
    df = pd.read_csv(file)
    df_trimmed = df.head(300)
    df_trimmed.to_csv(f"trimmed_{file}", index=False)
    print(f"{file}: {len(df)} rows → {len(df_trimmed)} rows saved as trimmed_{file}")