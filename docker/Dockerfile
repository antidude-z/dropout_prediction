FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY ./docker/requirements.txt .
COPY ./docker/extension.txt .

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ARG LIGHTWEIGHT=false
RUN if [ "$LIGHTWEIGHT" = "false" ]; then \
        pip install --no-cache-dir -r extension.txt; \
    fi

COPY src/ .

ENV MLFLOW_TRACKING_URI=sqlite:///mlflow/mlflow.db
ENV LIGHTWEIGHT=${LIGHTWEIGHT}
