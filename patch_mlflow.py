from mlflow.tracking._model_registry.registry import ModelRegistryStoreRegistry
from mlflow_custom_ext.notifying_registry_store import NotifyingRegistryStore

def patch_mlflow():
    # Get the global instance used by MLflow
    registry = ModelRegistryStoreRegistry()
    
    # Register your custom store scheme
    registry.register(
        "notifying-registry",
        lambda store_uri: NotifyingRegistryStore(store_uri)
    )

    print("✅ Patched MLflow with notifying-registry store.")
