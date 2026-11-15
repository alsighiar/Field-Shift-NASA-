import time
import logging
from google import genai 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RAGAgent:
    """
    مسؤول عن الاسترجاع من قاعدة المعرفة (FAISS) وتوليد التفسيرات
    العلمية باستخدام Gemini LLM مع نظام تخطي الأخطاء (Auto-Fallback) ودعم اللغتين.
    """

    def __init__(self, api_key: str, faiss_path: str = "data/faiss_index_real"):
        self.faiss_path = faiss_path
        self.client = genai.Client(api_key=api_key)
        self.retriever = self._load_faiss_retriever()
        self.candidate_models = ['gemini-3.1-flash-lite', 'gemini-1.5-flash', 'gemini-1.5-pro'] 

    def _load_faiss_retriever(self):
        try:
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vector_store = FAISS.load_local(self.faiss_path, embeddings, allow_dangerous_deserialization=True)
            logging.info("FAISS vector database loaded successfully.")
            return vector_store.as_retriever(search_kwargs={"k": 3})
        except Exception as e:
            logging.error(f"Failed to load FAISS index from {self.faiss_path}: {e}")
            raise e

    def generate_explanation(self, sponge_index: float, vpd: float, crop_rec: str, status: str, ai_base: float, sensor_act: float, lang: str = "en") -> str:
        query = f"Water stress, Soil Sponge Index {sponge_index:.2f}, VPD {vpd:.2f} kPa. Why is {crop_rec} recommended?"
        
        # شرط ذكي لتغيير لغة التقرير بناءً على اختيار المستخدم في الواجهة
        lang_instruction = "Write the explanation in English." if lang == "en" else "Write the explanation entirely in Arabic (لغة عربية واضحة ومبسطة للفلاح المصري)."
        
        try:
            relevant_docs = self.retriever.invoke(query)
            context_text = "\n".join([doc.page_content for doc in relevant_docs])
            
            prompt = f"""
            You are an expert agricultural AI assistant for the 'Field Shift' project.
            Use ONLY the following retrieved context from the official FAO-56 document to explain our recommendation to the farmer.
            
            Context (FAO-56):
            {context_text}
            
            Farmer's Scenario:
            - AI Optimal Moisture: {ai_base:.3f}
            - Actual Sensor Moisture: {sensor_act:.3f}
            - Field Status: {status}
            - Recommended Crop: {crop_rec}
            
            Task: Write a 3-sentence professional explanation for the farmer on why {crop_rec} is suitable for these exact conditions based ONLY on the context provided. Do NOT hallucinate.
            {lang_instruction}
            """

            for model_name in self.candidate_models:
                for attempt in range(1, 4):
                    try:
                        logging.info(f"Calling {model_name} (attempt {attempt}/3).")
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=prompt
                        )
                        logging.info(f"RAG explanation generated successfully via {model_name}.")
                        return response.text.strip()
                    
                    except Exception as e:
                        err_msg = str(e)
                        if "503" in err_msg or "429" in err_msg or "UNAVAILABLE" in err_msg:
                            wait_time = attempt * 2
                            logging.warning(f"Server busy. Waiting {wait_time}s before retry.")
                            time.sleep(wait_time)
                        else:
                            logging.warning(f"Skipping {model_name} due to error: {err_msg[:60]}...")
                            break 
            
            error_msg = "System is currently experiencing high load. Please rely on the basic AI recommendation." if lang == "en" else "النظام يواجه ضغطاً حالياً. يرجى الاعتماد على التوصية الأساسية."
            return error_msg
            
        except Exception as e:
            logging.error(f"Error in RAG generation: {e}")
            return "Unable to generate scientific report at this time." if lang == "en" else "تعذر توليد التقرير العلمي في الوقت الحالي."