from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

# Initialize FastAPI
app = FastAPI(
    title="Suwa Setha Hospital Symptom Checker",
    description="AI Healthcare Assistant - Academic Project",
    version="1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
HUGGINGFACE_API_KEY = "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"
MODEL_NAME = "google/flan-t5-base"

# Pydantic 1.x Models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    disclaimer: str = "⚠️ Educational tool only. Consult Suwa Setha Hospital for medical advice."

@app.get("/")
async def root():
    return {
        "service": "Suwa Setha Hospital AI Symptom Checker API",
        "status": "active",
        "usage": "POST /chat with {'message': 'symptoms'}"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": MODEL_NAME}

def create_prompt(symptoms: str) -> str:
    return f"""You are a healthcare assistant. Patient says: "{symptoms}"

Provide general health information only:
- Basic self-care tips
- When to see a doctor
- No diagnosis, no medicines
- Always recommend consulting a real doctor

Start with: "Based on your symptoms,"

Response:"""

@app.post("/chat")
async def chat(chat_request: ChatRequest):
    try:
        # Validate
        message = chat_request.message.strip()
        if not message or len(message) < 3:
            raise HTTPException(status_code=400, detail="Describe symptoms (min 3 characters)")
        
        if len(message) > 300:
            message = message[:300]
        
        # Create prompt
        prompt = create_prompt(message)
        
        # Call Hugging Face API
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200, "temperature": 0.7}
        }
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
            headers=headers,
            json=payload,
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and result:
                text = result[0].get('generated_text', '').strip()
                if text and len(text) > 10:
                    # Clean up response
                    if text.startswith(prompt):
                        text = text[len(prompt):].strip()
                    if not text.startswith("Based on your symptoms,"):
                        text = f"Based on your symptoms, {text}"
                    return ChatResponse(response=text)
        
        # Fallback response
        fallback = """Based on your symptoms, here is general health information:

It's important to monitor your symptoms carefully. Common symptoms can have various causes.

General self-care:
• Rest and stay hydrated
• Monitor for any changes
• Avoid self-medication

When to seek medical help:
• Symptoms worsen or don't improve
• Severe pain or difficulty breathing
• Symptoms persist beyond a few days

Please consult Suwa Setha Hospital or a healthcare provider for proper medical evaluation.

⚠️ Remember: This AI provides general information only, not medical diagnosis."""
        
        return ChatResponse(response=fallback)
        
    except requests.exceptions.Timeout:
        fallback = """Based on your symptoms:

Thank you for sharing your symptoms. For proper medical advice, please contact Suwa Setha Hospital directly.

This AI assistant provides general health information for educational purposes only.

Please consult with a healthcare professional for medical evaluation."""
        return ChatResponse(response=fallback)
        
    except Exception as e:
        print(f"Error: {e}")
        fallback = """Based on your symptoms:

It's important to seek proper medical advice for health concerns. 

Please contact Suwa Setha Hospital for professional medical evaluation.

This is an educational AI tool providing general information only."""
        return ChatResponse(response=fallback)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
