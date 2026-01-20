from fastapi import FastAPI
import ollama

app = FastAPI()

@app.post("/generate")
def generate_text(prompt: str):
    response = ollama.chat(model="ministral-3-3b", messages=[{"role": "user", "content": prompt}])
    return {"response": response['message']['content']}