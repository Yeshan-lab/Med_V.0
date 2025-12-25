from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

class MedicalModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.generator = None
        self.model_loaded = False
        
    def load_model(self):
        """Load a very small medical model"""
        try:
            print("🔄 Loading medical model...")
            
            # Using a DIFFERENT tiny model that doesn't need protobuf
            # Let's try a different approach - use a text-generation model instead
            
            # OPTIONS (all under 100MB):
            # 1. "sshleifer/tiny-gpt2" (82MB) - Simple text generation
            # 2. "distilgpt2" (334MB) - A bit larger but good quality
            # 3. "microsoft/DialoGPT-small" (334MB) - Chat optimized
            
            # Let's use the smallest possible
            model_name = "sshleifer/tiny-gpt2"  # Only 82MB and doesn't need protobuf
            
            print(f"📥 Downloading model: {model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Create pipeline
            self.generator = pipeline(
                "text-generation",  # Changed from text2text-generation
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1,  # Use CPU
                max_length=200,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            self.model_loaded = True
            print("✅ Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            import traceback
            traceback.print_exc()
            self.model_loaded = False
            return False
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using the model"""
        if not self.model_loaded:
            if not self.load_model():
                return None
        
        try:
            result = self.generator(
                prompt,
                max_length=200,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            if result and len(result) > 0:
                generated_text = result[0]['generated_text']
                # Remove the prompt from the response
                if generated_text.startswith(prompt):
                    generated_text = generated_text[len(prompt):].strip()
                return generated_text
                
        except Exception as e:
            print(f"❌ Generation error: {e}")
            import traceback
            traceback.print_exc()
            
        return None

# Create global instance
medical_ai = MedicalModel()

# Simple test function
def test_model():
    """Test if model works"""
    prompt = "Patient: headache\nDoctor advice:"
    response = medical_ai.generate_response(prompt)
    return response
