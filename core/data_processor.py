import logging
import numpy as np
import pandas as pd
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataProcessor:
    """
    مسؤول عن تحويل البيانات الخام إلى ميزات فيزيائية وزراعية (Feature Engineering)
    لكي تكون جاهزة لنموذج الذكاء الاصطناعي في الوقت الفعلي.
    """

    @staticmethod
    def preprocess_live_data(raw_data: Dict[str, Any]) -> pd.DataFrame:
        """
        تستقبل قاموس (Dictionary) يحتوي على القراءات الحالية وتعيد DataFrame متكامل.
        """
        try:
            # تحويل القاموس إلى DataFrame (صف واحد)
            df = pd.DataFrame([raw_data])

            # 1. الإجهاد الحراري للنبات (Thermal Stress)
            if 'LST_Celsius' in df.columns and 'Temperature_Avg' in df.columns:
                df['Thermal_Stress_Diff'] = df['LST_Celsius'] - df['Temperature_Avg']
            
            # 2. مؤشر عطش الهواء (VPD - Vapor Pressure Deficit)
            if 'Temperature_Avg' in df.columns and 'Relative_Humidity' in df.columns:
                temp = df['Temperature_Avg']
                rh = df['Relative_Humidity']
                svp = 0.6108 * np.exp((17.27 * temp) / (temp + 237.3))
                df['VPD_kPa'] = svp * (1 - (rh / 100))
            
            # 3. مؤشر احتفاظ التربة بالمياه (Soil Sponge Index)
            if 'Soil_Clay_pct' in df.columns and 'Soil_Sand_pct' in df.columns:
                df['Soil_Sponge_Index'] = df['Soil_Clay_pct'] / (df['Soil_Sand_pct'] + 1e-5)

            # ترتيب الأعمدة بنفس الترتيب الذي تدرب عليه نموذج CatBoost لضمان عدم حدوث خطأ
            expected_features = [
                'Temperature_Avg', 'Relative_Humidity', 'Precipitation', 'NDVI',
                'LST_Celsius', 'Soil_Sand_pct', 'Soil_Clay_pct', 'Crop_Kc',
                'Thermal_Stress_Diff', 'VPD_kPa', 'Soil_Sponge_Index',
                'Month', 'DayOfYear', 'Rain_3d_sum', 'LST_5d_avg'
            ]
            
            # التحقق من وجود كل الأعمدة المطلوبة
            missing_cols = [col for col in expected_features if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required features for prediction: {missing_cols}")

            logging.info("Live data preprocessed and physical equations applied successfully.")
            return df[expected_features]

        except Exception as e:
            logging.error(f"Error in data preprocessing: {e}")
            raise e