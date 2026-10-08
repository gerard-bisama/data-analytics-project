import pandas as pd
import requests
import json

#CSV_FILE = "../mlops/data/raw/requisition_dashboard.csv"
DATA_SOURCE = "csv"
MLOPS_API_DATA_INGESTION_URL = (
    "http://localhost:8000/predict/data_ingestion"
)
MLOPS_API_GETDATA_FORINTERPRETATION_URL = (
    "http://localhost:8000/predict/rawbatch_for_interpretation"
)
GENAIOPS_INTERPRET_URL = (
    "http://localhost:8001/interpret"
)
# ==========================================
# STEP 1 — Data ingestion
# ==========================================

print("\n=== STEP 1: DATA INGESTION ===")

ingestion_response = requests.post(
    MLOPS_API_DATA_INGESTION_URL,
    json={
        "source": DATA_SOURCE
    },
    timeout=120
)

print(
    "Ingestion HTTP status:",
    ingestion_response.status_code
)
ingestion_response.raise_for_status()
records = ingestion_response.json()

payload = {
    "records": records
}
#payload_json = json.dumps(payload)
#print(payload_json)
response = requests.post(MLOPS_API_GETDATA_FORINTERPRETATION_URL,
    json=payload,
    timeout=120
)
#print(payload_json)
print("HTTP status:", response.status_code)
response.raise_for_status()
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
#print( json.dumps(engineered_predicted_records))

df_engineered = pd.DataFrame(
    engineered_predicted_records
)

# ==========================================
# GenAIOps API
# ==========================================


interpretation_payload = {
    "records": engineered_predicted_records,
    "prompt": (
        "Provide a concise management interpretation "
        "of the main supply situation in this dataset."
    )
}


print(
    "\nSending predictions to GenAIOps..."
)


genai_response = requests.post(
    GENAIOPS_INTERPRET_URL,
    json=interpretation_payload,
    timeout=180
)


print(
    "GenAIOps HTTP status:",
    genai_response.status_code
)


if genai_response.status_code != 200:

    print(
        "\n=== GENAIOPS ERROR ==="
    )

    print(
        genai_response.text
    )

    raise RuntimeError(
        "GenAIOps interpretation "
        "request failed."
    )


genai_result = (
    genai_response.json()
)


print(
    "\n=== GENAI INTERPRETATION ==="
)

print(
    genai_result["interpretation"]
)


print(
    "\nRecords analyzed:",
    genai_result["records_analyzed"]
)