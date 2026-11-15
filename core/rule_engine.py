import os
import json
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RuleEngine:
    """
    مسؤول عن تحديد حالة الحقل (جفاف/غرق) واختيار المحصول المناسب
    من قاعدة البيانات المحلية (JSON) لضمان توصية خالية من الهلوسة.
    """

    def __init__(self, json_path: str = "data/crops_knowledge_base.json"):
        self.json_path = json_path
        self.crops_db = self._load_db()

    def _load_db(self) -> dict:
        """تحميل قاعدة البيانات الخاصة بالمحاصيل."""
        if not os.path.exists(self.json_path):
            logging.error(f"Knowledge Base JSON not found at: {self.json_path}")
            raise FileNotFoundError(f"JSON file is missing: {self.json_path}")
        
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
                logging.info("Crop knowledge base loaded successfully.")
                return db
        except Exception as e:
            logging.error(f"Failed to load JSON database: {e}")
            raise e

    def evaluate_status(self, ai_baseline: float, sensor_reading: float, threshold: float = 0.10) -> Tuple[str, float, str]:
        """
        تستقبل الرطوبة المثالية والقراءة الحالية، وتحسب الفجوة، وتعيد:
        (المحصول المرشح، قيمة الفجوة، الحالة)
        """
        difference = ai_baseline - sensor_reading
        status = ""
        recommended_crop = ""

        try:
            if difference > threshold:
                status = "SEVERE WATER STRESS"
                # الفلترة: اختيار محصول احتياجه للمياه منخفض (Low) مثل الذرة الرفيعة
                recommended_crop = next(
                    (crop for crop, details in self.crops_db.items() if details.get("water_need") == "Low"), 
                    "Sorghum" # قيمة احتياطية
                )
            
            elif difference < -threshold:
                status = "OVER-IRRIGATION"
                # الفلترة: اختيار محصول يتحمل المياه أو احتياجه عالي (High)
                recommended_crop = next(
                    (crop for crop, details in self.crops_db.items() if details.get("water_need") == "High"), 
                    "Corn"
                )
            
            else:
                status = "OPTIMAL"
                recommended_crop = "Wheat" # محصول قياسي في الحالة المثالية

            logging.info(f"Field Status Evaluated: {status} | Recommended: {recommended_crop}")
            return recommended_crop, float(difference), status

        except Exception as e:
            logging.error(f"Error evaluating field status: {e}")
            raise e