# ML Studio Job Logging Extension

A plugin extension for **ML Studio** that adds Redis-based event notifications when new runs or model versions are created.

## 🚀 Features
- Custom MLflow Tracking Store (`notifying-tracking://`)
- Custom MLflow Registry Store (`notifying-registry://`)
- Publishes MLflow events (`RUN_CREATED`, `MODEL_VERSION_CREATED`) to a Redis channel
- Easy integration into Blendata Enterprise’s ML Studio

## 🧠 Usage

### 1. Install
```bash
pip install -e .
````

### 2. Start Redis

```bash
redis-server
```

### 3. Start MLflow with custom URIs

```bash
mlflow server \
    --backend-store-uri "notifying-tracking://sqlite:///mlflow.db" \
    --registry-store-uri "notifying-registry://sqlite:///mlflow.db" \
    --default-artifact-root ./mlartifacts \
    --host 127.0.0.1 \
    --port 5000
```

### 4. Log and register models

```python
import mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("RedisDemo")

with mlflow.start_run():
    mlflow.log_param("lr", 0.01)
    mlflow.log_metric("accuracy", 0.9)
    mlflow.sklearn.log_model(sk_model=model, artifact_path="model")
    mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/model", "RedisModel")
```

---

## 📡 Redis Event Example

When a new model version is created, a message like this will be published:

```json
Published RUN_CREATED event: {'event': 'RUN_CREATED', 'status': 'Successful', 'run_id': 'f8f65648f1994de4bb33fc89514266ff'}

Published MODEL_VERSION event: {'event': 'MODEL_VERSION_CREATED', 'model_name': 'RedisNotifyModel', 'version': 2, 'source': '/home/ryank/Downloads/mlflow_custom_ext/mlartifacts/3/4476e8503c46444fa4bcb4223f3e1043/artifacts/model', 'status': 'Successful'}
```

---

## ✅ To Test Locally

```bash
# Create venv
python3 -m venv venv
source venv/bin/activate

# Install plugin
pip install -e .

# Run Redis
redis-server

# Start MLflow with your new URIs
mlflow server \
    --backend-store-uri "notifying-tracking://sqlite:///mlflow.db" \
    --registry-store-uri "notifying-registry://sqlite:///mlflow.db" \
    --default-artifact-root ./mlartifacts \
    --host 127.0.0.1 \
    --port 5000
```
