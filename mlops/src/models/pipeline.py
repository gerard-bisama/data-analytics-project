from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

from src.features.engineering import (
    SupplyChainFeatureEngineer,
    ModelFeatureSelector
)

CATEGORICAL_FEATURES = [
    "product_group",
    "facility_type",
    "reporting_month",
    "zone_type",
    "High_Transmission_Preparation",
    "stock_status",
]

NUMERICAL_FEATURES = [
    "beginning_balance",
    "quantity_received",
    "quantity_dispensed",
    "total_losses_and_adjustments",
    "stock_in_hand",
    "months_of_stock",
    "amc",
]

categorical_transformer = OneHotEncoder(
    handle_unknown="ignore",
    drop="first",
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            categorical_transformer,
            CATEGORICAL_FEATURES,
        ),
        (
            "numerical",
            "passthrough",
            NUMERICAL_FEATURES,
        ),
    ]
)

random_forest = RandomForestRegressor(
    n_estimators=300,
    max_depth=6,
    max_features=None,
    max_samples=0.8,
    min_samples_leaf=30,
    min_samples_split=10,
    bootstrap=True,
    n_jobs=-1,
    random_state=0,
)

model_pipeline = Pipeline(
    steps=[
        (
            "feature_engineering",
            SupplyChainFeatureEngineer()
        ),
        (
            "feature_selection",
            ModelFeatureSelector()
        ),
        (
            "preprocessing",
            preprocessor
        ),
        (
            "model",
            random_forest
        ),
    ]
)

