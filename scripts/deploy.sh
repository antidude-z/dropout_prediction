#!/bin/bash
set -e

docker rm -f ${MODEL_CONTAINER} 2>/dev/null || true

docker run -d -p 8080:8080 --name ${MODEL_CONTAINER} -v $(pwd)/mlflow:/app/mlflow ${IMAGE_NAME} \
    mlflow models serve -m /app/mlflow/best_model/model -p 8080 --host 0.0.0.0 --env-manager=local