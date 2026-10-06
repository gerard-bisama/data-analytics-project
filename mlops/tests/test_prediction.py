import requests
import random as rd

sample = {
    "product_primary_name": "ACT-AD",
    "processing_periods_name": "May 2025",
    "facility_type_name": "health center",
    "beginning_balance": 100,
    "quantity_received": 50,
    "quantity_dispensed": 80,
    "total_losses_and_adjustments": 0,
    "stock_in_hand": 70,
    "amc": 35,
    "zone": "DISTRICT5"
}
payload = sample
response = requests.post(
    "http://localhost:8000/predict",
    json=payload,
    timeout=120
)

print(
    "Status:",
    response.status_code
)

result = response.json()

print(
    "Predictions:",
    result["predicted_quantity_approved"]
)

