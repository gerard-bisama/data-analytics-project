import argparse

import joblib
#==========MLFlow imports ================
import mlflow
import mlflow.sklearn
import numpy as np
from mlflow.models import infer_signature
#=========================================

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


from src.data.ingestion import load_data
from src.data.cleaning import (
    clean_training_data,
    remove_unsupported_records,
)

from src.models.pipeline import (
    model_pipeline
)

#==================MLFlow configuration =======================
MLFLOW_TRACKING_URI = (
    "http://127.0.0.1:5000"
)

EXPERIMENT_NAME = (
    "malaria-order-prediction"
)
mlflow.set_tracking_uri(
    MLFLOW_TRACKING_URI
)

mlflow.set_experiment(
    EXPERIMENT_NAME
)
#==============================================================
TARGET = "quantity_approved"


POSTGRES_QUERY = """
SELECT *
FROM requisitions_raw
"""


def train(
    source: str,
    csv_path: str | None = None
):

    # -----------------------
    # 1. Ingestion
    # -----------------------

    if source == "csv":

        df = load_data(
            source="csv",
            csv_path=csv_path
        )

    else:

        df = load_data(
            source="postgres",
            query=POSTGRES_QUERY
        )

    print(
        f"Loaded {len(df):,} rows"
    )

    # -----------------------
    # 2. Cleaning
    # -----------------------

    df = clean_training_data(df)

    #df = remove_unsupported_records(df)

    print(
        f"After cleaning: {len(df):,} rows"
    )

    # -----------------------
    # 3. X / y
    # -----------------------

    X = df.drop(
        columns=[TARGET]
    )

    y = df[TARGET]

    # -----------------------
    # 4. Train / test split
    # -----------------------
    
    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=0
        )
    )

    # -----------------------
    # 5. Train complete pipeline
    # -----------------------
    with mlflow.start_run() as run:
        
        mlflow.set_tag(
            "data_source",
            source
        )

        mlflow.set_tag(
            "model_type",
            "RandomForestRegressor"
        )

        mlflow.set_tag(
            "target",
            TARGET
        )

        rf = model_pipeline.named_steps[
            "model"
        ]

        mlflow.log_params({
            "n_estimators":
                rf.n_estimators,

            "max_depth":
                rf.max_depth,

            "max_features":
                rf.max_features,

            "max_samples":
                rf.max_samples,

            "min_samples_leaf":
                rf.min_samples_leaf,

            "min_samples_split":
                rf.min_samples_split,

            "bootstrap":
                rf.bootstrap,

            "random_state":
                rf.random_state,

            "dataset_rows":
                len(df),

            "train_rows":
                len(X_train),

            "test_rows":
                len(X_test),
        })
        model_pipeline.fit(
            X_train,
            y_train
        )

        # -----------------------
        # 6. Evaluate
        # -----------------------

        predictions = (
            model_pipeline.predict(X_test)
        )

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = np.sqrt (
            mean_squared_error(
                y_test,
                predictions
            ) 
        )

        r2 = r2_score(
            y_test,
            predictions
        )

        print("\nModel performance")
        print("------------------")
        print(f"MAE : {mae:.2f}")
        print(f"RMSE: {rmse:.2f}")
        print(f"R2  : {r2:.4f}")
        #===
        mlflow.log_metrics({
            "mae": mae,
            "rmse": rmse,
            "r2": r2,
         })

        input_example = (
            X_train.head(5)
        )
        signature = infer_signature(
            input_example,
            model_pipeline.predict(
                input_example
            )
        )
        mlflow.sklearn.log_model(
            sk_model=model_pipeline,
            name="model",
            signature=signature,
            input_example=input_example,
            serialization_format="cloudpickle",
            code_paths=["src"],
        )
        print(
            "Run ID:",
            run.info.run_id
        )

    # -----------------------
    # 7. Save complete pipeline
    # -----------------------

    joblib.dump(
        model_pipeline,
        "artifacts/random_forest_pipeline.joblib"
    )

    print(
        "\nModel saved:"
        "\nartifacts/random_forest_pipeline.joblib"
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source",
        required=True,
        choices=["csv", "postgres"]
    )

    parser.add_argument(
        "--csv-path",
        required=False
    )

    args = parser.parse_args()

    train(
        source=args.source,
        csv_path=args.csv_path
    )
