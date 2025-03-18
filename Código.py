from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import json
import os


openai.api_key = os.getenv("")
app = FastAPI()

# anco de dados
KEYWORD_DB = {
    "banana": 3,
    "maçã": 5,
    "carro": 8
}

# Modelo de entrada
class TextInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(input_data: TextInput):
    """
    Recebe um texto, usa a LLM para extrair palavras-chave e retorna os IDs dos vídeos.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Extraia palavras-chave relevantes do texto e retorne em JSON."},
                {"role": "user", "content": input_data.text}
            ]
        )
        
        keywords = json.loads(response["choices"][0]["message"]["content"])
        video_ids = [KEYWORD_DB[key] for key in keywords if key in KEYWORD_DB]
        
        return {"video_ids": video_ids}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "API de Identificação de Palavras-chave Rodando!"}

