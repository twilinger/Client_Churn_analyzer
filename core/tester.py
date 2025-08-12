from ollama_handle import OllamaChurnExpert
expert = OllamaChurnExpert()
answer = expert.generate_answer("describe database sctructure")
print(answer)