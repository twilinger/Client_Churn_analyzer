from ollama_handle import OllamaChurnExpert
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"     
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"   

expert = OllamaChurnExpert()
answer = expert.generate_answer("describe database sctructure")
print(answer)