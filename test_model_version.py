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
    print(f"Run created with ID: {run_id}")

    # Log params/metrics
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)

    # Train and log dummy model
    model = LinearRegression()
    mlflow.sklearn.log_model(model, artifact_path="model")

    # --- Automatically register it like UI ---
    model_uri = f"runs:/{run_id}/model"
    print(f"Auto-registering model from {model_uri}")

    registered_model = mlflow.register_model(model_uri, model_name)

print(f"Model registered successfully: {registered_model.name} (v{registered_model.version})")
