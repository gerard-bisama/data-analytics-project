from src.api.schemas import (
    InterpretationRequest
)


payload = {
    "records": [
        {
            "record_id": "Req-001",
            "product_group": "PYRA",
            "facility_type": "HEALTH CENTER",
            "reporting_month": "May",
            "zone_type": "RURAL",
            "High_Transmission_Preparation": "YES",
            "stock_status": "Overstock",
            "quantity_dispensed": 10,
            "total_losses_and_adjustments": 313,
            "stock_in_hand": 980,
            "months_of_stock": 490,
            "amc": 2,
            "predicted_ordered_quantity": 1
        },
        {
            "record_id": "Req-002",
            "product_group": "ACT",
            "facility_type": "HEALTH CENTER",
            "reporting_month": "May",
            "zone_type": "RURAL",
            "High_Transmission_Preparation": "YES",
            "stock_status": "Overstock",
            "quantity_dispensed": 10,
            "total_losses_and_adjustments": 313,
            "stock_in_hand": 980,
            "months_of_stock": 490,
            "amc": 2,
            "predicted_ordered_quantity": 1
        }
    ],
    "prompt": (
        "Provide a concise management interpretation "
        "of the main supply situation in this dataset."
    )
}


request = InterpretationRequest(**payload)


assert len(request.records) == 2

assert (
    request.records[0].record_id
    == "Req-001"
)

assert (
    request.records[0].product_group
    == "PYRA"
)


print(
    "STAGE 5.10 - SCHEMA TEST PASSED"
)