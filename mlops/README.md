# Project 4 -- MLOps Deployment of the Malaria Order Prediction Model

📁 **Directory:** `mlops/`

## Objective

This project extends **Project 2 -- Quantity to Order Prediction** by
moving the trained malaria commodity order-prediction model from the
analytical environment into a reproducible inference service.

The MLOps implementation uses:

  -----------------------------------------------------------------------
  Tool                                Purpose
  ----------------------------------- -----------------------------------
  **Python 3.11**                     Training and inference runtime

  **scikit-learn**                    Complete ML Pipeline and Random
                                      Forest model

  **MLflow 3.x**                      Experiment tracking, model logging
                                      and model retrieval

  **FastAPI**                         REST inference service

  **Pydantic**                        API request/response validation

  **Uvicorn**                         ASGI server

  **Docker**                          Reproducible packaging of the
                                      inference service

  **Swagger UI**                      Interactive API documentation and
                                      testing

  **pandas / NumPy**                  Tabular processing and batch
                                      inference

  **CSV / PostgreSQL**                Upstream data-source scenarios
  -----------------------------------------------------------------------

The deployed service supports a health check, single-record prediction
and batch prediction. A dashboard-oriented request model also introduces
`record_id` so predictions can be safely associated with source records.

``` text
MLflow Server :5000
       │
       │ models:/<model_id>
       ▼
FastAPI inference service
       ├── GET  /health
       ├── POST /predict
       └── POST /predict/batch
       └── POST /predict/batch_dashboard
                 │
                 ▼
       scikit-learn Pipeline
                 │
                 ▼
       Random Forest prediction
```

➡️ **MLOps implementation:** `mlops/`

------------------------------------------------------------------------

# Technical Documentation

## 1. Project Structure

``` text
mlops/
├── requirements.txt
├── env_template
├── env_template.docker
├── .env
├── .env.docker
├── Dockerfile
├── .dockerignore
├── src/
│   ├── data/
│   │   ├── ingestion.py
│   │   └── cleaning.py
│   ├── features/
│   │   └── engineering.py
│   ├── models/
│   │   ├── pipeline.py
│   │   └── train.py
│   └── api/
│       ├── main.py
│       ├── schemas.py
│       └── model_loader.py
└── tests/
```

### File responsibilities

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `requirements.txt`                  Python dependencies required by the
                                      MLOps runtime.

  `env_template`                      Template for local FastAPI/MLflow
                                      configuration.

  `env_template.docker`               Template for Docker runtime
                                      configuration.

  `.env`                              Local environment values; should
                                      not be committed.

  `.env.docker`                       Docker environment values; should
                                      not be committed.

  `Dockerfile`                        Builds the FastAPI inference image.

  `.dockerignore`                     Excludes secrets, virtual
                                      environments, caches and
                                      unnecessary artifacts from the
                                      build context.

  `src/data/ingestion.py`             CSV/PostgreSQL ingestion
                                      abstraction used by the wider MLOps
                                      workflow.

  `src/data/cleaning.py`              Dataset-level cleaning before
                                      training.

  `src/features/engineering.py`       Reusable custom scikit-learn
                                      feature-engineering and
                                      feature-selection transformers.

  `src/models/pipeline.py`            Complete feature-engineering,
                                      preprocessing and Random Forest
                                      Pipeline.

  `src/models/train.py`               Trains/evaluates the model and logs
                                      the complete Pipeline to MLflow.

  `src/api/schemas.py`                Pydantic contracts for single,
                                      batch and dashboard
                                      requests/responses.

  `src/api/model_loader.py`           Configures MLflow and loads the
                                      Logged Model.

  `src/api/main.py`                   FastAPI application and prediction
                                      endpoints.

  `tests/`                            Validation assets/tests for MLOps
                                      components.
  -----------------------------------------------------------------------

> **Important:** custom transformers are serialized with the model. Keep the serving code and model-sensitive libraries such as 
> `scikit-learn` and `cloudpickle` compatible with the training environment.

------------------------------------------------------------------------

## 2. Runtime and Compatibility

