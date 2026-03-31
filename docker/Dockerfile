FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY ./docker/requirements/ .
COPY ./docker/scripts/install.sh .

ARG LIGHTWEIGHT=false
RUN sh install.sh

COPY src/ .

ENV MLFLOW_TRACKING_URI=sqlite:///mlflow/mlflow.db
ENV LIGHTWEIGHT=${LIGHTWEIGHT}
