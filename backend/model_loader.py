from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
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
            
            # Using a tiny GPT-2 model (82MB)
            model_name = "sshleifer/tiny-gpt2"  # Only 82MB
            
            print(f"📥 Downloading model: {model_name}")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)  # FIXED: Changed to AutoModelForCausalLM
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print("✅ Model and tokenizer loaded!")
            
            # Create text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1,  # Use CPU
                max_length=200,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            self.model_loaded = True
            print("✅ Pipeline created successfully!")
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
            # Generate response
            result = self.generator(
                prompt,
                max_length=200,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                no_repeat_ngram_size=3
            )
            
            if result and len(result) > 0:
                generated_text = result[0]['generated_text']
                
                # Remove the prompt from the response
                if generated_text.startswith(prompt):
                    generated_text = generated_text[len(prompt):].strip()
                
                # Clean up any extra text
                generated_text = generated_text.strip()
                
                print(f"🤖 Generated response: {generated_text[:100]}...")
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
    if response:
        print(f"✅ Test successful: {response[:50]}...")
    else:
        print("❌ Test failed")
    return response
