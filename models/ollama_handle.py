import ollama
from typing import List

class OllamaChurnAnalyzer:
    def __init__(self, model_name: str = "llama3"):
        self.model = model_name
        self.system_prompt = """Ты аналитик оттока клиентов. Отвечай:
        1. Корректно
        2. С опорой на данные
        3. С рекомендациями"""
    
    def generate_response(self, question: str, context: List[str] = None) -> str:
        """Генерация ответа с учетом контекста"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": question}
        ]
        
        if context:
            messages.insert(1, {
                "role": "assistant",
                "content": "Контекст:\n" + "\n".join(context)
            })
        
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={"temperature": 0.3}
        )
        return response['message']['content']

if __name__ == "__main__":
    analyzer = OllamaChurnAnalyzer()
    print(analyzer.generate_response("Какие клиенты чаще уходят?"))