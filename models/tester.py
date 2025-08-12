from ollama_handle import OllamaChurnExpert
expert = OllamaChurnExpert()
answer = expert.generate_answer("Какие клиенты уходят чаще всего?")
print(answer)