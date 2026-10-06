import pandas as pd

from src.processing.dataframe_summary import (
    summarize_prediction_dataframe
)


data = [
    {
      "index": "ACT-AD-1",
      "product_group": "ACT",
      "facility_type": "HEALTH CENTER",
      "reporting_month": "May",
      "zone_type": "RURAL",
      "High_Transmission_Preparation": "YES",
      "stock_status": "Low",
      "quantity_dispensed": 80,
      "total_losses_and_adjustments": 0,
      "stock_in_hand": 0,
      "months_of_stock": 2,
      "amc": 35,
      "predicted_ordered_quantity": 526.34
    },
    {
      "index": "ACT-AD-2",
      "product_group": "PYRA",
      "facility_type": "HEALTH CENTER",
      "reporting_month": "May",
      "zone_type": "URBAN",
      "High_Transmission_Preparation": "YES",
      "stock_status": "Low",
      "quantity_dispensed": 500,
      "total_losses_and_adjustments": 50,
      "stock_in_hand": 50,
      "months_of_stock": 1.3,
      "amc": 350,
      "predicted_ordered_quantity": 2536.14
    }
]


df = pd.DataFrame(data)

summary = summarize_prediction_dataframe(df)

print(summary)