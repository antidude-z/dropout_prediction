import subprocess


def serve_model():
    subprocess.run([
        "mlflow", "models", "serve",
        "--model-uri", "./mlflow/best_model/model",
        "--env-manager=local",
        "--port", "8080"
    ], env={'MLFLOW_TRACKING_URI': "sqlite:///mlflow/mlflow.db"})


def serve_ui():
    subprocess.run([
        "mlflow", "ui",
        "--backend-store-uri", "sqlite:///mlflow/mlflow.db",
        "--port", "5000"
    ])
