import mlflow
from mlflow.tracking import MlflowClient
from sklearn.linear_model import LinearRegression
import os

# --- Setup MLflow connection ---
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("RedisModelTest")

# --- Initialize MLflow client ---
client = MlflowClient()

# --- Define model name (for registry) ---
model_name = "RedisNotifyModel"

# --- Start and log your run ---
with mlflow.start_run() as run:
    run_id = run.info.run_id

# Register the model
client = MlflowClient()
model_name = "RedisNotifyModel"
model_source = f"runs:/{run_id}/model"

# This triggers create_model_version in your LoggingStore
mv = client.create_model_version(name=model_name, source=model_source, run_id=run_id)

print(f"Model registered successfully: {registered_model.name} (v{registered_model.version})")
