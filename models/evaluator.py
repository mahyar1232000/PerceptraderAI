import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import joblib


def evaluate_model(df: pd.DataFrame, target_column: str, model_path: str = 'models/random_forest_model.pkl') -> dict:
    """
    ارزیابی مدل ذخیره‌شده با استفاده از داده‌های آزمون.

    :param df: DataFrame شامل ویژگی‌ها و هدف
    :param target_column: نام ستون هدف
    :param model_path: مسیر مدل ذخیره‌شده
    :return: دیکشنری شامل معیارهای ارزیابی
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # تقسیم داده‌ها به آموزش و آزمون
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # بارگذاری مدل و نرمال‌ساز
    saved = joblib.load(model_path)
    model = saved['model']
    scaler = saved['scaler']

    # نرمال‌سازی داده‌های آزمون
    X_test_scaled = scaler.transform(X_test)

    # پیش‌بینی و محاسبهٔ معیارها
    y_pred = model.predict(X_test_scaled)
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1_score': f1_score(y_test, y_pred, zero_division=0)
    }
    return metrics
