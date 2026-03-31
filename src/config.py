from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

model_grid = {
    "LogisticRegression": {
        "model": LogisticRegression(max_iter=10000, random_state=42),
        "param_grid": {"C": [0.1, 0.3, 0.8, 2.0]},
        "flavor": "sklearn",
    },
    "RandomForest": {
        "model": RandomForestClassifier(random_state=42, n_jobs=-1),
        "param_grid": {
            "n_estimators": [400, 800],
            "max_depth": [12, 18, None],
            "min_samples_leaf": [1, 2],
        },
        "flavor": "sklearn",
    },
    "XGBoost": {
        "model": XGBClassifier(
            objective="binary:logistic", random_state=42, eval_metric="aucpr"
        ),
        "param_grid": {
            "n_estimators": [400, 800],
            "max_depth": [5, 7, 9],
            "learning_rate": [0.02, 0.05, 0.1],
            "subsample": [0.7, 0.9],
            "colsample_bytree": [0.7, 0.9],
        },
        "flavor": "xgboost",
    },
    "CatBoost": {
        "model": CatBoostClassifier(
            loss_function="Logloss",
            eval_metric="PRAUC",
            random_seed=42,
            verbose=0,
            allow_writing_files=False,
        ),
        "param_grid": {
            "iterations": [500, 900, 1400],
            "depth": [6, 8],
            "learning_rate": [0.03, 0.06, 0.1],
        },
        "flavor": "catboost",
    },
}
