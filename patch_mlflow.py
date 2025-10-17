import mlflow.store.model_registry.sqlalchemy_store as registry_store
from mlflow_custom_ext.notifying_store import NotifyingStore

# Keep the original __init__ so we can call it
_original_init = registry_store.SqlAlchemyStore.__init__

def patched_init(self, uri, artifact_uri=None):
    # If our custom scheme, strip it before calling original constructor
    if uri.startswith("notifying-db://"):
        real_uri = uri.split("://", 1)[1]
    else:
        real_uri = uri
    _original_init(self, real_uri, artifact_uri)

# Patch the constructor
registry_store.SqlAlchemyStore.__init__ = patched_init

# Replace the class with your NotifyingStore for notifications
registry_store.SqlAlchemyStore = NotifyingStore

print("MLflow 2.17.2 patched: notifying-db:// will work for model registry")