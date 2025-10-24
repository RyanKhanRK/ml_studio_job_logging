import json
import redis
from mlflow.store.tracking.sqlalchemy_store import SqlAlchemyStore

class NotifyingTrackingStore(SqlAlchemyStore):
    def __init__(self, store_uri, artifact_uri=None):
        if store_uri.startswith("notifying-tracking://"):
            real_store_uri = store_uri.split("://", 1)[1]
        else:
            real_store_uri = store_uri
        print("Initializing NotifyingTrackingStore...")
        super().__init__(real_store_uri, artifact_uri)

        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        print("Connected to Redis server on localhost:6379")

    def create_run(self, experiment_id, user_id, start_time, tags, **kwargs):
        event = {"event": "RUN_CREATED"}
        self.redis_client.publish("mlflow_events", json.dumps(event))
        run = None
        try:
            run = super().create_run(experiment_id, user_id, start_time, tags, **kwargs)
            event.update({"status": "Successful", "run_id": run.info.run_id})
        except Exception as e:
            event.update({"status": "Unsuccessful", "error": str(e)})
        self.redis_client.publish("mlflow_events", json.dumps(event))
        print("Published RUN_CREATED event:", event)
        return run