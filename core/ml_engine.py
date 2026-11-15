import os
import logging
import pandas as pd
from catboost import CatBoostRegressor

# إعداد الـ Logging عشان لو حصل إيرور في الـ Automation نعرف مكانه
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PredictiveEngine:
    """
    هذا الكلاس مسؤول بالكامل عن تحميل نموذج CatBoost النهائي وإجراء التنبؤات.
    (Single Responsibility Principle)
    """
    
    def __init__(self, model_path: str = "models/Field_Shift_CatBoost_Final.cbm"):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self) -> CatBoostRegressor:
        """دالة داخلية (Private Method) لتحميل الموديل بأمان."""
        if not os.path.exists(self.model_path):
            logging.error(f"Model file not found at: {self.model_path}")
            raise FileNotFoundError(f"Model file is missing: {self.model_path}")
        
        try:
            model = CatBoostRegressor()
            model.load_model(self.model_path)
            logging.info("CatBoost model loaded successfully.")
            return model
        except Exception as e:
            logging.error(f"Failed to load CatBoost model: {e}")
            raise e

    def predict_optimal_moisture(self, features_df: pd.DataFrame) -> float:
        """
        تستقبل بيانات المزرعة (DataFrame) وتعيد الرطوبة المثالية المتوقعة (float).
        """
        try:
            # جلب أول قيمة من المصفوفة الناتجة
            prediction = self.model.predict(features_df)[0]
            logging.info(f"AI Baseline prediction calculated: {prediction:.3f}")
            return float(prediction)
        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            raise e