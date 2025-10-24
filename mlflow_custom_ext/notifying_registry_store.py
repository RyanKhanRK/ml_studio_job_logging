import json
import redis
from mlflow.store.model_registry.sqlalchemy_store import SqlAlchemyStore

class NotifyingRegistryStore(SqlAlchemyStore):
    def __init__(self, store_uri, artifact_uri=None):
        if store_uri.startswith("notifying-registry://"):
            real_store_uri = store_uri.split("://", 1)[1]
        else:
            real_store_uri = store_uri
        print("Initializing NotifyingRegistryStore...")
        super().__init__(real_store_uri, artifact_uri)

        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        print("Connected to Redis server on localhost:6379")

    def create_model_version(self, name, source, run_id=None, tags=None, **kwargs):
        mv = None
        try:
            mv = super().create_model_version(
                name=name, source=source, run_id=run_id, tags=tags, **kwargs
            )
            event = {
                "event": "MODEL_VERSION_CREATED",
                "model_name": mv.name,
                "version": mv.version,
                "status": "Successful",
            }
        except Exception as e:
            event = {
                "event": "MODEL_VERSION_FAILED",
                "model_name": name,
                "status": "Unsuccessful",
                "error": str(e),
            }

        self.redis_client.publish("mlflow_events", json.dumps(event))
        print("Published MODEL_VERSION event:", event)
        return mv