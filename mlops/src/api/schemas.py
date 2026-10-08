from typing import List
from pydantic import BaseModel, Field, field_validator
from typing import Literal

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

class PredictionRequestDashboard(BaseModel):

    record_id: str
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

class BatchPredictionRequestDashboard(BaseModel):
    records: List[PredictionRequestDashboard]

class BatchPredictionItem(BaseModel):
    index: int
    predicted_quantity_approved: float

class BatchPredictionItemInterpretation(BaseModel):
    record_id: str
    product_group: str | None = None
    facility_type: str | None = None
    reporting_month : str | None = None
    zone_type: str | None = None
    High_Transmission_Preparation: str
    stock_status: str | None = None
    quantity_dispensed: float 
    total_losses_and_adjustments: float
    stock_in_hand: float
    months_of_stock: float
    amc: float
    predicted_ordered_quantity: float
    @field_validator(
        "facility_type",
        mode="before")
    @classmethod
    def normalize_facility_type (cls, value):
        # Python None
        #return value
        #if value is None:
        #    return None 
        
        # Empty strings or textual NaN
        if isinstance(value, str):
            value = value.strip()

            if value == "":
                return None

            if value.lower() in {"nan", "none", "null"}:
                return None
            else:
                return value
class FeatureEngineeringRecord(BaseModel):
    record_id: str

    product_primaryname: str
    processing_periods_name: str
    facility_type_name: str | None = None

    beginningbalance: float | None = None
    quantityreceived: float | None = None
    quantitydispensed: float | None = None
    stockinhand: float | None = None
    totallossesandadjustments: float | None = None

    amc: float | None = None
    zone: str
    quantityapproved: float | None = None

class FeatureEngineeringRequest(BaseModel):
    records: list[FeatureEngineeringRecord]

class BatchPredictionItemDashboard(BaseModel):
    index: str
    predicted_quantity_approved: float

class SourcePredictionRequest(BaseModel):
    source: Literal["csv", "postgres"]

class BatchPredictionResponse(BaseModel):
    count: int
    predictions: List[BatchPredictionItem]

class BatchPredictionResponseDashboard(BaseModel):
    count: int
    predictions: List[BatchPredictionItemDashboard]

class BatchPredictionResponseInterpretation(BaseModel):
    count: int
    predictions: List[BatchPredictionItemInterpretation]