import os

import mlflow
import mlflow.sklearn
from dotenv import load_dotenv
load_dotenv()

MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://127.0.0.1:5000",
)

MODEL_URI = os.getenv(
    "MODEL_URI"
)

def load_model():

    if not MODEL_URI:
        raise ValueError(
            "MODEL_URI environment variable "
            "is not defined."
        )

    mlflow.set_tracking_uri(
        MLFLOW_TRACKING_URI
    )

    model = mlflow.sklearn.load_model(
        MODEL_URI
    )

    return model