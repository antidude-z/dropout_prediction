# Student Dropout Prediction Pipeline

<image-card alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" ></image-card>
<image-card alt="MLflow" src="https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white" ></image-card>
<image-card alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" ></image-card>

> An end-to-end MLOps pipeline for predicting student dropout using machine learning.  
> Built for MLOps laboratory assignments #3 and #4.

## Overview

This project implements a complete machine learning pipeline for **binary classification** of student dropout risk. It uses the well-known [Predict Students' Dropout and Academic Success](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success) dataset from the UCI Machine Learning Repository.

The model predicts whether a student is likely to **drop out** (class 1) or **continue their studies** (class 0) based on academic, demographic, and socioeconomic features.

The pipeline includes:
- Automated data downloading and preprocessing
- Training and hyperparameter tuning of multiple models
- Model selection based on **ROC-AUC**
- Model serving with MLflow
- Health checks and MLflow UI
- CI/CD deployment via Jenkins + Docker

## Important: LIGHTWEIGHT Mode

The pipeline supports a **`LIGHTWEIGHT`** parameter (boolean).  

- **LIGHTWEIGHT=true** → Trains only a small subset of models with limited hyperparameter combinations. Much faster, ideal for quick tests and development.
- **LIGHTWEIGHT=false** (default) → Trains all models with full hyperparameter search (slower but better performance).

This parameter is especially useful in the Jenkins pipeline (set it in the job parameters) and can also be passed locally via environment variable.

## Models

By default, the pipeline trains and compares four classifiers:
- **Logistic Regression**
- **Random Forest Classifier**
- **XGBoost Classifier**
- **CatBoost Classifier**

Each model is evaluated with multiple hyperparameter combinations defined in `src/config.py`. The best-performing model (by ROC-AUC) is automatically selected and registered for serving.

## Quick Start (Local Deployment)

### Prerequisites
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Git
- Python 3.10+

### Installation

```bash
git clone https://github.com/antidude-z/dropout_prediction.git
cd dropout_prediction
uv sync
```

### Available Commands

| Command                        | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| `uv run train-model`           | Train models (uses LIGHTWEIGHT=false by default)                            |
| `LIGHTWEIGHT=true uv run train-model` | Train in lightweight/fast mode                                      |
| `uv run serve-model`           | Serve the best model using MLflow on **port 8080**                          |
| `uv run health-check`          | Run a quick accuracy test on 50 random test samples                         |
| `uv run serve-ui`              | Start the MLflow UI on **port 5000** for experiment tracking                |

#### Example Usage

```bash
# Full training (recommended for best results)
uv run train-model

# Fast training for testing
LIGHTWEIGHT=true uv run train-model

# Serve the model for inference
uv run serve-model

# Open MLflow UI in another terminal
uv run serve-ui
```

## Jenkins CI/CD Deployment

The repository includes a `Jenkinsfile` for automated deployment.

When creating the Pipeline job in Jenkins:
- You will see a **LIGHTWEIGHT** parameter in the job UI.
- Set it to `true` for faster builds during development.
- Set it to `false` for full training (better model quality).

On successful completion, two Docker containers will start:
- **`ml_model`** — serves model inference on **port 8080**
- **`mlflow_ui`** — provides the MLflow dashboard on **port 5000**

Containers are recreated on every pipeline run.

## Project Structure

```
dropout_prediction/
├── src/                  # Main source code (training, preprocessing, config)
├── docker/               # Dockerfile and related scripts
├── mlflow/               # Trained models and artifacts (generated)
├── Jenkinsfile           # CI/CD pipeline definition
├── pyproject.toml        # Project & dependency configuration
├── uv.lock
└── README.md
```

## Technologies Used

- **Python** + `uv` for dependency management
- **scikit-learn**, **XGBoost**, **CatBoost**
- **MLflow** (experiment tracking + model serving)
- **Docker** for containerization
- **Jenkins** for CI/CD

## Dataset

- Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)
- Task: Binary classification (Dropout vs. Non-Dropout)

---

**Made with ❤️ for MLOps learning purposes.**

Feel free to open issues or submit pull requests!
