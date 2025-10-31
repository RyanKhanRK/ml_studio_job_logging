# 🚀 MLflow Custom Extension (with Redis Notifications)

This project extends **MLflow (v2.17.2)** with **Redis-based notifications** — allowing real-time tracking of new model versions and run events.  
It’s designed for integration into **Blendata Enterprise’s ML Studio**.

---

## ✨ Features

- 🔌 Custom MLflow Tracking Store (`notifying-tracking://`)
- 🧩 Custom MLflow Model Registry Store (`notifying-registry://`)
- 📡 Publishes Redis events when:
  - A **new run** is created
  - A **new model version** is registered
- ⚙️ Easy setup for both local development and integration inside ML Studio

---

## 🛠️ Prerequisites

Before you start, make sure you have:

- **Python 3.9+**
- **pip** and **virtualenv**
- **Redis** server (local or Docker)
- **MLflow 2.17.2**

---

## ⚙️ Installation Steps

### 1️⃣ Clone this repository

```bash
git clone https://github.com/<your-username>/ml_studio_job_logging.git
cd ml_studio_job_logging
````

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate    # (Linux/Mac)
venv\Scripts\activate       # (Windows)
```

### 3️⃣ Install MLflow and Redis Python packages

```bash
pip install mlflow==2.17.2 redis==5.0.0 sqlalchemy
```

### 4️⃣ Install the custom plugin

```bash
pip install -e .
```

---

## 🧱 Setting Up Redis

### Option 1: Local installation (Linux/Mac)

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

### Option 2: Docker

```bash
docker run -d --name redis -p 6379:6379 redis
```

### Verify Redis is running:

```bash
redis-cli ping
# → PONG
```

---

## 🚀 Running MLflow with Custom Stores

Now that MLflow and Redis are ready, start the MLflow server with your custom URIs:

```bash
mlflow server \
    --backend-store-uri "notifying-tracking://sqlite:///mlflow.db" \
    --registry-store-uri "notifying-registry://sqlite:///mlflow.db" \
    --default-artifact-root ./mlartifacts \
    --host 127.0.0.1 \
    --port 5000
```

You should see logs like:

```
Initializing NotifyingRegistryStore...
Connected to Redis server on localhost:6379
✅ MLflow patched successfully with notifying stores.
```

---

## 📡 Example Redis Event

When a new model version is created, Redis will publish an event like this:

```json
{
  "event": "MODEL_VERSION_CREATED",
  "model_name": "RedisModel",
  "version": 1,
  "source": "runs:/abc123/model",
  "status": "Successful"
}
```

You can listen to these events using:

```bash
redis-cli subscribe mlflow_events
```

---

## 💡 Notes

* The **URI scheme prefixes** (`notifying-tracking://` and `notifying-registry://`) automatically wrap around standard MLflow stores (like SQLite, MySQL, or PostgreSQL).
* The plugin emits events to the Redis channel `mlflow_events`.
* Designed to work with **MLflow v2.17.2** and higher.

---
