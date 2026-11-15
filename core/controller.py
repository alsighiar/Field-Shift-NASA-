import logging
import pandas as pd
from typing import Dict, Any

# استدعاء الكلاسات اللي عملناها
from core.data_processor import DataProcessor
from core.ml_engine import PredictiveEngine
from core.rule_engine import RuleEngine
from core.rag_agent import RAGAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FieldShiftController:
    """
    المايسترو الذي يربط جميع وحدات النظام (Data, ML, Rules, RAG)
    ويوفر واجهة واحدة بسيطة للـ Frontend.
    """

    def __init__(self, api_key: str):
        logging.info("Initializing Field Shift Controller...")
        # تهيئة جميع المحركات
        self.ml_engine = PredictiveEngine()
        self.rule_engine = RuleEngine()
        self.rag_agent = RAGAgent(api_key=api_key)
        
        # الـ DataProcessor عبارة عن دوال Static فمش محتاج Initialize

    def run_pipeline(self, raw_input_data: Dict[str, Any], live_sensor_reading: float, lang: str = "en") -> Dict[str, Any]:
        """
        تشغيل دورة النظام الكاملة (End-to-End Pipeline).
        """
        try:
            logging.info("Starting Field Shift pipeline.")
            
            # 1. Feature Engineering (Data Processor)
            features_df = DataProcessor.preprocess_live_data(raw_input_data)
            
            # 2. AI Prediction (CatBoost)
            ai_baseline = self.ml_engine.predict_optimal_moisture(features_df)
            
            # 3. Decision Logic & JSON Filter (Rule Engine)
            crop_rec, deficit, status = self.rule_engine.evaluate_status(ai_baseline, live_sensor_reading)
            
            # 4. Retrieve RAG Context & LLM Explanation (RAG Agent)
            sponge_idx = features_df['Soil_Sponge_Index'].values[0]
            vpd = features_df['VPD_kPa'].values[0]
            
            report = self.rag_agent.generate_explanation(
                sponge_index=sponge_idx,
                vpd=vpd,
                crop_rec=crop_rec,
                status=status,
                ai_base=ai_baseline,
                sensor_act=live_sensor_reading,
                lang=lang
            )
            
            # 5. تجميع النتائج وإرسالها للواجهة
            logging.info("Pipeline executed successfully.")
            return {
                "ai_baseline": ai_baseline,
                "sensor_reading": live_sensor_reading,
                "deficit": deficit,
                "status": status,
                "recommended_crop": crop_rec,
                "fao_report": report
            }
            
        except Exception as e:
            logging.error(f"Pipeline failed: {e}")
            raise e