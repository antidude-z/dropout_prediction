#!/bin/bash
set -e

docker rm -f ${UI_CONTAINER} 2>/dev/null || true

docker run -d -p 5000:5000 --name ${UI_CONTAINER} -v $(pwd)/mlflow:/app/mlflow ${IMAGE_NAME} \
    mlflow ui --backend-store-uri sqlite:///mlflow/mlflow.db --host 0.0.0.0 --port 5000
