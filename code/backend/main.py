from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from supabase import create_client, Client
from transformers import AutoTokenizer, AutoModelForCausalLM

# Initialize FastAPI app
app = FastAPI()

# Load Mistral-7B Model
model_name = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Supabase setup (replace with your Supabase keys)
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class ChatRequest(BaseModel):
    message: str

# Chatbot route
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        inputs = tokenizer(request.message, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=150)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Calendar events route
@app.get("/events")
def get_events():
    try:
        response = supabase.table("events").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root route
@app.get("/")
def home():
    return {"message": "AI-Twin Backend is running!"}
