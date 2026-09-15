from typing import List
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):

    product_primary_name: str

    processing_periods_name: str

    facility_type_name: str

    beginning_balance: float = Field(
        ge=0
    )

    quantity_received: float = Field(
        ge=0
    )

    quantity_dispensed: float = Field(
        ge=0
    )

    total_losses_and_adjustments: float

    stock_in_hand: float = Field(
        ge=0
    )

    amc: float = Field(
        gt=0
    )

    zone: str

class PredictionResponse(BaseModel):

    predicted_quantity_approved: float

class BatchPredictionRequest(BaseModel):
    records: List[PredictionRequest]


class BatchPredictionItem(BaseModel):
    index: int
    predicted_quantity_approved: float


class BatchPredictionResponse(BaseModel):
    count: int
    predictions: List[BatchPredictionItem]