from tests.sample_data import (generate_sample_dataframe)
df = generate_sample_dataframe(number_of_records=20,seed=42)

print("\n=== SYNTHETIC DATASET ===")
print(df.head(2).to_string(index=False))

print("\n=== DATASET SHAPE ===")
print(df.shape)


print("\n=== STOCK STATUS DISTRIBUTION ===")
print(
    df["stock_status"]
    .value_counts(dropna=False)
)

for _, row in df.iterrows():

    mos = row["months_of_stock"]
    status = row["stock_status"]

    if status == "Stockout":
        assert mos == 0

    elif status == "Critical":
        assert 0 < mos <= 1

    elif status == "Low":
        assert 1 < mos < 3

    elif status == "Adequate":
        assert 3 <= mos <= 5

    elif status == "Overstock":
        assert mos > 5

    elif status == "Unknown":
        assert mos != mos  # pandas NaN


print(
    "\nSUPPLY CHAIN BUSINESS RULES PASSED"
)