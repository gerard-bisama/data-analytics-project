from pydantic import BaseModel, Field


class PredictionRecord(BaseModel):
    """
    One engineered prediction record returned by the
    MLOps /predict/rawbatch_for_interpretation endpoint.
    """

    record_id: str

    product_group: str
    facility_type: str
    reporting_month: str
    zone_type: str
    High_Transmission_Preparation: str
    stock_status: str

    quantity_dispensed: float
    total_losses_and_adjustments: float

    stock_in_hand: float | None = None
    months_of_stock: float | None = None

    amc: float

    predicted_ordered_quantity: float


class InterpretationRequest(BaseModel):
    """
    Input contract for POST /interpret.
    """
    records: list[PredictionRecord]
    prompt: str = Field(
        min_length=3,
        max_length=2000
    )


class InterpretationResponse(BaseModel):
    """
    Output contract for POST /interpret.
    """
    records_analyzed: int
    interpretation: str