import pandas as pd


COLUMN_MAPPING = {
    "product_primaryname": "product_primary_name",
    "beginningbalance": "beginning_balance",
    "quantityreceived": "quantity_received",
    "quantitydispensed": "quantity_dispensed",
    "stockinhand": "stock_in_hand",
    "quantityrequested": "quantity_requested",
    "quantityapproved": "quantity_approved",
    "totallossesandadjustments": "total_losses_and_adjustments",
    "packsize": "pack_size",
    "dispensingunit": "dispensing_unit",
}


REQUIRED_MODEL_COLUMNS = [
    "product_primary_name",
    "processing_periods_name",
    "facility_type_name",
    "beginning_balance",
    "quantity_received",
    "quantity_dispensed",
    "stock_in_hand",
    "total_losses_and_adjustments",
    "amc",
    "zone",
]

FILTER_MONTHS = ['February','May','August','November']


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.rename(
        columns=COLUMN_MAPPING,
        inplace=True
    )

    return df


def validate_columns(
    df: pd.DataFrame,
    training: bool = True
) -> None:

    required = REQUIRED_MODEL_COLUMNS.copy()

    if training:
        required.append("quantity_approved")

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Required columns missing: {missing}"
        )
def remove_unsupported_records(df: pd.DataFrame
) -> pd.DataFrame:

    df = df[
        df["amc"] > 0
    ].copy()

    return df
def remove_regular_months_records(df: pd.DataFrame
) -> pd.DataFrame:
    df["processing_periods_name"] = pd.to_datetime(
            df["processing_periods_name"],format="mixed",errors="coerce"
        )
    df["reporting_month"] = (
            df["processing_periods_name"]
            .dt
            .month_name()
        )
    df = df[
        df["reporting_month"].isin(FILTER_MONTHS)
    ].copy()

    return df


def clean_training_data(df: pd.DataFrame) -> pd.DataFrame:

    df = standardize_column_names(df)

    validate_columns(df, training=True)

    required_inventory = [
        "beginning_balance",
        "quantity_received",
        "quantity_dispensed",
        "stock_in_hand",
        "amc",
        "quantity_approved",
    ]
    df = remove_unsupported_records(df).copy()
    df =remove_regular_months_records(df).copy()
    df = df.dropna(
        subset=required_inventory
    ).copy()

    return df
