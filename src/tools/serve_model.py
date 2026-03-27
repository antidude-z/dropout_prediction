import subprocess

def main():
    subprocess.run([
        "mlflow", "models", "serve",
        "-m", "./mlflow/best_model/model",
        "-p", "8080",
        "--host", "0.0.0.0",
        "--env-manager=local"
    ])
