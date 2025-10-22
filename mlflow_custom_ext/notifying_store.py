import json
import redis
from mlflow.store.tracking.sqlalchemy_store import SqlAlchemyStore

class NotifyingStore(SqlAlchemyStore):
    def __init__(self, store_uri, artifact_uri=None):
        # Handle custom scheme
        if store_uri.startswith("notifying-db://"):
            real_store_uri = store_uri.split("://", 1)[1]
        else:
            real_store_uri = store_uri
        print("Initializing NotifyingStore wrapper...")
        super().__init__(real_store_uri, artifact_uri)

        # Redis connection
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        print("Connected to Redis server on localhost:6379")

    def create_run(self, experiment_id, user_id, start_time, tags, **kwargs):
        event = {'event': 'RUN_CREATED'}
        self.redis_client.publish('mlflow_events', json.dumps(event))
        print("Published RUN_CREATED event 1:", event)
        run = None
        try:
            run = super().create_run(experiment_id, user_id, start_time, tags, **kwargs)
            event.update({'status': 'Successful', 'run_id': run.info.run_id})
        except Exception as e:
            event.update({'status': 'Unsuccessful', 'error': str(e)})
        self.redis_client.publish('mlflow_events', json.dumps(event))
        print("Published RUN_CREATED event 2:", event)
        return run

    def create_model_version(self, name, source, run_id=None, tags=None, **kwargs):
        mv = None
        try:
            mv = super().create_model_version(name=name, source=source, run_id=run_id, tags=tags, **kwargs)
            event = {
                'event': 'MODEL_VERSION_CREATED',
                'model_name': mv.name,
                'version': mv.version,
                'source': mv.source,
                'status': 'Successful'
            }
        except Exception as e:
            event = {
                'event': 'MODEL_VERSION_FAILED',
                'model_name': name,
                'source': source,
                'status': 'Unsuccessful',
                'error': str(e)
            }

        self.redis_client.publish('mlflow_events', json.dumps(event))
        print("Published MODEL_VERSION event:", event)
        return mv
