import os
import subprocess

env = os.environ.copy()
env["MLFLOW_TRACKING_URI"] = "sqlite:///mlflow/mlflow.db"


def serve_model():
    subprocess.run(
        [
            "mlflow",
            "models",
            "serve",
            "--model-uri",
            "./mlflow/best_model/model",
            "--env-manager=local",
            "--port",
            "8080",
        ],
        env=env,
    )


def serve_ui():
    subprocess.run(
        [
            "mlflow",
            "ui",
            "--backend-store-uri",
            "sqlite:///mlflow/mlflow.db",
            "--port",
            "5000",
        ],
        env=env,
    )
