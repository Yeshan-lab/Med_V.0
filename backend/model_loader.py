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
            
            # Using a TINY model that fits in Render's memory
            # OPTION 1: distilbart-cnn-12-6 (84MB) - Good for summarization
            # OPTION 2: sshleifer/tiny-mbart (85MB) - Multilingual
            # OPTION 3: sshleifer/distilbart-xsum-12-1 (250MB) - A bit larger but good
            
            model_name = "sshleifer/tiny-mbart"  # Only 85MB!
            
            print(f"📥 Downloading model: {model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            # Create pipeline
            self.generator = pipeline(
                "text2text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1,  # Use CPU
                max_length=200,
                temperature=0.7,
                do_sample=True
            )
            
            self.model_loaded = True
            print("✅ Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
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
                max_length=150,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1
            )
            
            if result and len(result) > 0:
                return result[0]['generated_text']
                
        except Exception as e:
            print(f"❌ Generation error: {e}")
            
        return None

# Create global instance
medical_ai = MedicalModel()

# Simple test function
def test_model():
    """Test if model works"""
    prompt = "Patient: headache\nDoctor advice:"
    response = medical_ai.generate_response(prompt)
    return response