Validated host: **Ubuntu 20.04 LTS**, without changing the OS version.

  Component                      Recommended deployment baseline
  ------------------------------ --------------------------------------------
  Python                         3.11.x
  pip                            Current Python-3.11-compatible release
  MLflow                         Tested 3.x release
  scikit-learn                   Same version as training whenever possible
  cloudpickle                    Same/tested compatible version as training
  pandas / NumPy                 Pinned/tested versions
  Docker Engine                  24.0.9 validated
  FastAPI / Uvicorn / Pydantic   Pin in `requirements.txt`

Check versions:

``` bash
python --version
python -m pip --version
docker version

python -c "import mlflow, sklearn, pandas, numpy, cloudpickle; \
print('MLflow', mlflow.__version__); \
print('sklearn', sklearn.__version__); \
print('pandas', pandas.__version__); \
print('NumPy', numpy.__version__); \
print('cloudpickle', cloudpickle.__version__)"
```

### Docker compatibility note

Docker Engine **20.10.7** on the original Ubuntu 20.04 host caused thread-creation failures such as:

``` text
RuntimeError: can't start new thread
OpenBLAS ... pthread_create failed ... Operation not permitted
jemalloc ... background thread creation failed
```

A diagnostic test succeeded with `seccomp=unconfined`, isolating the issue to the Docker runtime/security layer. The working correction was upgrading the Docker Engine server to **24.0.9** while retaining Ubuntu
20.04.

Validate after upgrade:

``` bash
docker run --rm python:3.11-slim \
python -c "import threading; t=threading.Thread(target=lambda: print('THREAD OK')); t.start(); t.join()"
```

Expected:

``` text
THREAD OK
```

> `--security-opt seccomp=unconfined` was diagnostic only and should not be retained as the deployment solution.

------------------------------------------------------------------------

# Part A -- MLflow + FastAPI

## 3. Prepare the Environment

``` bash
cd mlops

python3.11 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

Verify:

``` bash
which python
python --version
```

------------------------------------------------------------------------

## 4. Configure `.env`

Create the operational file from the repository template:

``` bash
cp env_template .env
```

Configure at least:

``` dotenv
MLFLOW_TRACKING_URI=http://127.0.0.1:5000
MODEL_URI=models:/<MLFLOW_MODEL_ID>
```

Example used during development:

``` dotenv
MLFLOW_TRACKING_URI=http://127.0.0.1:5000
MODEL_URI=models:/m-cefb647d09244448b6a225ac2ea16d01
```

If PostgreSQL ingestion is enabled, also configure the DB variables
defined in `env_template`, for example:

``` dotenv
DB_HOST=<host>
DB_PORT=5432
DB_NAME=<database>
DB_USER=<user>
DB_PASSWORD=<password>
```

------------------------------------------------------------------------

## 5. Start and Test MLflow

Start MLflow using the backend/artifact options configured for the project:

``` bash
mlflow server \
  --host 127.0.0.1 \
  --port 5000 \
  <existing-backend-and-artifact-options>
```

Connectivity test:

``` bash
curl -I http://127.0.0.1:5000
```

### MLflow UI

Open:

``` text
http://127.0.0.1:5000
```

Use the UI to inspect experiments, runs, metrics and Logged Models.

### MLflow 3 model URI

This deployment uses:

``` text
models:/<model_id>
```

Use the URI returned by MLflow when logging the model rather than assuming the model exists at `runs:/<run_id>/model`.

------------------------------------------------------------------------

## 6. Test Model Loading Before FastAPI

``` bash
python -c "from src.api.model_loader import load_model; \
m=load_model(); print(type(m)); print('MODEL LOAD OK')"
```

Expected:

``` text
<class 'sklearn.pipeline.Pipeline'>
MODEL LOAD OK
```

Do not move to the API layer until this test passes.

------------------------------------------------------------------------

## 7. Start FastAPI Locally

``` bash
uvicorn src.api.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --log-level info
```

Development mode:

``` bash
uvicorn src.api.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload \
  --log-level info
