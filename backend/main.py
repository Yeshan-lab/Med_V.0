from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import random

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

# Initialize the model (will download on first request)
medical_model = None
tokenizer = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    disclaimer: str = "⚠️ Educational tool only. Consult Suwa Setha Hospital for medical advice."

def load_model():
    """Load the model on first request"""
    global medical_model, tokenizer
    if medical_model is None:
        print("Loading medical model...")
        try:
            # Using a smaller model that works locally
            model_name = "google/flan-t5-small"  # Small version works locally
            
            # Alternative models you can try:
            # "microsoft/DialoGPT-small"  # Chat model
            # "distilgpt2"  # Text generation
            
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            medical_model = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                device=-1  # Use CPU (-1), use 0 for GPU if available
            )
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            medical_model = None

@app.get("/")
async def root():
    return {
        "service": "Suwa Setha Hospital AI Symptom Checker API",
        "status": "active",
        "usage": "POST /chat with {'message': 'symptoms'}",
        "note": "Academic project - Emerging Technologies in Healthcare"
    }

@app.get("/health")
async def health_check():
    load_model()
    status = "healthy" if medical_model is not None else "model_loading_failed"
    return {"status": status, "model_loaded": medical_model is not None}

def create_prompt(symptoms: str) -> str:
    """Create a medical prompt"""
    return f"""Patient: {symptoms}

Healthcare Assistant at Suwa Setha Hospital (provide general information only):
- Basic self-care tips
- When to consider seeing a doctor
- Important safety reminders

Rules: No diagnosis, no medications, no treatments. Always advise consulting a real doctor.

Response: Based on your symptoms,"""

@app.post("/chat")
async def chat(chat_request: ChatRequest):
    try:
        # Validate
        message = chat_request.message.strip()
        if not message or len(message) < 3:
            raise HTTPException(status_code=400, detail="Describe symptoms (min 3 characters)")
        
        if len(message) > 300:
            message = message[:300]
        
        print(f"Received: {message}")
        
        # Try to use AI model
        ai_response = try_local_ai(message)
        
        if ai_response:
            # Clean up response
            text = ai_response.strip()
            if not text.lower().startswith("based on your symptoms"):
                text = f"Based on your symptoms, {text}"
            
            # Add safety note if missing
            if "consult" not in text.lower() and "doctor" not in text.lower():
                text += "\n\nPlease consult Suwa Setha Hospital or a healthcare provider for proper medical advice."
            
            print(f"AI Response: {text[:150]}...")
            return ChatResponse(response=text)
        else:
            # Use dynamic fallback
            print("Using dynamic fallback response")
            return get_dynamic_fallback(message)
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Unexpected error: {e}")
        return get_dynamic_fallback(chat_request.message if 'chat_request' in locals() else "")

def try_local_ai(symptoms: str):
    """Try to generate response using local model"""
    try:
        load_model()
        
        if medical_model is None:
            print("Model not loaded, using fallback")
            return None
        
        prompt = create_prompt(symptoms)
        
        # Generate response
        result = medical_model(
            prompt,
            max_length=200,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            num_return_sequences=1
        )
        
        if result and len(result) > 0:
            generated_text = result[0]['generated_text']
            print(f"Generated: {generated_text[:150]}...")
            return generated_text
        
    except Exception as e:
        print(f"Local AI error: {e}")
    
    return None

def get_dynamic_fallback(symptoms: str):
    """Generate context-aware fallback responses"""
    symptoms_lower = symptoms.lower()
    
    # Emergency symptoms
    emergency_keywords = ['chest pain', 'shortness of breath', 'severe pain', 'can\'t breathe', 'unconscious']
    if any(kw in symptoms_lower for kw in emergency_keywords):
        response = """Based on your symptoms, this may require URGENT medical attention.

⚠️ EMERGENCY WARNING: Some symptoms you described could indicate serious conditions.

If experiencing:
• Chest pain, pressure, or tightness
• Difficulty breathing or shortness of breath
• Severe pain anywhere in the body
• Sudden confusion, dizziness, or weakness

Please seek IMMEDIATE medical attention or call emergency services.

For less severe symptoms, contact Suwa Setha Hospital during regular hours.

This information is general. Always consult healthcare professionals for medical concerns."""
    
    elif any(word in symptoms_lower for word in ['fever', 'temperature']):
        responses = [
            """Based on your fever symptoms: Rest, hydrate, and monitor your temperature. If fever persists over 102°F or lasts more than 3 days, consult Suwa Setha Hospital. Common causes include infections.""",
            """Based on your fever: Stay hydrated, get plenty of rest, and avoid spreading germs. Monitor for other symptoms like cough or body aches. Seek medical advice if symptoms worsen."""
        ]
        response = random.choice(responses)
    
    elif any(word in symptoms_lower for word in ['headache', 'migraine']):
        responses = [
            """Based on your headache: Try resting in a quiet place, stay hydrated, and avoid screen time. Common causes include tension, dehydration, or eye strain. Contact Suwa Setha Hospital if severe.""",
            """Based on your headache symptoms: Gentle neck stretches, hydration, and rest may help. Monitor for patterns. Consult if headaches are frequent or severe."""
        ]
        response = random.choice(responses)
    
    elif any(word in symptoms_lower for word in ['stomach', 'abdomen', 'nausea']):
        responses = [
            """Based on your stomach symptoms: Stick to bland foods, stay hydrated, and rest. Avoid spicy or fatty foods initially. If pain is severe or persistent, seek medical evaluation.""",
            """Based on your stomach discomfort: Digestive issues can have various causes. Note any food triggers and monitor symptoms. Consult if symptoms continue or worsen."""
        ]
        response = random.choice(responses)
    
    elif any(word in symptoms_lower for word in ['cough', 'cold', 'sore throat']):
        responses = [
            """Based on your cough: Rest, hydrate, and use a humidifier. Common with respiratory infections. If accompanied by breathing difficulty or high fever, seek medical attention.""",
            """Based on your respiratory symptoms: Stay hydrated, rest, and monitor for fever. Gargle with warm salt water for sore throat. Contact Suwa Setha Hospital if symptoms worsen."""
        ]
        response = random.choice(responses)
    
    else:
        responses = [
            f"""Based on your symptoms: "{symptoms[:50]}"

Thank you for describing your health concerns. Monitoring symptoms is important for understanding your health.

General recommendations:
• Note symptom patterns
• Maintain rest and hydration
• Avoid self-medication

Contact Suwa Setha Hospital for personalized medical consultation.""",
            f"""Based on your symptoms: "{symptoms[:50]}"

It's wise to pay attention to your body and seek professional advice when needed.

Consider:
• Tracking when symptoms occur
• Resting adequately
• Staying hydrated

Please consult Suwa Setha Hospital for proper medical evaluation."""
        ]
        response = random.choice(responses)
    
    return ChatResponse(response=response)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Suwa Setha Hospital AI Chatbot")
    print(f"🔗 Port: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
