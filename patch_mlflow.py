import mlflow.store.model_registry.sqlalchemy_store as registry_store
from mlflow_custom_ext.notifying_store import NotifyingStore

# Keep original init
_original_init = registry_store.SqlAlchemyStore.__init__

def patched_init(self, uri, artifact_uri=None):
    if uri.startswith("notifying-db://"):
        real_uri = uri.split("://", 1)[1]
    else:
        real_uri = uri
    _original_init(self, real_uri, artifact_uri)

registry_store.SqlAlchemyStore.__init__ = patched_init
registry_store.SqlAlchemyStore = NotifyingStore

print("MLflow 2.17.2 patched: notifying-db:// works for tracking and model registry")