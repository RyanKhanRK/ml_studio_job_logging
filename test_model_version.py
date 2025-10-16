import mlflow
from mlflow.tracking import MlflowClient

# Connect to your running MLflow server
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Create a test experiment and run
mlflow.set_experiment("ModelVersionTest")

with mlflow.start_run() as run:
    mlflow.log_param("lr", 0.01)
    mlflow.log_metric("accuracy", 0.9)
    mlflow.sklearn.log_model(sk_model=None, artifact_path="model")  # dummy model

    run_id = run.info.run_id

# Register the model
client = MlflowClient()
model_name = "RedisNotifyModel"
model_source = f"runs:/{run_id}/model"

# This triggers create_model_version in your NotifyingStore
mv = client.create_model_version(name=model_name, source=model_source, run_id=run_id)

print(f"✅ Created model version: {mv.name} (v{mv.version})")
