from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

app = FastAPI(
    title="Suwa Setha Hospital Symptom Checker API",
    description="AI-powered symptom assessment chatbot for academic project",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face API Configuration
HUGGINGFACE_API_KEY = "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"
MODEL_NAME = "google/flan-t5-base"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    disclaimer: str = "⚠️ This chatbot provides general information only and is not a substitute for professional medical advice."

@app.get("/")
def root():
    return {
        "message": "Suwa Setha Hospital AI Symptom Checker API",
        "status": "active"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "model": MODEL_NAME}

def create_prompt(symptoms: str) -> str:
    return f"""You are a healthcare assistant. Patient says: "{symptoms}"

Give general health information about these symptoms:
1. Basic self-care tips
2. Common conditions (possibilities only)
3. When to see a doctor
4. If urgent attention needed

Rules: No diagnosis, no medicines, no treatments. Always say to consult a real doctor.

Start: "Based on your symptoms:"
End: "Please consult a healthcare provider."

Response:"""

@app.post("/chat")
def chat_endpoint(chat_request: ChatRequest):
    try:
        # Validate
        if not chat_request.message or len(chat_request.message.strip()) < 3:
            raise HTTPException(status_code=400, detail="Describe symptoms (min 3 chars)")
        
        if len(chat_request.message) > 300:
            raise HTTPException(status_code=400, detail="Message too long (max 300 chars)")
        
        # Create prompt
        prompt = create_prompt(chat_request.message.strip())
        
        # Call Hugging Face
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200, "temperature": 0.7}
        }
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
            headers=headers,
            json=payload,
            timeout=25
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get('generated_text', '')
                if text and len(text.strip()) > 10:
                    text = text.strip()
                    if not text.startswith("Based on your symptoms:"):
                        text = f"Based on your symptoms: {text}"
                    if "consult" not in text.lower():
                        text += "\n\nPlease consult a healthcare provider."
                    return ChatResponse(response=text)
        
        # Fallback response
        fallback = """Based on your symptoms:

It's important to monitor your health. Common symptoms can have various causes.

General advice:
• Rest and stay hydrated
• Monitor symptom changes
• Avoid self-medication

Seek medical help if:
• Symptoms worsen or persist
• You have severe pain or difficulty breathing
• You're concerned about your health

Please consult Suwa Setha Hospital or your healthcare provider for proper medical advice."""
        
        return ChatResponse(response=fallback)
        
    except Exception as e:
        print(f"Error: {e}")
        fallback = """Based on your symptoms:

Thank you for sharing your symptoms. For proper medical evaluation, please consult with a healthcare professional at Suwa Setha Hospital.

This AI provides general information only and cannot provide medical diagnosis or treatment recommendations.

Please contact Suwa Setha Hospital for professional medical advice."""
        
        return ChatResponse(response=fallback)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