```

### Health test

``` bash
curl http://127.0.0.1:8000/health
```

Expected:

``` json
{"status":"healthy","model_loaded":true}
```

### Swagger UI

Open:

``` text
http://127.0.0.1:8000/docs
```

Swagger allows request schemas and all available endpoints to be inspected and tested interactively.

------------------------------------------------------------------------

## 8. Single Prediction

Endpoint:

``` text
POST /predict
```

Example:

``` bash
curl -X POST "http://127.0.0.1:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "product_primary_name": "ACT-AD",
  "processing_periods_name": "May 2025",
  "facility_type_name": "health center",
  "beginning_balance": 100,
  "quantity_received": 50,
  "quantity_dispensed": 80,
  "total_losses_and_adjustments": 0,
  "stock_in_hand": 70,
  "amc": 35,
  "zone": "DISTRICT12"
}'
```

`amc` must be greater than zero. An invalid payload such as `amc = 0` is rejected by Pydantic with HTTP `422`.

------------------------------------------------------------------------

## 9. Batch Prediction

Endpoint:

``` text
POST /predict/batch
```

Batch inference allows a dashboard or another application to submit hundreds or thousands of records in one HTTP request.

Example:

``` bash
curl -X POST "http://127.0.0.1:8000/predict/batch" \
-H "Content-Type: application/json" \
-d '{
  "records": [
    {
      "product_primary_name": "ACT-AD",
      "processing_periods_name": "May 2025",
      "facility_type_name": "health center",
      "beginning_balance": 100,
      "quantity_received": 50,
      "quantity_dispensed": 80,
      "total_losses_and_adjustments": 0,
      "stock_in_hand": 70,
      "amc": 35,
      "zone": "DISTRICT1"
    },
    {
      "product_primary_name": "RDT",
      "processing_periods_name": "May 2025",
      "facility_type_name": "health center",
      "beginning_balance": 200,
      "quantity_received": 100,
      "quantity_dispensed": 120,
      "total_losses_and_adjustments": 0,
      "stock_in_hand": 180,
      "amc": 60,
      "zone": "DISTRICT2"
    }
  ]
}'
```

Example response:

``` json
{
  "count": 2,
  "predictions": [
    {"index": 0, "predicted_quantity_approved": 1234.5},
    {"index": 1, "predicted_quantity_approved": 876.2}
  ]
}
```

### `index` association

`index` is the **zero-based position in the submitted `records` array**:

``` text
records[0] --> prediction index 0
records[1] --> prediction index 1
records[2] --> prediction index 2
```

It is not automatically a pandas index, database ID, requisition ID or facility ID.

The current maximum batch configuration is:

``` text
MAX_BATCH_SIZE = 5000
```

A request above this limit returns HTTP `413`. A batch containing an invalid object can return HTTP `422` before the prediction function
runs.

### Batch performance test

Test progressively:

``` text
10 -> 100 -> 300 -> 500 -> 1,000 -> 5,000
```

Example Python client:

``` python
import requests
import time

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
    "zone": "DISTRICT10"
}

payload = {"records": [sample.copy() for _ in range(1000)]}

start = time.perf_counter()
response = requests.post(
    "http://127.0.0.1:8000/predict/batch",
    json=payload,
    timeout=120
)

print("HTTP:", response.status_code)
print("Seconds:", round(time.perf_counter() - start, 3))
print(response.json() if response.ok else response.text)
```

------------------------------------------------------------------------

## 10. Dashboard-Oriented Scenario: `record_id`

For a dashboard, positional `index` is less robust than a stable identifier.

`PredictionRequestDashboard(BaseModel)` introduces:

``` python
record_id: str
```

The dashboard supplies `record_id` with every record. It is retained only to associate the response with the source row and **must not be
passed to the ML model as a feature**.

Conceptually:

``` python
record_ids = input_data["record_id"].copy()
model_input = input_data.drop(columns=["record_id"])
predictions = model.predict(model_input)
```

The response can therefore contain:

``` json
{
  "record_id": "REQ-LINE-000145",
  "predicted_quantity_approved": 1234.5
}
```

Recommended flow:

``` text
Dashboard source row
      │
      │ record_id
      ▼
FastAPI batch request
      │
      ▼
ML prediction (record_id excluded)
      │
      ▼
record_id + prediction
      │
      ▼
