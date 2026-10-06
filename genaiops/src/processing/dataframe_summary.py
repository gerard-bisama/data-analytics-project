import pandas as pd

PREDICTION_COLUMN = "predicted_ordered_quantity"
CATEGORTY_COLUMN = [
    "product_group",
    "facility_type",
    "reporting_month",
    "zone_type",
    "High_Transmission_Preparation",
    "stock_status",
]

def summarize_prediction_dataframe(df: pd.DataFrame) -> dict:
    """
    Create a deterministic statistical summary of malaria
    prediction results.

    The returned dictionary will be used as factual context
    for the LLM.
    """

    if df.empty:
        raise ValueError(
            "Prediction DataFrame cannot be empty."
        )

    if PREDICTION_COLUMN not in df.columns:
        raise ValueError(
            f"Required column '{PREDICTION_COLUMN}' "
            "is missing from the DataFrame."
        )

    summary = {
        "records_analyzed": len(df),

        "prediction_statistics": {
            "total_predicted_quantity": round(
                float(df[PREDICTION_COLUMN].sum()),
                2
            ),

            "average_predicted_quantity": round(
                float(df[PREDICTION_COLUMN].mean()),
                2
            ),

            "median_predicted_quantity": round(
                float(df[PREDICTION_COLUMN].median()),
                2
            ),

            "minimum_predicted_quantity": round(
                float(df[PREDICTION_COLUMN].min()),
                2
            ),

            "maximum_predicted_quantity": round(
                float(df[PREDICTION_COLUMN].max()),
                2
            ),
        }
    }
    for category in CATEGORTY_COLUMN:
        summary ['by_'+category] = summarize_by_category(df,category)
        #print(cat_dict)
        #summary |= cat_dict

    #
    #for category in CATEGORTY_COLUMN:
    #     summary [category+"perventage"] = summarize_by_percentage(df,category)
    #    summary |= cat_dict

    return summary



def summarize_by_category(df: pd.DataFrame, category_column: str,
    prediction_column: str = PREDICTION_COLUMN) -> list[dict]:

    if category_column not in df.columns:
        return []

    grouped = (
        df.groupby(
            category_column,
            dropna=False
        )[prediction_column]
        .agg(
            records="count",
            total_predicted_quantity="sum",
            average_predicted_quantity="mean"
        )
        .reset_index()
    )

    grouped["total_predicted_quantity"] = (
        grouped["total_predicted_quantity"].round(2)
    )

    grouped["average_predicted_quantity"] = (
        grouped["average_predicted_quantity"].round(2)
    )

    return grouped.to_dict(
        orient="records"
        #orient="series"
    )
def summarize_by_percentage(df: pd.DataFrame, category_column: str) -> list[dict]:

    if category_column not in df.columns:
        return []

    counts = (
        df[category_column]
        .fillna("Unknown")
        .value_counts()
        .rename_axis(category_column)
        .reset_index(name="records")
    )

    counts["percentage"] = (
        counts["records"]
        / len(df)
        * 100
    ).round(2)

    return counts.to_dict(
        orient="records"
    )