import subprocess

def main():
    subprocess.run([
        "mlflow", "ui",
        "--backend-store-uri", "sqlite:///mlflow/mlflow.db",
        "--host", "0.0.0.0",
        "--port", "5000"
    ])
