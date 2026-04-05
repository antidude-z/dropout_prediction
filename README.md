# Student Dropout Prediction Pipeline

> An end-to-end MLOps pipeline for predicting student dropout using machine learning.  
> Built for MLOps laboratory assignments #3 and #4.

## Overview

This project implements a complete machine learning pipeline for **binary classification** of student dropout risk. It uses the well-known [Predict Students' Dropout and Academic Success](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success) dataset from the UCI Machine Learning Repository.

The model predicts whether a student is likely to **drop out** (class 1) or **continue their studies** (class 0) based on academic, demographic, and socioeconomic features.

The pipeline includes automated data handling, multiple model training with hyperparameter tuning, inference and MLFlow UI serving, health checks, and Jenkins + Docker CI/CD deployment. The best-performing model (by ROC-AUC) is automatically selected among competitors.

## Models

The pipeline trains and compares four classifiers:
- **Logistic Regression**
- **Random Forest Classifier**
- **XGBoost Classifier**
- **CatBoost Classifier**

Hyperparameter combinations for each model are defined in `src/config.py`.

## Lightweight Mode

> [!IMPORTANT]
> The pipeline supports a `LIGHTWEIGHT` parameter (boolean, default: `false`).

When `LIGHTWEIGHT=true`, the pipeline **excludes the two heavy models (XGBoost and CatBoost)** and trains only Logistic Regression and Random Forest. This mode is significantly faster and recommended for quick tests and development.

You can enable it locally via environment variable or through the Jenkins job parameters.

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

| Command                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `uv run train-model`     | Download data, preprocess, train models, and save artifacts                 |
| `uv run serve-model`     | Serve the best model using MLflow on **port 8080**                          |
| `uv run health-check`    | Run a quick accuracy test on 50 random test samples                         |
| `uv run serve-ui`        | Start the MLflow UI on **port 5000** for experiment tracking                |

#### Example Usage

```bash
# Train the models (full mode by default)
uv run train-model

# Serve the model for inference
uv run serve-model

# Open MLflow UI in another terminal
uv run serve-ui
```

## Jenkins CI/CD Deployment

The repository includes a `Jenkinsfile` for automated deployment.

1. Create a new **Pipeline** job in Jenkins.
2. Set **Definition** to *Pipeline script from SCM*.
3. Choose **Git** and enter the repository URL.
4. Save and run the pipeline.

> [!NOTE]
> The first run may be aborted by Jenkins in order to correctly set pipeline parameters.

On successful completion, two Docker containers will start in the background:
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

**Made with ❤️ by ubiquiste for MLOps learning purposes.**
