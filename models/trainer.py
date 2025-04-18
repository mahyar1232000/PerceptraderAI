import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os


def train_model(df: pd.DataFrame, target_column: str, model_path: str = 'models/random_forest_model.pkl') -> None:
    """
    آموزش مدل Random Forest و ذخیرهٔ آن.

    :param df: DataFrame شامل ویژگی‌ها و هدف
    :param target_column: نام ستون هدف
    :param model_path: مسیر ذخیرهٔ مدل
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # تقسیم داده‌ها به آموزش و آزمون
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # نرمال‌سازی ویژگی‌ها
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # آموزش مدل
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # ذخیرهٔ مدل و نرمال‌ساز
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump({'model': model, 'scaler': scaler}, model_path)