Safe join back to dashboard dataset
```

Prefer an existing stable source-system key when appropriate. This avoids relying on response order when predictions are integrated into
dashboards.

------------------------------------------------------------------------

# Part B -- Docker Packaging

## 11. Docker Architecture

The validated architecture keeps MLflow on the Ubuntu host and packages the FastAPI inference service in Docker:

``` text
Ubuntu 20.04
├── MLflow :5000
└── Docker Engine
    └── malaria-api
        └── FastAPI :8000
             │
             └── MLflow client
                  └── host.docker.internal:5000
```

------------------------------------------------------------------------

## 12. Configure `.env.docker`

``` bash
cp env_template.docker .env.docker
```

Configure:

``` dotenv
MLFLOW_TRACKING_URI=http://host.docker.internal:5000
MODEL_URI=models:/<MLFLOW_MODEL_ID>
```

Inside Docker, `127.0.0.1` refers to the container. `host.docker.internal` is therefore used to reach MLflow on the Ubuntu host.

------------------------------------------------------------------------

## 13. Configure MLflow for Container Access

MLflow must listen on a reachable interface:

``` bash
mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --allowed-hosts "localhost:*,127.0.0.1:*,host.docker.internal:*" \
  <existing-backend-and-artifact-options>
```

This also addresses MLflow Host-header validation encountered during deployment. Avoid `--allowed-hosts "*"` as a permanent configuration.

------------------------------------------------------------------------

## 14. Build the Docker Image

``` bash
docker build -t malaria-order-api:1.0 .
```

Verify:

``` bash
docker images malaria-order-api
```

The Dockerfile packages Python, `requirements.txt` and the FastAPI
source, and starts Uvicorn on:

``` text
0.0.0.0:8000
```

------------------------------------------------------------------------

## 15. Intermediate Docker Tests

### 15.1 Thread/runtime test

``` bash
docker run --rm python:3.11-slim \
python -c "import threading; t=threading.Thread(target=lambda: print('THREAD OK')); t.start(); t.join()"
```

### 15.2 Host resolution

``` bash
docker run --rm \
--add-host=host.docker.internal:host-gateway \
python:3.11-slim \
python -c "import socket; print(socket.gethostbyname('host.docker.internal'))"
```

### 15.3 Docker-to-MLflow connectivity

``` bash
docker run --rm \
--add-host=host.docker.internal:host-gateway \
curlimages/curl \
-i http://host.docker.internal:5000/
```

### 15.4 Environment configuration

``` bash
docker run --rm \
--env-file .env.docker \
--entrypoint python \
malaria-order-api:1.0 \
-c "import os; print(os.getenv('MLFLOW_TRACKING_URI')); print(os.getenv('MODEL_URI'))"
```

Expected pattern:

``` text
http://host.docker.internal:5000
models:/<model_id>
```

### 15.5 Model loading inside Docker

``` bash
docker run --rm \
--add-host=host.docker.internal:host-gateway \
--env-file .env.docker \
--entrypoint python \
malaria-order-api:1.0 \
-c "from src.api.model_loader import load_model; \
m=load_model(); print(type(m)); print('MODEL LOAD OK')"
```

Only start FastAPI after `MODEL LOAD OK`.

------------------------------------------------------------------------

## 16. Start the Dockerized API

``` bash
docker rm -f malaria-api 2>/dev/null || true

