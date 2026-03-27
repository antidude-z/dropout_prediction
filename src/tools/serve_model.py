import subprocess
import os

os.environ["MLFLOW_TRACKING_URI"] = "sqlite:///mlflow/mlflow.db"

def main():
    subprocess.run([
        "mlflow", "models", "serve",
        "-m", "./mlflow/best_model/model",
        "-p", "8080",
        "--host", "0.0.0.0",
        "--env-manager=local"
    ], env=os.environ.copy())
