from fastapi import FastAPI
import ollama

app = FastAPI()

@app.post("/generate") # Endpoint to generate text using the ministral-3-3b model
def generate_text(prompt: str):
    response = ollama.chat(model="ministral-3-3b", messages=[{"role": "user", "content": prompt}]) # Call the Ollama API with the specified model and prompt
    return {"response": response['message']['content']} # Return the generated text in the response