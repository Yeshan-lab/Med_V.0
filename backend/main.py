from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import json
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
    allow_origins=["*"],  # For production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face API Configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"  # Free model with good instruction following

# Alternative models you can try:
# - "google/flan-t5-xxl"
# - "microsoft/DialoGPT-medium"
# - "distilgpt2"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    disclaimer: str = "This chatbot provides general information only and is not a substitute for professional medical advice. Always consult a healthcare professional for medical concerns."

def create_medical_prompt(user_message: str) -> str:
    """Create a safe, structured prompt for medical guidance"""
    
    prompt = f"""You are a healthcare support assistant at Suwa Setha Hospital. Your role is to provide GENERAL health guidance and information based on symptoms described.

User symptoms: "{user_message}"

Please provide:
1. **General Health Guidance**: Basic self-care tips that might help
2. **Possible Causes**: Common conditions associated with these symptoms (mention these are POSSIBILITIES only)
3. **When to Seek Help**: Clear advice on when to consult a medical professional
4. **Urgency Level**: Indicate if this might require urgent attention (emergency/non-emergency)

IMPORTANT SAFETY RULES:
- DO NOT provide a diagnosis
- DO NOT recommend specific medications
- DO NOT suggest treatment plans
- ALWAYS emphasize consulting a real doctor
- Be cautious and conservative in your advice
- If symptoms could be serious, clearly state to seek immediate medical attention
- Keep response under 250 words

Response format:
Start with: "Based on your symptoms, here is some general information:"
End with: "Please consult a healthcare professional for proper medical advice."

Now provide your response:"""
    
    return prompt

@app.get("/")
async def root():
    return {
        "message": "Suwa Setha Hospital AI Symptom Checker API",
        "status": "active",
        "instructions": "Send POST request to /chat with JSON: {'message': 'your symptoms'}",
        "note": "This is an academic project for educational purposes only"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    try:
        # Validate input
        if not chat_request.message or len(chat_request.message.strip()) < 3:
            raise HTTPException(status_code=400, detail="Please describe your symptoms")
        
        if len(chat_request.message) > 500:
            raise HTTPException(status_code=400, detail="Message too long. Please keep under 500 characters")
        
        # Create the prompt
        prompt = create_medical_prompt(chat_request.message)
        
        # Call Hugging Face Inference API
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 300,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        # Make API request
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
            headers=headers,
            json=payload
        )
        
        # Check response
        if response.status_code != 200:
            # Try with a simpler model if the first one fails
            alt_model = "google/flan-t5-large"
            print(f"Primary model failed, trying {alt_model}")
            
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{alt_model}",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Hugging Face API error: {response.text}"
                )
        
        # Parse response
        result = response.json()
        
        # Extract generated text (handle different response formats)
        if isinstance(result, list):
            generated_text = result[0].get('generated_text', '')
        elif isinstance(result, dict):
            generated_text = result.get('generated_text', '')
        else:
            generated_text = str(result)
        
        # Clean up the response
        if generated_text:
            # Remove the prompt if it was included in response
            if prompt in generated_text:
                generated_text = generated_text.replace(prompt, "").strip()
            
            # Ensure safety disclaimer is present
            safety_note = "This is not a medical diagnosis. Please consult a healthcare professional."
            if safety_note not in generated_text:
                generated_text += f"\n\n{safety_note}"
        else:
            generated_text = "I understand you're describing symptoms. Based on general health information, it's important to monitor your symptoms and consult with a healthcare professional for proper evaluation. Common causes for such symptoms can vary widely, so professional medical advice is essential."
        
        return ChatResponse(response=generated_text)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        # Return a safe, generic response if API fails
        safe_response = """Based on your symptoms, here is some general information:

It's important to monitor your symptoms closely. Common symptoms can have various causes, from minor conditions to more serious ones that require medical attention.

General Guidance:
• Rest and stay hydrated
• Monitor your symptoms for any changes
• Avoid self-medication without professional advice

When to Seek Help:
• If symptoms worsen or don't improve
• If you experience severe pain, difficulty breathing, or confusion
• If symptoms persist beyond a few days

Please consult a healthcare professional at Suwa Setha Hospital or your local clinic for proper medical advice. This information is for educational purposes only and not a medical diagnosis."""
        
        return ChatResponse(response=safe_response)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
