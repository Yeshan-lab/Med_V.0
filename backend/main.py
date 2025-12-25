from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Hugging Face API Configuration - USING YOUR TOKEN AND MODEL
HUGGINGFACE_API_KEY = "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"  # Your token here
MODEL_NAME = "google/flan-t5-base"  # Using the base model as requested

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    disclaimer: str = "⚠️ This chatbot provides general information only and is not a substitute for professional medical advice. Always consult a healthcare professional at Suwa Setha Hospital for medical concerns."

def create_medical_prompt(user_message: str) -> str:
    """Create a safe, structured prompt for medical guidance"""
    
    prompt = f"""You are a healthcare assistant at Suwa Setha Hospital. A patient says: "{user_message}"

Give general health information about these symptoms:

1. Basic self-care tips
2. Common conditions that might cause such symptoms (these are possibilities only)
3. When to see a doctor
4. If urgent medical attention might be needed

IMPORTANT RULES:
- DO NOT give a diagnosis
- DO NOT recommend medicines
- DO NOT suggest treatments
- ALWAYS say to consult a real doctor
- If symptoms could be serious, say to get emergency help
- Keep response short (under 150 words)

Start with: "Based on your symptoms:"
End with: "Please consult a healthcare provider for proper medical advice."

Response:"""
    
    return prompt

@app.get("/")
async def root():
    return {
        "message": "Suwa Setha Hospital AI Symptom Checker API",
        "status": "active",
        "instructions": "Send POST request to /chat with JSON: {'message': 'your symptoms'}",
        "note": "Academic project - Emerging Technologies in Healthcare"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "symptom-checker-api", "model": MODEL_NAME}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    try:
        # Validate input
        if not chat_request.message or len(chat_request.message.strip()) < 3:
            raise HTTPException(status_code=400, detail="Please describe your symptoms (minimum 3 characters)")
        
        if len(chat_request.message) > 300:
            raise HTTPException(status_code=400, detail="Message too long. Please keep under 300 characters")
        
        # Create the prompt
        prompt = create_medical_prompt(chat_request.message.strip())
        print(f"Prompt: {prompt[:100]}...")
        
        # Call Hugging Face Inference API
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Payload for FLAN-T5 model
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True,
            }
        }
        
        # Make API request
        print(f"Calling Hugging Face API: {MODEL_NAME}")
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
            headers=headers,
            json=payload,
            timeout=25
        )
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            print(f"API Success: {result}")
            
            # Extract generated text
            generated_text = ""
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
            
            # Clean and format response
            if generated_text and len(generated_text.strip()) > 10:
                # Clean up
                generated_text = generated_text.strip()
                
                # Ensure it has proper start
                if not generated_text.startswith("Based on your symptoms:"):
                    generated_text = f"Based on your symptoms: {generated_text}"
                
                # Add safety note if not present
                if "consult a healthcare" not in generated_text.lower():
                    generated_text += "\n\nPlease consult a healthcare provider at Suwa Setha Hospital for proper medical advice."
            else:
                # Use fallback if response is empty
                generated_text = get_fallback_response(chat_request.message).response
                
        else:
            print(f"API Error {response.status_code}: {response.text}")
            # Use fallback response
            generated_text = get_fallback_response(chat_request.message).response
        
        return ChatResponse(response=generated_text)
        
    except requests.exceptions.Timeout:
        print("API timeout - using fallback")
        return get_fallback_response(chat_request.message if 'chat_request' in locals() else "")
    
    except HTTPException as he:
        raise he
    
    except Exception as e:
        print(f"Error: {e}")
        return get_fallback_response(chat_request.message if 'chat_request' in locals() else "")

def get_fallback_response(user_message: str = ""):
    """Return safe fallback responses"""
    
    # Simple keyword-based responses
    if user_message:
        msg_lower = user_message.lower()
        
        emergency_keywords = ['chest pain', 'shortness of breath', 'severe pain', 'can\'t breathe', 'unconscious']
        if any(kw in msg_lower for kw in emergency_keywords):
            response = """Based on your symptoms: 

⚠️ URGENT MEDICAL ATTENTION MAY BE NEEDED

Some symptoms you described could indicate a serious medical condition requiring immediate evaluation.

• If experiencing chest pain, difficulty breathing, severe pain, or loss of consciousness
• Call emergency services or go to the nearest hospital immediately
• Do not wait or attempt to self-treat

For less severe symptoms, please contact Suwa Setha Hospital or your healthcare provider for guidance.

This is not medical advice. Please seek immediate professional medical attention if symptoms are severe."""
        
        elif any(kw in msg_lower for kw in ['fever', 'cough', 'cold', 'flu']):
            response = """Based on your symptoms: 

Common respiratory symptoms like fever, cough, or cold-like symptoms can have various causes, often viral infections.

General self-care:
• Rest and get adequate sleep
• Stay hydrated with water, herbal tea, or broth
• Use a humidifier if you have congestion
• Monitor your temperature

When to see a doctor:
• High fever (above 102°F/39°C)
• Symptoms worsening after 3-4 days
• Difficulty breathing
• Persistent fever beyond 5 days

Please consult a healthcare provider at Suwa Setha Hospital for proper evaluation. This is general information only."""
        
        elif any(kw in msg_lower for kw in ['headache', 'migraine', 'head pain']):
            response = """Based on your symptoms: 

Headaches can result from various factors including tension, dehydration, stress, or underlying conditions.

Self-care tips:
• Rest in a quiet, dark room
• Stay well-hydrated
• Apply cool compress to forehead
• Consider gentle neck stretches

Seek medical attention if:
• Sudden, severe headache
• Headache after head injury
• Headache with fever, stiff neck, or confusion
• New or changing headache patterns

Please consult a healthcare provider for proper assessment. This information is for educational purposes."""
        
        else:
            response = """Based on your symptoms: 

Thank you for describing your symptoms. It's important to monitor any health concerns carefully.

General guidance:
• Note when symptoms occur and what makes them better/worse
• Maintain hydration and adequate rest
• Avoid self-medication without professional advice
• Keep track of symptom progression

When to seek medical help:
• Symptoms that worsen or don't improve
• New or concerning symptoms
• Any symptoms causing significant discomfort
• Symptoms persisting beyond a few days

Please consult with a healthcare professional at Suwa Setha Hospital for personalized medical advice. This is general information only."""
    
    else:
        response = """Based on your symptoms: 

It's important to pay attention to your body and seek medical advice when needed. 

General health tips include adequate rest, proper hydration, and monitoring symptom changes. If symptoms are severe, persistent, or causing concern, please contact Suwa Setha Hospital or your healthcare provider.

Remember that only a qualified medical professional can provide proper diagnosis and treatment recommendations.

Please consult a healthcare provider for medical advice. This chatbot provides general information for educational purposes only."""

    return ChatResponse(response=response)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print("=" * 60)
    print("Suwa Setha Hospital AI Symptom Checker")
    print(f"Using model: {MODEL_NAME}")
    print(f"Server starting on port: {port}")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=port)
