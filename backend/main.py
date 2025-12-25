from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time
import os  # ⬅️ ADD THIS IMPORT
from model_loader import medical_ai, test_model

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

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    disclaimer: str = "⚠️ Educational tool only. Consult Suwa Setha Hospital for medical advice."

# Pre-load model on startup
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Suwa Setha Hospital AI Chatbot...")
    print("🔄 Pre-loading medical model (might take 30-60 seconds)...")
    
    # Try to load model in background
    import threading
    def load_model_background():
        success = medical_ai.load_model()
        if success:
            print("✅ Model pre-loaded successfully!")
            # Test the model
            test_response = test_model()
            if test_response:
                print(f"🤖 Test generation: {test_response[:50]}...")
        else:
            print("⚠️ Model loading failed, will use fallback responses")
    
    # Start loading in background
    thread = threading.Thread(target=load_model_background)
    thread.daemon = True
    thread.start()

@app.get("/")
async def root():
    return {
        "service": "Suwa Setha Hospital AI Symptom Checker API",
        "status": "active",
        "usage": "POST /chat with {'message': 'symptoms'}",
        "model_loaded": medical_ai.model_loaded,
        "note": "Academic project - Emerging Technologies in Healthcare"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": medical_ai.model_loaded,
        "service": "medical_ai_chatbot"
    }

def create_medical_prompt(symptoms: str) -> str:
    """Create a prompt for medical advice"""
    return f"""Patient symptoms: {symptoms}

As a healthcare assistant at Suwa Setha Hospital, provide GENERAL health information about these symptoms.

Include:
1. Basic self-care tips
2. When to consider seeing a doctor
3. Important safety reminders

IMPORTANT RULES:
- DO NOT give medical diagnosis
- DO NOT recommend specific medications
- DO NOT suggest treatment plans
- ALWAYS advise consulting a real doctor

Start response with: "Based on your symptoms,"

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
        
        print(f"📝 Received: {message}")
        
        # Try AI model first
        ai_response = None
        if medical_ai.model_loaded:
            prompt = create_medical_prompt(message)
            print(f"🤖 Generating AI response...")
            
            try:
                ai_response = medical_ai.generate_response(prompt)
                if ai_response:
                    print(f"✅ AI generated: {ai_response[:100]}...")
            except Exception as e:
                print(f"❌ AI generation failed: {e}")
        
        # If AI worked, use it
        if ai_response and len(ai_response.strip()) > 20:
            text = ai_response.strip()
            
            # Clean up
            if "Based on your symptoms," not in text:
                text = f"Based on your symptoms, {text}"
            
            # Ensure safety disclaimer
            if "consult" not in text.lower() and "doctor" not in text.lower():
                text += "\n\nPlease consult Suwa Setha Hospital or a healthcare provider for proper medical advice."
            
            return ChatResponse(response=text)
        
        # Otherwise use intelligent fallback
        print("📋 Using intelligent fallback response")
        return get_intelligent_fallback(message)
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return get_intelligent_fallback(chat_request.message if 'chat_request' in locals() else "")

def get_intelligent_fallback(symptoms: str):
    """Smart fallback responses that sound like AI"""
    symptoms_lower = symptoms.lower()
    
    # Check emergency first
    emergency_keywords = ['chest pain', 'shortness of breath', 'severe pain', 'can\'t breathe', 'unconscious']
    if any(kw in symptoms_lower for kw in emergency_keywords):
        response = """Based on your symptoms: ⚠️ URGENT MEDICAL ATTENTION MAY BE REQUIRED

Some symptoms you described could indicate serious conditions requiring immediate evaluation.

If experiencing:
• Chest pain, pressure, or tightness
• Difficulty breathing or shortness of breath
• Severe pain anywhere
• Sudden confusion, dizziness, or weakness

Please seek EMERGENCY medical attention immediately.

For less severe symptoms, contact Suwa Setha Hospital during regular hours.

