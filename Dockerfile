# 1. Use an official Python runtime as a parent image
FROM python:3.10-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application source code
COPY . .

# 5. Install the custom plugin using setup.py
RUN pip install .

# 6. Create directories for artifacts and the database
RUN mkdir mlartifacts

# 7. Expose the port MLflow will run on
EXPOSE 5000

# 8. Define the command to run the MLflow server
#    - We use 0.0.0.0 to allow external connections
#    - We point to the persistent data volumes
CMD ["mlflow", "server", \
     "--backend-store-uri", "notifying-tracking://sqlite:////data/mlflow.db", \
     "--registry-store-uri", "notifying-registry://sqlite:////data/mlflow.db", \
     "--default-artifact-root", "/app/mlartifacts", \
     "--host", "0.0.0.0", \
     "--port", "5000"]
