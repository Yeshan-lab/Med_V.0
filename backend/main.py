from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import json

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
MODEL_NAME = "distilgpt2e"
# Use the new router endpoint
API_URL = "https://api-inference.huggingface.co"

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
        "usage": "POST /chat with {'message': 'symptoms'}",
        "model": MODEL_NAME,
        "api_url": API_URL
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": MODEL_NAME, "api_endpoint": "router.huggingface.co"}

def create_prompt(symptoms: str) -> str:
    """Create a medical prompt"""
    return f"""As a healthcare assistant at Suwa Setha Hospital, provide GENERAL information about these symptoms: "{symptoms}"

Include:
1. Basic self-care tips
2. When to consider seeing a doctor
3. Safety reminders

Rules: No diagnosis, no medications, no treatments. Always advise consulting a real doctor.

Response should start with "Based on your symptoms," and be under 150 words."""

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
        
        # Create prompt
        prompt = create_prompt(message)
        
        # Call NEW Hugging Face Router API
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        print(f"Calling Hugging Face Router API for model: {MODEL_NAME}")
        
        try:
            # NEW API ENDPOINT
            response = requests.post(
                f"{API_URL}/models/{MODEL_NAME}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"API Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API Response: {json.dumps(result)[:200]}...")
                
                # Extract text from response
                generated_text = ""
                
                if isinstance(result, list):
                    if len(result) > 0:
                        if isinstance(result[0], dict):
                            generated_text = result[0].get('generated_text', '')
                        else:
                            generated_text = str(result[0])
                elif isinstance(result, dict):
                    generated_text = result.get('generated_text', '')
                    if not generated_text and 'generated_texts' in result:
                        generated_text = result['generated_texts'][0] if result['generated_texts'] else ""
                
                if generated_text and len(generated_text.strip()) > 10:
                    text = generated_text.strip()
                    
                    # Clean up
                    if prompt in text:
                        text = text.replace(prompt, "").strip()
                    
                    # Ensure proper start
                    if not text.lower().startswith("based on your symptoms"):
                        text = f"Based on your symptoms, {text}"
                    
                    # Add safety note if missing
                    if "consult" not in text.lower() and "doctor" not in text.lower():
                        text += "\n\nPlease consult Suwa Setha Hospital or a healthcare provider for proper medical advice."
                    
                    print(f"AI Response: {text[:150]}...")
                    return ChatResponse(response=text)
                else:
                    print("AI response was empty")
            else:
                print(f"API Error {response.status_code}: {response.text[:200]}")
                
                # Try with a different model if first fails
                return try_alternative_model(message)
                
        except requests.exceptions.Timeout:
            print("API timeout")
        except Exception as api_error:
            print(f"API error: {str(api_error)}")
        
        # If we reach here, use dynamic fallback
        return get_dynamic_fallback(message)
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Unexpected error: {e}")
        return get_dynamic_fallback(chat_request.message if 'chat_request' in locals() else "")

def try_alternative_model(symptoms: str):
    """Try with a different model"""
    alternative_models = [
        "distilgpt2",  # Very reliable
        "gpt2",        # Always works
        "microsoft/DialoGPT-small"  # Chat optimized
    ]
    
    prompt = f"Patient: {symptoms}\nHealthcare advice (general only, no diagnosis):"
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150}
    }
    
    for model in alternative_models:
        try:
            print(f"Trying alternative model: {model}")
            response = requests.post(
                f"https://router.huggingface.co/models/{model}",
                headers=headers,
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and result:
                    text = result[0].get('generated_text', '').strip()
                    if text:
                        text = text.replace(prompt, "").strip()
                        if not text.startswith("Based on"):
                            text = f"Based on your symptoms, {text}"
                        return ChatResponse(response=text)
        except:
            continue
    
    # If all models fail, use dynamic fallback
    return get_dynamic_fallback(symptoms)

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
        response = f"""Based on your symptoms mentioning fever:

Fever is often a sign your body is fighting infection. Common causes include viral illnesses like cold or flu.

Self-care suggestions:
• Rest and get adequate sleep
• Drink plenty of fluids (water, herbal tea, broth)
• Monitor your temperature regularly
• Use cool compresses if uncomfortably warm

When to contact a doctor:
• Fever above 102°F (39°C)
• Fever lasting more than 3 days
• Accompanied by rash, stiff neck, or severe headache
• In infants under 3 months

Please consult Suwa Setha Hospital if symptoms concern you. This is general information only."""
    
    elif any(word in symptoms_lower for word in ['headache', 'migraine']):
        response = f"""Based on your headache symptoms:

Headaches can result from various factors including tension, dehydration, stress, eye strain, or sinus issues.

General relief tips:
• Rest in a quiet, dark environment
• Stay well-hydrated throughout the day
• Apply cool compress to forehead or back of neck
• Gentle neck and shoulder stretches

Medical attention recommended if:
• Sudden, severe "thunderclap" headache
• Headache following head injury
• Accompanied by fever, confusion, vision changes, or weakness
• Headaches increasing in frequency or severity

Schedule an appointment at Suwa Setha Hospital for proper evaluation. This information is educational."""
    
    elif any(word in symptoms_lower for word in ['stomach', 'abdomen', 'nausea', 'diarrhea']):
        response = f"""Based on your stomach-related symptoms:

Digestive symptoms can stem from various causes including dietary factors, infections, or digestive conditions.

General guidance:
• Stay hydrated with clear fluids (water, electrolyte drinks)
• Eat bland, easily digestible foods (toast, rice, bananas)
• Avoid spicy, fatty, or heavy meals initially
• Note any food triggers or patterns

Seek medical advice if:
• Severe or persistent abdominal pain
• Vomiting or diarrhea preventing fluid intake
• Symptoms lasting beyond 48 hours
• Blood in stool or vomit

Contact Suwa Setha Hospital for gastrointestinal concerns. This is not medical advice."""
    
    elif any(word in symptoms_lower for word in ['cough', 'cold', 'sore throat', 'congestion']):
        response = f"""Based on your respiratory symptoms:

Common respiratory symptoms often indicate viral infections like colds or flu, but can have other causes.

Self-care approaches:
• Rest to support immune function
• Stay hydrated with warm fluids
• Use humidifier for dry air
• Gargle with warm salt water for sore throat

Consider medical consultation if:
• Difficulty breathing or shortness of breath
• High fever (above 102°F/39°C)
• Symptoms worsening after 3-4 days
• Severe ear pain or sinus pressure

Suwa Setha Hospital can provide proper evaluation. This information is general only."""
    
    else:
        response = f"""Based on your symptoms: "{symptoms[:100]}"

Thank you for describing your health concerns. Monitoring symptoms is important for understanding your health.

General health recommendations:
• Note symptom patterns (timing, triggers, severity)
• Maintain adequate rest and hydration
• Avoid self-medication without professional guidance
• Keep a symptom diary if symptoms persist

When to seek professional medical advice:
• Symptoms that worsen or don't improve
• New or concerning symptoms develop
• Significant discomfort affecting daily activities
• Symptoms persisting beyond reasonable expectation

Please contact Suwa Setha Hospital for personalized medical consultation. This AI provides educational information only."""

    return ChatResponse(response=response)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Suwa Setha Hospital AI Chatbot starting on port {port}")
    print(f"🤖 Using model: {MODEL_NAME}")
    print(f"🔗 API Endpoint: {API_URL}")
    uvicorn.run(app, host="0.0.0.0", port=port)
