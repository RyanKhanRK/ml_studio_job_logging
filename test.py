import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("NotifyTest")

with mlflow.start_run():
    mlflow.log_param("alpha", 0.5)
    mlflow.log_metric("accuracy", 0.8)