⚠️ This is general information only. Always consult healthcare professionals."""
    
    # Fever responses
    elif any(word in symptoms_lower for word in ['fever', 'temperature', 'hot', 'chills']):
        responses = [
            """Based on your fever symptoms: This often indicates your body is fighting infection. General care includes rest, hydration with fluids like water or broth, and temperature monitoring. Contact Suwa Setha Hospital if fever exceeds 102°F, persists beyond 3 days, or is accompanied by concerning symptoms.""",
            
            """Based on your elevated temperature: Common causes include viral or bacterial infections. Self-management: adequate rest, maintain hydration, light clothing. Seek medical advice if: fever is very high, persistent, or accompanied by other severe symptoms."""
        ]
        response = random.choice(responses)
    
    # Headache responses
    elif any(word in symptoms_lower for word in ['headache', 'migraine', 'head pain']):
        responses = [
            """Based on your headache: Possible factors include tension, dehydration, eye strain, or sinus issues. Relief strategies: rest in quiet environment, stay hydrated, apply cool compress. Consult Suwa Setha Hospital if headaches are severe, sudden, or accompanied by vision changes or confusion.""",
            
            """Based on your headache symptoms: Many elements can contribute including stress, posture, or environmental factors. General advice: ensure hydration, manage stress, take screen breaks. Medical evaluation recommended for persistent or unusually severe headaches."""
        ]
        response = random.choice(responses)
    
    # Stomach responses
    elif any(word in symptoms_lower for word in ['stomach', 'abdomen', 'nausea', 'vomit', 'diarrhea']):
        responses = [
            """Based on your stomach symptoms: Digestive discomfort can stem from dietary factors, infections, or digestive conditions. Initial management: bland foods (toast, rice, bananas), maintain hydration, avoid spicy/fatty foods. Seek medical advice if symptoms are severe, persistent, or prevent fluid intake.""",
            
            """Based on your abdominal discomfort: Common considerations include indigestion, food sensitivities, or gastrointestinal issues. Self-care: note food triggers, smaller meals, clear fluids. Professional evaluation recommended for severe pain or persistent symptoms."""
        ]
        response = random.choice(responses)
    
    # Cough/cold responses
    elif any(word in symptoms_lower for word in ['cough', 'cold', 'sore throat', 'congestion']):
        responses = [
            """Based on your respiratory symptoms: Often associated with infections, allergies, or irritants. General care: warm fluids, humidifier, rest, avoid smoke. Contact Suwa Setha Hospital if symptoms are severe, persistent beyond 2 weeks, or include breathing difficulty.""",
            
            """Based on your cough: Common with respiratory conditions. Suggestions: honey in warm tea may soothe, adequate rest supports recovery. Medical consultation advised if coughing causes chest pain, breathing problems, or doesn't improve."""
        ]
        response = random.choice(responses)
    
    # Default intelligent response
    else:
        responses = [
            f"""Based on your symptoms: "{symptoms[:80]}"

Thank you for sharing your health concerns. Monitoring symptoms is important for health maintenance.

General recommendations:
• Note symptom patterns and triggers
• Maintain adequate rest and hydration
• Avoid self-medication without professional advice

Please consider scheduling an appointment at Suwa Setha Hospital for personalized medical evaluation.""",
            
            f"""Based on your symptoms: "{symptoms[:80]}"

It's important to pay attention to bodily changes and seek appropriate medical guidance when needed.

Tracking symptom details can be helpful:
• When symptoms occur
• What makes them better or worse
• Any associated factors

Suwa Setha Hospital healthcare providers can offer professional assessment and advice for your specific situation."""
        ]
        response = random.choice(responses)
    
    return ChatResponse(response=response)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    
    print("=" * 60)
    print("🏥 Suwa Setha Hospital AI Symptom Checker")
    print(f"🔗 Port: {port}")
    print(f"🤖 Model loaded: {medical_ai.model_loaded}")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=port)
