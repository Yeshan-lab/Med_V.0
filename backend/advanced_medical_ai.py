"""
Advanced Medical AI using Rule-Based Knowledge
Replaces unreliable small language models
"""

from medical_knowledge import medical_kb
import random

class AdvancedMedicalAI:
    def __init__(self):
        self.knowledge_base = medical_kb
        self.conversation_history = []
        
    def process_query(self, user_input: str) -> str:
        """Process medical query with advanced analysis"""
        
        # Clean and prepare input
        user_input = user_input.lower().strip()
        
        # Check for emergencies first
        emergencies = self.knowledge_base.check_emergency(user_input)
        if emergencies:
            return self._generate_emergency_response(emergencies)
        
        # Identify potential conditions
        possible_conditions = self.knowledge_base.identify_condition(user_input)
        
        # Store in conversation history
        self.conversation_history.append({
            "user_input": user_input,
            "matched_conditions": possible_conditions
        })
        
        # Generate appropriate response
        if possible_conditions:
            # Multiple possible conditions
            if len(possible_conditions) > 1:
                return self._generate_differential_diagnosis(possible_conditions, user_input)
            # Single likely condition
            else:
                return self.knowledge_base.generate_advice(
                    possible_conditions[0]["condition_id"],
                    user_input
                )
        else:
            # No specific condition matched
            return self.knowledge_base._generate_general_advice(user_input)
    
    def _generate_emergency_response(self, emergencies):
        """Generate emergency response"""
        response = "🚨 **EMERGENCY MEDICAL ALERT** 🚨\n\n"
        response += f"Based on your description of: {', '.join(emergencies)}\n\n"
        
        response += "**IMMEDIATE ACTION REQUIRED:**\n"
        response += "• Call emergency services (1990 in Sri Lanka) or go to nearest hospital\n"
        response += "• Do not wait for symptoms to improve\n"
        response += "• Do not drive yourself if experiencing these symptoms\n\n"
        
        response += "**Emergency Symptoms Detected:**\n"
        for emergency in emergencies:
            response += f"• {emergency.title()}\n"
        
        response += "\n**Suwa Setha Hospital Emergency Department**\n"
        response += "📍 Location: SuwaSetha Hospital Colombo"
        response += "📞 Emergency: 1990 or 0112 691 111"
        response += "⏰ 24/7 Emergency Services Available\n\n"
        
        response += "⚠️ THIS IS NOT A SUBSTITUTE FOR EMERGENCY MEDICAL CARE."
        return response
    
    def _generate_differential_diagnosis(self, conditions, symptoms):
        """Generate response when multiple conditions are possible"""
        response = "🏥 **Suwa Setha Hospital - Symptom Analysis**\n\n"
        response += f"Based on your symptoms: *{symptoms[:100]}...*\n\n"
        response += "**Possible Conditions to Consider:**\n\n"
        
        for i, condition in enumerate(conditions[:3], 1):
            response += f"{i}. **{condition['name']}**\n"
            response += f"   Match Confidence: {'★' * min(5, condition['match_score'])}\n"
            if condition['matched_symptoms']:
                response += f"   Matching Symptoms: {', '.join(condition['matched_symptoms'])}\n"
            response += "\n"
        
        response += "**Recommendations:**\n"
        response += "1. The condition with highest match is most likely\n"
        response += "2. Each condition has different management approaches\n"
        response += "3. Professional evaluation is needed for accurate diagnosis\n\n"
        
        # Offer detailed info on top match
        top_condition = conditions[0]
        response += f"**Detailed Information for {top_condition['name']}:**\n"
        detailed_advice = self.knowledge_base.generate_advice(
            top_condition["condition_id"],
            symptoms
        )
        
        # Extract just the advice part
        if "Self-Care Recommendations:" in detailed_advice:
            advice_start = detailed_advice.find("Self-Care Recommendations:")
            response += detailed_advice[advice_start:advice_start+500] + "...\n\n"
        
        response += "**Next Steps:**\n"
        response += "• Monitor symptoms closely\n"
        response += "• Follow general self-care recommendations\n"
        response += "• Schedule appointment at Suwa Setha Hospital for proper diagnosis\n\n"
        
        response += self.knowledge_base.safety_disclaimer
        return response

# Create global instance
medical_ai = AdvancedMedicalAI()
