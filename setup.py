from setuptools import setup, find_packages

setup(
    name="mlflow-custom-ext",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "mlflow.tracking_store": [
            "logging-tracking=mlflow_custom_ext.logging_tracking_store:LoggingTrackingStore"
        ],
        "mlflow.model_registry_store": [
            "logging-registry=mlflow_custom_ext.logging_registry_store:LoggingRegistryStore"
        ],
    },
)