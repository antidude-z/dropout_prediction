#!/bin/bash
set -e

docker run --rm -v $(pwd)/mlflow:/app/mlflow ${IMAGE_NAME} python -u train_model.py
