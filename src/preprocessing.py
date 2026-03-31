import pandas as pd
from mlflow.models import infer_signature
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from ucimlrepo import fetch_ucirepo


def prepare_student_data(test_size=0.2, random_state=42):
    # 1. Загрузка данных
    df = fetch_ucirepo(id=697).data.original

    # 2. Целевая переменная
    y = (df["Target"] == "Dropout").astype(int)
    X = df.drop(columns=["Target"])

    # 3. Категориальные и числовые признаки
    categorical_cols = [
        "Marital Status",
        "Application mode",
        "Application order",
        "Course",
        "Daytime/evening attendance",
        "Previous qualification",
        "Nacionality",
        "Mother's qualification",
        "Father's qualification",
        "Mother's occupation",
        "Father's occupation",
        "Displaced",
        "Educational special needs",
        "Debtor",
        "Tuition fees up to date",
        "Gender",
        "Scholarship holder",
        "International",
    ]
    numeric_cols = [col for col in X.columns if col not in categorical_cols]

    # 4. Разделение на train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    # 5. Кодирование категориальных признаков
    X_train = pd.get_dummies(X_train, columns=categorical_cols, drop_first=True)
    X_test = pd.get_dummies(X_test, columns=categorical_cols, drop_first=True)
    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

    # 6. Масштабирование числовых признаков
    scaler = StandardScaler()
    X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

    # 7. Инференс подписи
    small_X = X_train.iloc[:100]
    small_y = y_train.iloc[:100]
    res = LogisticRegression().fit(small_X, small_y).predict(small_X)
    signature = infer_signature(small_X, res)

    return X_train, X_test, y_train, y_test, signature
