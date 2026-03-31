import shutil
from pathlib import Path

import mlflow
from mlflow.tracking import MlflowClient
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    average_precision_score,
    f1_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.utils.class_weight import compute_sample_weight

# Загрузка и подготовка данных (бинарная классификация: Dropout = 1)
from config import model_grid
from preprocessing import prepare_student_data

mlflow.set_tracking_uri("sqlite:///mlflow/mlflow.db")


def train():
    shutil.rmtree("./mlflow", ignore_errors=True)
    Path("./mlflow").mkdir(exist_ok=True)

    X_train, X_test, y_train, y_test, signature = prepare_student_data()

    experiment_name = "Student_Dropout"
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        mlflow.create_experiment(experiment_name, artifact_location="./mlflow/mlruns")

    mlflow.set_experiment(experiment_name)

    sample_weights = compute_sample_weight(class_weight="balanced", y=y_train)
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

    best_score = -float("inf")
    best_run_id = None
    best_model_name = None

    for model_name, cfg in model_grid.items():
        print(f"\n=== {model_name} ===")

        with mlflow.start_run(run_name=model_name):
            grid = GridSearchCV(
                estimator=cfg["model"],
                param_grid=cfg["param_grid"],
                cv=cv,
                scoring="roc_auc",
                n_jobs=-1 if cfg["flavor"] == "sklearn" else 1,
                verbose=1,
            )

            grid.fit(X_train, y_train, sample_weight=sample_weights)
            best_model = grid.best_estimator_

            y_pred = best_model.predict(X_test)
            y_proba = best_model.predict_proba(X_test)[:, 1]

            metrics = {
                "test_f1": f1_score(y_test, y_pred),
                "test_recall": recall_score(y_test, y_pred),
                "test_roc_auc": roc_auc_score(y_test, y_proba),
                "test_prauc": average_precision_score(y_test, y_proba),
            }

            mlflow.log_params(grid.best_params_)
            mlflow.log_metrics(metrics)

            getattr(mlflow, cfg["flavor"]).log_model(
                best_model,
                name="model",
                signature=signature,
                input_example=X_train.iloc[:5].copy(),
            )

            disp = ConfusionMatrixDisplay.from_predictions(
                y_test, y_pred, display_labels=["Остаётся", "Отчислен"], cmap="Blues"
            )
            mlflow.log_figure(
                figure=disp.figure_, artifact_file=f"confusion_matrix_{model_name}.png"
            )

            print(f"Test ROC AUC: {metrics['test_roc_auc']:.4f}")
            print(f"Best CV ROC AUC: {grid.best_score_:.4f}")

            if metrics["test_roc_auc"] > best_score:
                best_score = metrics["test_roc_auc"]
                best_run_id = mlflow.active_run().info.run_id
                best_model_name = model_name

    print("\n=== Downloading Best Model ===")
    print(f"Best model: '{best_model_name}' (ROC AUC = {best_score:.4f})")

    client = MlflowClient()
    client.download_artifacts(
        run_id=best_run_id, path="model", dst_path="./mlflow/best_model"
    )


if __name__ == "__main__":
    train()
