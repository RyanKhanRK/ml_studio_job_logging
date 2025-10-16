from setuptools import setup, find_packages

setup(
    name="mlflow-custom-ext",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "mlflow.tracking_store": [
            "notifying-db=mlflow_custom_ext.notifying_store:NotifyingStore"
        ],
    },
)
