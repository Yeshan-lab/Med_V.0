from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

app = FastAPI(
    title="Suwa Setha Hospital Symptom Checker",
    description="AI healthcare assistant - Academic Project",
    version="1.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face config
API_KEY = "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"
MODEL = "google/flan-t5-base"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    disclaimer: str = "⚠️ Educational tool only. Consult Suwa Setha Hospital for medical advice."

@app.get("/")
def home():
    return {
        "service": "Suwa Setha Hospital AI Symptom Checker",
        "status": "active",
        "usage": "POST /chat with {'message': 'symptoms'}"
    }

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL}

@app.post("/chat")
def chat(chat_request: ChatRequest):
    # Validate
    if not chat_request.message or len(chat_request.message.strip()) < 3:
        raise HTTPException(400, "Describe symptoms (min 3 characters)")
    
    # Create prompt
    symptoms = chat_request.message.strip()[:300]
    prompt = f"""Patient: {symptoms}

Healthcare assistant (give general info only):
- Basic self-care tips
- When to see a doctor
- Important: No diagnosis, no medicines recommended
- Always say to consult real doctor

Response: Based on your symptoms,"""
    
    try:
        # Call Hugging Face
        headers = {"Authorization": f"Bearer {API_KEY}"}
        data = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200, "temperature": 0.7}
        }
        
        resp = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL}",
            headers=headers,
            json=data,
            timeout=20
        )
        
        if resp.status_code == 200:
            result = resp.json()
            if isinstance(result, list) and result:
                text = result[0].get('generated_text', '')
                if text:
                    # Clean response
                    text = text.replace(prompt, "").strip()
                    if not text.startswith("Based on your symptoms,"):
                        text = f"Based on your symptoms, {text}"
                    return ChatResponse(response=text)
    except Exception as e:
        print(f"API error: {e}")
    
    # Fallback response
    fallback = """Based on your symptoms:

Thank you for sharing your symptoms. It's important to:
• Monitor your symptoms
• Rest and stay hydrated
• Avoid self-medication

Please consult Suwa Setha Hospital or a healthcare provider for proper medical evaluation.

Remember: This AI provides general information only, not medical diagnosis."""
    
    return ChatResponse(response=fallback)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
