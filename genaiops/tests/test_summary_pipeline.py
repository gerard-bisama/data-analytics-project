from tests.sample_data import (
    generate_sample_dataframe
)

from src.processing.dataframe_summary import (
    summarize_prediction_dataframe
)


df = generate_sample_dataframe(
    number_of_records=20,
    seed=42
)

summary = summarize_prediction_dataframe(df)


# -----------------------------------
# Test 1: Number of records
# -----------------------------------

assert summary["records_analyzed"] == 20


# -----------------------------------
# Test 2: Total prediction
# -----------------------------------

expected_total = round(
    float(
        df["predicted_ordered_quantity"].sum()
    ),
    2
)

assert (
    summary["prediction_statistics"]
    ["total_predicted_quantity"]
    == expected_total
)


# -----------------------------------
# Test 3: Average
# -----------------------------------

expected_average = round(
    float(
        df["predicted_ordered_quantity"].mean()
    ),
    2
)

assert (
    summary["prediction_statistics"]
    ["average_predicted_quantity"]
    == expected_average
)


# -----------------------------------
# Test 4: Maximum
# -----------------------------------

expected_maximum = round(
    float(
        df["predicted_ordered_quantity"].max()
    ),
    2
)

assert (
    summary["prediction_statistics"]
    ["maximum_predicted_quantity"]
    == expected_maximum
)


print("\nSUMMARY TESTS PASSED")