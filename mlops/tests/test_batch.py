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
range_beginning_balance = {"min":50,"max":150}
range_quantity_received = {"min":10,"max":500}
range_quantity_dispensed = {"min":0,"max":300}
range_total_losses_and_adjustments = {"min":0,"max":100}
range_stock_in_hand = {"min":0,"max":1000}
range_amc = {"min":10,"max":300}
range_zone = {"min":1,"max":28}


payload = {
    "records": [
        {
            "product_primary_name": "ACT-AD",
            "processing_periods_name": "May 2025",
            "facility_type_name": "health center",
            "beginning_balance": rd.randint(range_beginning_balance['min'],range_beginning_balance['max']),
            "quantity_received": rd.randint(range_quantity_received['min'],range_quantity_received['max']),
            "quantity_dispensed":rd.randint(range_quantity_dispensed['min'],range_quantity_dispensed['max']),
            "total_losses_and_adjustments": rd.randint(range_total_losses_and_adjustments['min'],
                    range_total_losses_and_adjustments['max']),
            "stock_in_hand": rd.randint(range_stock_in_hand['min'],
                    range_stock_in_hand['max']),
            "amc": rd.randint(range_amc['min'],range_amc['max']),
            "zone": f"DISTRICT{rd.randint(range_zone['min'],range_zone['max'])}"
        }
        #sample.copy()
        for _ in range(5000)
    ]
}


response = requests.post(
    "http://localhost:8000/predict/batch",
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
    result["count"]
)

print(
    "First prediction:",
    result["predictions"][0:3]
)