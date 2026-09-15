from fastapi import FastAPI
from fastapi import HTTPException
import logging
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)
from src.api.model_loader import (
    load_model,
)

from src.api.schemas import (
    BatchPredictionItemDashboard,
    BatchPredictionResponseDashboard,
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    BatchPredictionItem,
    BatchPredictionRequestDashboard
)
import pandas as pd

app = FastAPI(
    title="Malaria ML prediction API",
    description=("API for predicting malaria commadities"),
     version="1.0.0",
)
model = load_model()
MAX_BATCH_SIZE = 5000

@app.get("/")
def root():
    return { "message": "Malaria Order Prediction API"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
    }

@app.post("/predict-test")
def predict_test(
    request: PredictionRequest
):

    return request.model_dump()


@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(
    request: PredictionRequest
):
    try:
        input_data = pd.DataFrame(
        [
            request.model_dump()
        ])

        prediction = model.predict(
            input_data
        )

        return {
            "predicted_quantity_approved":
                float(prediction[0])
        }
    except Exception as exc:

        raise HTTPException(
            status_céode=500,
            detail="Prediction failed."
        ) from exc


@app.post(
    "/predict/batch",
    response_model=BatchPredictionResponse
)
def predict_batch(
    request: BatchPredictionRequest
):

    start = time.perf_counter()
    count = len(request.records)
    logger.info(
        "Batch prediction started: %s records",
        count
    )
    if count == 0:
        raise HTTPException(
            status_code=400,
            detail="No records provided."
        )

    if count > MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=413,
            detail=(
                f"Maximum batch size is "
                f"{MAX_BATCH_SIZE} records."
            )
        )
    try:
        #Stage 1
        records = [
            record.model_dump()
            for record in request.records
        ]
        logger.info(
                "Stage 1 complete: records converted"
            )
        #Stage 2

        input_data = pd.DataFrame(records)
        logger.info(
                "Stage 2 complete: DataFrame shape=%s",
                input_data.shape
            )
        # Stage 3
        predict_start = time.perf_counter()

        predictions = model.predict(input_data)
        logger.info(
                "Stage 3 complete: model.predict() "
                "returned %s predictions in %.3f sec",
                len(predictions),
                time.perf_counter() - predict_start
            )
        # Stage 4
        results = [
            BatchPredictionItem(
                index=i,
                predicted_quantity_approved=float(pred)
            )
            for i, pred in enumerate(predictions)
        ]
        logger.info(
                "Stage 4 complete: response created"
            )

        return BatchPredictionResponse(
            count=len(results),
            predictions=results
        )
    except Exception:
        logger.exception(
            "Batch prediction failed for %s records",
            count
        )
        raise

@app.post(
    "/predict/batch_dashboard",
    response_model=BatchPredictionResponseDashboard
)
def predict_batch_dashboard(
    request: BatchPredictionRequestDashboard
):

    start = time.perf_counter()
    count = len(request.records)
    logger.info(
        "Batch prediction started: %s records",
        count
    )
    if count == 0:
        raise HTTPException(
            status_code=400,
            detail="No records provided."
        )

    if count > MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=413,
            detail=(
                f"Maximum batch size is "
                f"{MAX_BATCH_SIZE} records."
            )
        )
    try:
        #Stage 1
        records = [
            record.model_dump()
            for record in request.records
        ]
        logger.info(
                "Stage 1 complete: records converted"
            )
        #Stage 2
        df = pd.DataFrame(records)

        record_ids = df["record_id"].copy()

        model_input = df.drop(
            columns=["record_id"]
)

        input_data = model_input
        logger.info(
                "Stage 2 complete: DataFrame shape=%s",
                input_data.shape
            )
        # Stage 3
        predict_start = time.perf_counter()

        predictions = model.predict(input_data)
        logger.info(
                "Stage 3 complete: model.predict() "
                "returned %s predictions in %.3f sec",
                len(predictions),
                time.perf_counter() - predict_start
            )
        # Stage 4
        results = [
            BatchPredictionItemDashboard(
                index=record_id,
                predicted_quantity_approved=float(pred)
            )
            for record_id, pred
            in zip(record_ids, predictions)
        ]
        logger.info(
                "Stage 4 complete: response created"
            )

        return BatchPredictionResponseDashboard(
            count=len(results),
            predictions=results
        )
    except Exception:
        logger.exception(
            "Batch prediction failed for %s records",
            count
        )
        raise