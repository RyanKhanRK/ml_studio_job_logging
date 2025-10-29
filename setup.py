from setuptools import setup, find_packages

setup(
    name="mlflow-custom-ext",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "mlflow.tracking_store": [
            "notifying-tracking=mlflow_custom_ext.notifying_tracking_store:NotifyingTrackingStore"
        ],
        "mlflow.model_registry_store": [
            "notifying-registry=mlflow_custom_ext.notifying_registry_store:NotifyingRegistryStore"
        ],
    },
)
