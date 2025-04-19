import joblib
import os

class ModelLoader:
    @staticmethod
    def save_model(model, filename: str, model_dir="models/saved") -> None:
        os.makedirs(model_dir, exist_ok=True)
        filepath = os.path.join(model_dir, filename)
        joblib.dump(model, filepath)
        print(f"Model saved to {filepath}")

    @staticmethod
    def load_model(filename: str, model_dir="models/saved"):
        filepath = os.path.join(model_dir, filename)
        if os.path.exists(filepath):
            model = joblib.load(filepath)
            print(f"Model loaded from {filepath}")
            return model
        else:
            raise FileNotFoundError(f"No model found at {filepath}")
