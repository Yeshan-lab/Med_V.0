"""
Advanced Medical Knowledge Base - Rule-Based AI
Provides validated medical advice for common conditions
FIXED: Headache now correctly identifies tension headache instead of influenza
"""

class MedicalKnowledgeBase:
    def __init__(self):
        self.medical_database = self._build_knowledge_base()
        self.safety_disclaimer = "⚠️ EDUCATIONAL TOOL ONLY. Consult Suwa Setha Hospital or healthcare provider for medical advice."
        self.emergency_advice = "🚨 SEEK IMMEDIATE MEDICAL ATTENTION if experiencing: chest pain, difficulty breathing, severe pain, confusion, or loss of consciousness."
    
    def _build_knowledge_base(self):
        """Comprehensive medical knowledge database"""
        return {
            # ========== RESPIRATORY CONDITIONS ==========
            "common_cold": {
                "name": "Common Cold",
                "symptoms": ["runny nose", "sneezing", "sore throat", "mild cough", "congestion", "mild fatigue"],
                "causes": "Viral infection (rhinovirus, coronavirus)",
                "advice": [
                    "Rest and stay hydrated with warm fluids",
                    "Use saline nasal spray for congestion",
                    "Gargle with warm salt water for sore throat",
                    "Over-the-counter cold medications as directed",
                    "Use a humidifier to ease breathing"
                ],
                "duration": "7-10 days",
                "when_to_see_doctor": "If symptoms last more than 10 days, fever exceeds 101°F, or breathing difficulties occur",
                "severity": "mild"
            },
            
            "influenza": {
                "name": "Influenza (Flu)",
                "symptoms": ["high fever", "body aches", "chills", "severe fatigue", "headache", "dry cough"],
                "causes": "Influenza virus",
                "advice": [
                    "Rest and plenty of fluids",
                    "Antiviral medication (if prescribed early)",
                    "Over-the-counter fever reducers (acetaminophen, ibuprofen)",
                    "Stay home to prevent spreading",
                    "Annual flu vaccination for prevention"
                ],
                "duration": "1-2 weeks",
                "when_to_see_doctor": "High fever, difficulty breathing, chest pain, or symptoms worsening",
                "severity": "moderate"
            },
            
            "bronchitis": {
                "name": "Acute Bronchitis",
                "symptoms": ["persistent cough", "mucus production", "chest discomfort", "mild fever", "fatigue"],
                "causes": "Viral infection (usually), sometimes bacterial",
                "advice": [
                    "Increase fluid intake to thin mucus",
                    "Use honey in warm tea to soothe cough",
                    "Avoid smoke and irritants",
                    "Over-the-counter cough suppressants if needed",
                    "Rest to support immune system"
                ],
                "duration": "3 weeks typically",
                "when_to_see_doctor": "Fever over 100.4°F, blood in mucus, or symptoms beyond 3 weeks",
                "severity": "moderate"
            },
            
            # ========== GASTROINTESTINAL ==========
            "gastroenteritis": {
                "name": "Gastroenteritis (Stomach Flu)",
                "symptoms": ["diarrhea", "nausea", "vomiting", "abdominal cramps", "low-grade fever"],
                "causes": "Viral or bacterial infection, food poisoning",
                "advice": [
                    "Oral rehydration solution or clear fluids",
                    "BRAT diet (bananas, rice, applesauce, toast)",
                    "Avoid dairy, fatty, or spicy foods",
                    "Rest the digestive system with small, frequent meals",
                    "Wash hands frequently to prevent spread"
                ],
                "duration": "1-3 days typically",
                "when_to_see_doctor": "Signs of dehydration, blood in stool, fever over 102°F, or symptoms beyond 3 days",
                "severity": "moderate"
            },
            
            "acid_reflux": {
                "name": "GERD/Acid Reflux",
                "symptoms": ["heartburn", "regurgitation", "chest pain", "difficulty swallowing", "chronic cough"],
                "causes": "Stomach acid flowing back into esophagus",
                "advice": [
                    "Eat smaller, more frequent meals",
                    "Avoid trigger foods (spicy, fatty, citrus, chocolate)",
                    "Don't lie down for 2-3 hours after eating",
                    "Elevate head of bed 6-8 inches",
                    "Over-the-counter antacids as needed"
                ],
                "duration": "Chronic condition",
                "when_to_see_doctor": "Frequent symptoms, weight loss, severe pain, or difficulty swallowing",
                "severity": "mild_moderate"
            },
            
            # ========== NEUROLOGICAL ==========
            "migraine": {
                "name": "Migraine Headache",
                "symptoms": ["severe headache", "sensitivity to light/sound", "nausea", "aura", "throbbing pain"],
                "causes": "Neurological condition with various triggers",
                "advice": [
                    "Rest in dark, quiet room",
                    "Cold compress on forehead or neck",
                    "Stay hydrated",
                    "Prescription migraine medications if diagnosed",
                    "Identify and avoid triggers (stress, certain foods, lack of sleep)"
                ],
                "duration": "4-72 hours",
                "when_to_see_doctor": "First migraine, change in pattern, or severe symptoms",
                "severity": "moderate_severe"
            },
            
            "tension_headache": {
                "name": "Tension Headache",
                "symptoms": ["band-like pressure around head", "tight neck muscles", "mild to moderate pain"],
                "causes": "Muscle tension, stress, poor posture",
                "advice": [
                    "Gentle neck and shoulder stretches",
                    "Stress reduction techniques",
                    "Over-the-counter pain relievers (ibuprofen, acetaminophen)",
                    "Apply heat to tense muscles",
                    "Improve posture and take regular breaks"
                ],
                "duration": "30 minutes to several hours",
                "when_to_see_doctor": "Frequent headaches, not relieved by OTC medications",
                "severity": "mild_moderate"
            },
            
            # ========== MUSCULOSKELETAL ==========
            "back_pain": {
                "name": "Non-Specific Back Pain",
                "symptoms": ["lower back pain", "muscle stiffness", "limited mobility", "muscle spasms"],
                "causes": "Muscle strain, poor posture, injury",
                "advice": [
                    "Gentle stretching and walking",
                    "Apply ice first 48 hours, then heat",
                    "Over-the-counter anti-inflammatories",
                    "Improve posture and ergonomics",
                    "Avoid heavy lifting and sudden movements"
                ],
                "duration": "Few days to weeks",
                "when_to_see_doctor": "Severe pain, leg weakness, numbness, or bowel/bladder changes",
                "severity": "mild_moderate"
            },
            
            "arthritis": {
                "name": "Osteoarthritis",
                "symptoms": ["joint pain", "stiffness", "swelling", "reduced range of motion"],
                "causes": "Joint wear and tear",
                "advice": [
                    "Low-impact exercise (swimming, cycling)",
                    "Weight management to reduce joint stress",
                    "Heat therapy for stiffness",
                    "Over-the-counter pain relievers",
                    "Assistive devices if needed"
                ],
                "duration": "Chronic condition",
                "when_to_see_doctor": "Severe pain, joint deformity, or significant mobility loss",
                "severity": "moderate"
            },
            
            # ========== SKIN CONDITIONS ==========
            "eczema": {
                "name": "Atopic Dermatitis (Eczema)",
                "symptoms": ["itchy skin", "red patches", "dry skin", "scaling", "inflammation"],
                "causes": "Genetic, environmental triggers, immune system",
                "advice": [
                    "Moisturize regularly with fragrance-free creams",
                    "Use mild, fragrance-free soaps",
                    "Avoid known triggers (certain fabrics, soaps, foods)",
                    "Cool compresses for itching",
                    "Prescription creams for flare-ups"
                ],
                "duration": "Chronic with flare-ups",
                "when_to_see_doctor": "Infected skin, severe symptoms, or not controlled with OTC treatments",
                "severity": "mild_moderate"
            },
            
            "acne": {
                "name": "Acne Vulgaris",
                "symptoms": ["pimples", "blackheads", "whiteheads", "oiliness", "inflammation"],
                "causes": "Hormonal changes, bacteria, excess oil",
                "advice": [
                    "Gentle cleansing twice daily",
                    "Oil-free, non-comedogenic products",
                    "Don't pick or squeeze lesions",
                    "Over-the-counter benzoyl peroxide or salicylic acid",
                    "Healthy diet and stress management"
                ],
                "duration": "Variable, often teenage years",
                "when_to_see_doctor": "Severe acne, scarring, or not responding to OTC treatments",
                "severity": "mild_moderate"
            },
            
            # ========== METABOLIC/CHRONIC ==========
            "hypertension": {
                "name": "High Blood Pressure",
                "symptoms": ["often none", "headaches", "shortness of breath", "nosebleeds (rare)"],
                "causes": "Various factors including diet, genetics, lifestyle",
                "advice": [
                    "Reduce sodium intake",
                    "Regular aerobic exercise",
                    "Maintain healthy weight",
                    "Limit alcohol and caffeine",
                    "Monitor blood pressure regularly"
                ],
                "duration": "Chronic condition",
                "when_to_see_doctor": "New diagnosis, uncontrolled readings, or medication side effects",
                "severity": "moderate_severe"
            },
            
            "diabetes": {
                "name": "Type 2 Diabetes",
                "symptoms": ["increased thirst", "frequent urination", "fatigue", "blurred vision", "slow healing"],
                "causes": "Insulin resistance, genetic, lifestyle factors",
                "advice": [
                    "Regular blood sugar monitoring",
                    "Balanced diet with controlled carbohydrates",
                    "Regular physical activity",
                    "Medication adherence if prescribed",
                    "Foot care and regular check-ups"
                ],
                "duration": "Chronic condition",
                "when_to_see_doctor": "Abnormal blood sugar readings, new symptoms, or medication adjustments needed",
                "severity": "moderate_severe"
            },
            
            # ========== ALLERGIES ==========
            "allergic_rhinitis": {
                "name": "Hay Fever (Allergic Rhinitis)",
                "symptoms": ["sneezing", "runny nose", "itchy eyes", "congestion", "postnasal drip"],
                "causes": "Allergens (pollen, dust, pet dander)",
                "advice": [
                    "Avoid known allergens when possible",
                    "Over-the-counter antihistamines",
                    "Nasal corticosteroid sprays",
                    "Saline nasal rinses",
                    "Keep windows closed during high pollen seasons"
                ],
                "duration": "Seasonal or perennial",
                "when_to_see_doctor": "Symptoms not controlled with OTC medications or affecting quality of life",
                "severity": "mild_moderate"
            }
        }
    
    def identify_condition(self, symptoms_text):
        """FIXED: Advanced symptom analysis with better headache detection"""
        symptoms = symptoms_text.lower()
        matches = []
        
        # Special handling for headache complaints
        if "headache" in symptoms:
            return self._analyze_headache_case(symptoms_text)
        
        # General analysis for other symptoms
        for condition_id, info in self.medical_database.items():
            match_score = 0
            symptom_matches = []
            
            # Check for symptom keywords with intelligent weighting
            for symptom in info["symptoms"]:
                if symptom in symptoms:
                    # Different weights for different symptoms
                    if symptom == "headache":
                        if condition_id == "influenza":
                            match_score += 1  # Low weight: headache alone ≠ flu
                        elif condition_id in ["tension_headache", "migraine", "hypertension"]:
                            match_score += 4  # High weight: primary symptom
                        else:
                            match_score += 2  # Medium weight
                    elif symptom in ["high fever", "body aches", "chills"]:
                        match_score += 3  # Important flu symptoms
                    elif symptom in ["severe headache", "throbbing pain", "aura"]:
                        match_score += 4  # Important migraine symptoms
                    elif symptom in ["band-like pressure", "tight neck muscles"]:
                        match_score += 4  # Important tension headache symptoms
                    else:
                        match_score += 2  # Regular symptoms
                    
                    symptom_matches.append(symptom)
            
            # Check for condition name mention (high priority)
            if info["name"].lower() in symptoms:
                match_score += 6
            
            # Check for related keywords
            related_keywords = {
                "common_cold": ["cold", "sniffles", "stuffy nose"],
                "influenza": ["flu", "influenza", "body ache"],
                "bronchitis": ["bronchitis", "chest cough"],
                "gastroenteritis": ["stomach flu", "food poisoning", "vomiting"],
                "acid_reflux": ["gerd", "heartburn", "indigestion"],
                "migraine": ["migraine", "aura", "sensitivity light", "throbbing"],
                "tension_headache": ["tension headache", "stress headache", "pressure head"],
                "back_pain": ["backache", "lower back", "spinal"],
                "arthritis": ["joint pain", "arthritic"],
                "eczema": ["dermatitis", "skin rash", "itchy skin"],
                "acne": ["pimples", "blackheads", "breakout"],
                "hypertension": ["high blood pressure", "hypertension", "bp high"],
                "diabetes": ["high sugar", "diabetic", "blood glucose"],
                "allergic_rhinitis": ["hay fever", "allergies", "seasonal allergies"]
            }
            
            if condition_id in related_keywords:
                for keyword in related_keywords[condition_id]:
                    if keyword in symptoms:
                        match_score += 2
            
            # Only include meaningful matches
            if match_score >= 3:
                matches.append({
                    "condition_id": condition_id,
                    "name": info["name"],
                    "match_score": match_score,
                    "matched_symptoms": symptom_matches,
                    "severity": info["severity"]
                })
        
        # Sort by match score
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        
        # If no good matches, return general advice
        if not matches or matches[0]["match_score"] < 4:
            return []
        
        return matches[:3]
    
    def _analyze_headache_case(self, symptoms_text):
        """Specialized logic for headache complaints"""
        symptoms = symptoms_text.lower()
        matches = []
        
        # Check what type of headache it might be
        headache_type = "tension_headache"  # Default: most common
        
        # Migraine indicators
        migraine_indicators = [
            ("throbbing", 3), ("pulsating", 3), ("one side", 3), 
            ("light sensitivity", 3), ("sound sensitivity", 3), 
            ("aura", 4), ("visual disturbance", 3), ("nausea", 2), ("vomiting", 2)
        ]
        
        # Tension headache indicators
        tension_indicators = [
            ("pressure", 3), ("tight", 3), ("band", 3), ("stress", 2), 
            ("tension", 3), ("both sides", 2), ("mild to moderate", 2)
        ]
        
        # Calculate scores
        migraine_score = sum(score for indicator, score in migraine_indicators if indicator in symptoms)
        tension_score = sum(score for indicator, score in tension_indicators if indicator in symptoms)
        
        # Also check for other conditions that include headache
        other_conditions = []
        
        # Check for flu (needs additional symptoms)
        flu_indicators = ["fever", "body aches", "chills", "fatigue", "cough"]
        flu_count = sum(1 for indicator in flu_indicators if indicator in symptoms)
        
        # Check for sinus issues
        sinus_indicators = ["sinus", "facial pressure", "congestion", "runny nose"]
        sinus_count = sum(1 for indicator in sinus_indicators if indicator in symptoms)
        
        # Determine primary headache type
        if migraine_score >= 4:
            matches.append({
                "condition_id": "migraine",
                "name": "Migraine Headache",
                "match_score": 5 + migraine_score,
                "matched_symptoms": ["headache"] + [ind for ind, _ in migraine_indicators if ind in symptoms],
                "severity": "moderate_severe"
            })
        
        # Always include tension headache (most common)
        matches.append({
            "condition_id": "tension_headache",
            "name": "Tension Headache",
            "match_score": 5 + tension_score,
            "matched_symptoms": ["headache"] + [ind for ind, _ in tension_indicators if ind in symptoms],
            "severity": "mild_moderate"
        })
        
        # Include flu only if there are other flu symptoms
        if flu_count >= 2:
            matches.append({
                "condition_id": "influenza",
                "name": "Influenza (Flu)",
                "match_score": 3 + flu_count,
                "matched_symptoms": ["headache"] + [ind for ind in flu_indicators if ind in symptoms],
                "severity": "moderate"
            })
        
        # Include hypertension if mentioned
        if any(word in symptoms for word in ["high blood pressure", "hypertension", "bp"]):
            matches.append({
                "condition_id": "hypertension",
                "name": "High Blood Pressure",
                "match_score": 4,
                "matched_symptoms": ["headache"],
                "severity": "moderate_severe"
            })
        
        # Sort by match score
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches[:3]
    
    def generate_advice(self, condition_id, symptoms_text=""):
        """Generate comprehensive medical advice for a condition"""
        if condition_id not in self.medical_database:
            return self._generate_general_advice(symptoms_text)
        
        info = self.medical_database[condition_id]
        
        # Build comprehensive response
        response = f"🏥 **{info['name']} - Medical Information**\n\n"
        
        # Symptoms section
        response += f"**Common Symptoms:**\n"
        for symptom in info["symptoms"]:
            response += f"• {symptom.title()}\n"
        
        # Self-care advice
        response += f"\n**Self-Care Recommendations:**\n"
        for i, advice in enumerate(info["advice"], 1):
            response += f"{i}. {advice}\n"
        
        # Additional info
        response += f"\n**Additional Information:**\n"
        response += f"• Typical Duration: {info['duration']}\n"
        response += f"• Common Causes: {info['causes']}\n"
        
        # When to seek medical care
        response += f"\n**When to Consult Suwa Setha Hospital:**\n"
        response += f"• {info['when_to_see_doctor']}\n"
        
        # Severity and precautions
        severity_map = {
            "mild": "Generally manageable with self-care",
            "moderate": "May require medical evaluation",
            "severe": "Requires medical attention",
            "mild_moderate": "Monitor closely, seek care if worsens",
            "moderate_severe": "Medical evaluation recommended"
        }
        
        if info["severity"] in severity_map:
            response += f"• Severity Level: {severity_map[info['severity']]}\n"
        
        # Add emergency warning if needed
        if info["severity"] in ["severe", "moderate_severe"]:
            response += f"\n{self.emergency_advice}\n"
        
        # Always add disclaimer
        response += f"\n{self.safety_disclaimer}"
        
        return response
    
    def _generate_general_advice(self, symptoms_text):
        """Generate advice when no specific condition is identified"""
        response = "🤖 **Suwa Setha Hospital Health Assistant**\n\n"
        response += "Based on your symptoms, here's general health guidance:\n\n"
        
        # Analyze symptoms for general advice
        symptoms = symptoms_text.lower()
        
        if any(word in symptoms for word in ["fever", "temperature", "hot"]):
            response += "• For fever: Rest, stay hydrated, monitor temperature\n"
            response += "• Seek care if fever exceeds 102°F or persists beyond 3 days\n\n"
        
        if any(word in symptoms for word in ["pain", "ache", "hurt"]):
            response += "• For pain: Rest affected area, consider OTC pain relievers\n"
            response += "• Seek care if pain is severe, sudden, or worsening\n\n"
        
        if any(word in symptoms for word in ["cough", "breath", "chest"]):
            response += "• For respiratory symptoms: Stay hydrated, use humidifier\n"
            response += "• Seek care if experiencing difficulty breathing\n\n"
        
        if any(word in symptoms for word in ["stomach", "nausea", "vomit", "diarrhea"]):
            response += "• For digestive symptoms: BRAT diet, clear fluids\n"
            response += "• Seek care if signs of dehydration or severe pain\n\n"
        
        # General wellness tips
        response += "\n**General Wellness Recommendations:**\n"
        response += "1. Stay hydrated with water throughout the day\n"
        response += "2. Ensure adequate rest and sleep\n"
        response += "3. Monitor symptoms for changes or worsening\n"
        response += "4. Avoid self-medication without professional advice\n"
        response += "5. Consider keeping a symptom diary\n\n"
        
        response += "**When to Seek Medical Care:**\n"
        response += "• Symptoms are severe or worsening\n"
        response += "• New or concerning symptoms develop\n"
        response += "• Symptoms persist beyond expected duration\n"
        response += "• You have underlying health conditions\n\n"
        
        response += self.emergency_advice + "\n\n"
        response += self.safety_disclaimer
        
        return response
    
    def check_emergency(self, symptoms_text):
        """Check for emergency symptoms"""
        emergency_keywords = [
            "chest pain", "pressure chest", "tight chest",
            "can't breathe", "difficulty breathing", "short breath",
            "severe pain", "unbearable pain",
            "unconscious", "passed out", "fainted",
            "confused", "disoriented", "slurred speech",
            "severe headache", "worst headache",
            "bleeding won't stop", "heavy bleeding",
            "poison", "overdose"
        ]
        
        symptoms = symptoms_text.lower()
        emergencies = []
        
        for keyword in emergency_keywords:
            if keyword in symptoms:
                emergencies.append(keyword)
        
        return emergencies

# Create global instance
medical_kb = MedicalKnowledgeBase()
