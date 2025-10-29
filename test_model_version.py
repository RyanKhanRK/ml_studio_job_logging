import mlflow
from mlflow.tracking import MlflowClient
from sklearn.linear_model import LinearRegression
import os

# Connect to MLflow server
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("RedisModelTest")

# Start a run
with mlflow.start_run() as run:
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)

    # Create and log a dummy sklearn model
    model = LinearRegression()
    model_path = "model"
    mlflow.sklearn.log_model(sk_model=model, artifact_path=model_path)

    run_id = run.info.run_id
    print(f"Run created with ID: {run_id}")

# Register the model (this triggers create_model_version)
# client = MlflowClient()
# model_name = "RedisNotifyModel"
# source = f"runs:/{run_id}/{model_path}"

# print("Creating model version...")
# mv = client.create_model_version(
#     name=model_name,
#     source=source,
#     run_id=run_id
# )

# print(f"Model version created: {mv.name} (v{mv.version})")

mlflow.register_model("run://3/5a6f7b10636f4173b74a25304621e7b8/artifacts", "test")