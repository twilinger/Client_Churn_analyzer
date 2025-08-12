import ollama
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent 
sys.path.append(str(project_root))
from db.vector_db import VectorDB


class OllamaChurnExpert:
    def __init__(self):
        self.rag = VectorDB()
        self.model = "llama3"
        
    def generate_answer(self, question: str) -> str:
        context = self.rag.query(question)
        
        prompt = f"""
        Контекст из базы данных:
        {context}
        
        Вопрос аналитика:
        {question}
        
        Сформулируй ответ:
        - Основная причина
        - Подтверждающие данные
        - Рекомендация
        """
        
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]