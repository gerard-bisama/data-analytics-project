import pandas as pd
import requests
import json

from src.processing.dataframe_summary import (
    summarize_prediction_dataframe
)

from src.prompts.interpretation import (
    build_interpretation_messages
)

from src.llm.generator import (
    generate_interpretation
)

CSV_FILE = "../mlops/data/raw/requisition_dashboard.csv"

MLOPS_API_GETDATA_FORINTERPRETATION_URL = (
    "http://localhost:8000/predict/rawbatch_for_interpretation"
)


df_raw = pd.read_csv(CSV_FILE)


print("\n=== CSV LOADED ===")
print(f"Records: {len(df_raw)}")

print("\nColumns:")
print(df_raw.columns.tolist())

#print("\nFirst records:")
#print(df.head().to_string(index=False))

#print("\nMissing values:")
#print(df.isna().sum())
# ==========================================
# 2. Apply existing MLOps feature engineering
# ==========================================

"""
print("\n=== ENGINEERED DATA ===")
print(df_raw.head())
"""

records = (
    df_raw.astype(object)
    .where(pd.notnull(df_raw), None)
    .to_dict(orient="records")
)
#records = json.dumps(records)
print("\n=== FIRST API RECORD ===")
#print(records[0])
payload = {
    "records": records[0:10000]
}
payload_json = json.dumps(payload)
#print(payload_json)
response = requests.post(MLOPS_API_GETDATA_FORINTERPRETATION_URL,
    json=payload,
    timeout=120
)
#print(payload_json)
print("HTTP status:", response.status_code)
print("\n=== Response  API Data PREDICTION ===")
#print(response.text)

if response.status_code != 200:
    print("\n=== FEATURE ENGINEERING ERROR ===")
    print(response.text)

    raise RuntimeError(
        "MLOps feature engineering request failed."
    )
# ==========================================
# 4. Extract engineered records
# ==========================================

result = response.json()

engineered_predicted_records = result["predictions"]

df_engineered = pd.DataFrame(
    engineered_predicted_records
)

# ---------------------------------
# Step 2: Deterministic analysis
# ---------------------------------

summary = summarize_prediction_dataframe(df_engineered)

print("\n=== DATA SUMMARY ===")
#print(summary)

# ---------------------------------
# Step 3: Controlled prompt
# ---------------------------------

messages = build_interpretation_messages(
    summary=summary,
    user_prompt=(
        "Provide a concise management interpretation "
        "of the main supply situation in this dataset."
    )
)

# ---------------------------------
# Step 4: LLM interpretation
# ---------------------------------

print("\nSending analytical context to Hugging Face...")

interpretation = generate_interpretation(
    messages
)

print("\n=== GENAI INTERPRETATION ===")
print(interpretation)