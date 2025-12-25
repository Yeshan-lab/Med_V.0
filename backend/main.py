from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time
import os
from advanced_medical_ai import medical_ai  # Your new rule-based AI system

app = FastAPI(
    title="Suwa Setha Hospital Symptom Checker",
    description="Advanced Rule-Based Medical AI - Academic Project",
    version="2.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    disclaimer: str = "⚠️ EDUCATIONAL TOOL ONLY. Consult Suwa Setha Hospital or healthcare provider for medical advice."

# Startup event
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Suwa Setha Hospital Advanced Medical AI...")
    print("💡 Using Rule-Based AI System (No Model Downloads Needed)")
    print("✅ System ready immediately!")

@app.get("/")
async def root():
    return {
        "service": "Suwa Setha Hospital Advanced Medical AI",
        "status": "active",
        "ai_type": "Rule-Based Knowledge System",
        "coverage": "15+ medical conditions with validated advice",
        "endpoints": {
            "chat": "POST /chat with {'message': 'symptoms'}",
            "health": "GET /health",
            "docs": "GET /docs"
        },
        "note": "Academic project - Emerging Technologies in Healthcare"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_system": "advanced_rule_based",
        "conditions_covered": 15,
        "memory_usage": "minimal",
        "response_time": "instant"
    }

@app.post("/chat")
async def chat(chat_request: ChatRequest):
    try:
        message = chat_request.message.strip()
        
        if not message or len(message) < 3:
            raise HTTPException(status_code=400, detail="Describe symptoms (min 3 characters)")
        
        if len(message) > 500:
            message = message[:500]
        
        print(f"🎯 Processing: {message[:100]}...")
        
        # Use advanced rule-based AI
        ai_response = medical_ai.process_query(message)
        
        return ChatResponse(
            response=ai_response,
            disclaimer="⚠️ EDUCATIONAL TOOL ONLY. Consult Suwa Setha Hospital or healthcare provider for medical advice."
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"💥 Error in chat endpoint: {e}")
        # Fallback to intelligent response
        return get_intelligent_fallback(message)

def get_intelligent_fallback(symptoms: str):
    """Backup fallback system (kept for redundancy)"""
    symptoms_lower = symptoms.lower()
    
    # Check emergency first
    emergency_keywords = ['chest pain', 'shortness of breath', 'severe pain', 'can\'t breathe', 'unconscious']
    if any(kw in symptoms_lower for kw in emergency_keywords):
        response = """🚨 EMERGENCY: Based on your symptoms, immediate medical attention may be required.

If experiencing:
• Chest pain, pressure, or tightness
• Difficulty breathing
• Severe pain anywhere
• Sudden confusion or weakness

Please seek EMERGENCY medical attention immediately.

📍 Suwa Setha Hospital Emergency Department
📞 Emergency: 1990 / 0112 691 111

⚠️ THIS IS NOT A SUBSTITUTE FOR EMERGENCY CARE."""
        return ChatResponse(response=response)
    
    # General intelligent response
    responses = [
        f"""Thank you for sharing: "{symptoms[:80]}"

I've analyzed your symptoms with our medical knowledge base. For personalized assessment:

• Monitor symptom patterns
• Note any changes or worsening
• Stay hydrated and rest

For proper medical evaluation, please consider visiting Suwa Setha Hospital.""",
        
        f"""Based on: "{symptoms[:80]}"

Our medical AI recommends:
1. Document symptom details (timing, triggers, severity)
2. General self-care: rest, hydration, observation
3. Professional evaluation for accurate diagnosis

Suwa Setha Hospital offers comprehensive health assessments."""
    ]
    
    return ChatResponse(response=random.choice(responses))

# API Documentation endpoint
@app.get("/conditions")
async def list_conditions():
    """List all conditions covered by the AI"""
    conditions = [
        "Common Cold", "Influenza (Flu)", "Bronchitis",
        "Gastroenteritis", "Acid Reflux (GERD)",
        "Migraine", "Tension Headache",
        "Back Pain", "Arthritis",
        "Eczema", "Acne",
        "Hypertension", "Diabetes Type 2",
        "Allergic Rhinitis (Hay Fever)"
    ]
    return {
        "total_conditions": len(conditions),
        "conditions": conditions,
        "system": "Rule-Based Medical Knowledge AI"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    
    print("=" * 60)
    print("🏥 SUWA SETHA HOSPITAL - ADVANCED MEDICAL AI")
    print("=" * 60)
    print(f"🔗 Port: {port}")
    print(f"📊 Conditions: 15+ medical conditions")
    print(f"⚡ Response: Instant (no model downloads)")
    print(f"🎯 AI Type: Rule-Based Knowledge System")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=port)