docker run -d \
--name malaria-api \
--add-host=host.docker.internal:host-gateway \
--env-file .env.docker \
-p 8000:8000 \
malaria-order-api:1.0
```

Check:

``` bash
docker ps
docker logs -f malaria-api
```

Health:

``` bash
curl http://127.0.0.1:8000/health
```

Swagger:

``` text
http://127.0.0.1:8000/docs
```

Use the same `/predict` and `/predict/batch` payloads used during local testing. Local and Dockerized inference should return equivalent results for the same model and payload.

------------------------------------------------------------------------

## 17. Monitor Batch Execution

``` bash
docker logs -f malaria-api
```

Resource monitoring:

``` bash
docker stats malaria-api
```

Monitor CPU, memory and PIDs while increasing batch sizes.

------------------------------------------------------------------------

## 18. Troubleshooting

  --------------------------------------------------------------------------------------------
  Symptom                                  Likely cause            Resolution
  ---------------------------------------- ----------------------- ---------------------------
  `422 Unprocessable Entity`               Payload violates        Inspect response `detail`;
                                           Pydantic schema         e.g. `amc` must be `> 0`

  `413`                                    Batch above             Reduce batch or review
                                           `MAX_BATCH_SIZE`        tested limit

  `127.0.0.1:5000 Connection refused` in   Container is addressing Use
  Docker                                   itself                  `host.docker.internal` +
                                                                   `host-gateway`

  `Invalid Host header`                    MLflow hostname         Configure `--allowed-hosts`
                                           security validation     

  Model artifact path failure              Wrong MLflow 3 URI      Use `models:/<model_id>`

  `RuntimeError: can't start new thread`   Old Docker/seccomp      Upgrade Docker Engine and
                                           compatibility           rerun thread test

  OpenBLAS `pthread_create failed`         Same Docker             Correct runtime; do not
                                           runtime/security issue  permanently disable seccomp

  Custom transformer import error          Serving image lacks     Include project source/code
                                           compatible code         paths

  sklearn compatibility warning/error      Training/serving        Pin compatible versions
                                           dependency drift        

  Unknown OneHotEncoder categories         Category absent during  Review mapping/data;
                                           training                `handle_unknown="ignore"`
                                                                   avoids a crash
  --------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## 19. Deployment Checklist

-   [ ] Python 3.11 environment active.
-   [ ] Dependencies installed and versions recorded.
-   [ ] `.env` created from `env_template`.
-   [ ] MLflow server and UI accessible.
-   [ ] `models:/<model_id>` configured.
-   [ ] Model loads without FastAPI.
-   [ ] Local `/health` succeeds.
-   [ ] Local `/predict` succeeds.
-   [ ] Local `/predict/batch` succeeds.
-   [ ] Batch `index` association is understood.
-   [ ] Dashboard integration uses `record_id` where required.
-   [ ] Docker Engine passes normal thread test.
-   [ ] `.env.docker` created from `env_template.docker`.
-   [ ] Docker image builds.
-   [ ] Docker resolves `host.docker.internal`.
-   [ ] Docker reaches MLflow.
-   [ ] Docker model loading returns `MODEL LOAD OK`.
-   [ ] Container `/health` succeeds.
-   [ ] Container `/predict` and `/predict/batch` succeed.
-   [ ] Swagger UI is accessible.
-   [ ] Logs and resources are monitored during batch tests.

------------------------------------------------------------------------

## 20. Security Notes

-   Never commit `.env` or `.env.docker` containing secrets.
-   Do not permanently use `seccomp=unconfined`.
-   Restrict MLflow `--allowed-hosts`.
-   Do not expose MLflow publicly without appropriate network and
    authentication controls.
-   Pin model-sensitive dependency versions.
-   Keep custom transformer code compatible with the serialized model.
-   Before Internet-facing deployment, add appropriate authentication,
    TLS/reverse proxy, request controls, structured logging and
    monitoring.

------------------------------------------------------------------------

## 21. Current MLOps Scope

``` text
Training
   ↓
MLflow tracking / Logged Model
   ↓
Model retrieval
   ↓
FastAPI inference
   ↓
Single + batch prediction
   ↓
Docker packaging
   ↓
Dashboard-ready model service
```

Potential extensions include PostgreSQL-driven batch scoring, orchestration, prediction persistence, drift monitoring, observability,
CI/CD and formal model-promotion/versioning policies.

------------------------------------------------------------------------

## Repository

-   **Main project:**
    https://github.com/gerard-bisama/data-analytics-project
-   **MLOps:**
    https://github.com/gerard-bisama/data-analytics-project/tree/main/mlops
-   **Prediction model:**
    https://github.com/gerard-bisama/data-analytics-project/tree/main/order_prediction

This project demonstrates the transition from notebook-based Machine
Learning experimentation to a **reproducible, testable and containerized
inference service** that can be integrated with operational applications
and dashboards.
