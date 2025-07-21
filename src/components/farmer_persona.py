import asyncio
import random
import re
from typing import Dict, List, Optional
import openai
import logging

from ..models.data_models import FarmerProfile
from ..utils.helpers import clean_hindi_text, PerformanceTracker

class LLMFarmerPersona:
    """LLM-based farmer persona that generates realistic responses"""
    
    def __init__(self, openai_api_key: str, config: Dict, personas_config: Dict):
        self.openai_api_key = openai_api_key
        self.config = config
        self.personas_config = personas_config
        self.conversation_history = []
        self.logger = logging.getLogger(__name__)
        self.performance_tracker = PerformanceTracker()
        
        if openai_api_key:
            openai.api_key = openai_api_key
        else:
            self.logger.warning("OpenAI API key not provided - using mock mode")
        
        # Load response templates for mock mode
        self.response_templates = self._load_response_templates()
    
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Load response templates from personas config"""
        templates = {}
        
        for persona_type, persona_data in self.personas_config.get("persona_templates", {}).items():
            characteristics = persona_data.get("characteristics", {})
            templates[persona_type] = characteristics.get("response_patterns", [])
        
        return templates
    
    def create_farmer_persona_prompt(self, farmer_profile: FarmerProfile) -> str:
        """Create a detailed persona prompt for the LLM"""
        
        # Get persona template if available
        persona_template = None
        if farmer_profile.persona_type:
            persona_template = self.personas_config.get("persona_templates", {}).get(farmer_profile.persona_type)
        
        return f"""
        You are a {farmer_profile.age}-year-old farmer named {farmer_profile.name} from {farmer_profile.location}.
        
        FARMER PROFILE:
        - Education: {farmer_profile.education.value} 
        - Income: {farmer_profile.income.value}
        - Primary crops: {', '.join(farmer_profile.crops)}
        - Land size: {farmer_profile.land_size}
        - Skepticism level: {farmer_profile.skepticism}/1.0
        - Previous experience with govt schemes: {farmer_profile.govt_experience}
        - Language comfort: Primarily Hindi, some broken English
        - Family size: {farmer_profile.family_size}
        
        PERSONALITY TRAITS:
        - {self._get_personality_traits(farmer_profile, persona_template)}
        
        CONVERSATION STYLE:
        - Speak in Hindi mixed with local dialect
        - Use realistic farmer expressions like "Haan bhai", "Achha", "Samajh nahi aaya"
        - Show appropriate emotions based on content
        - Ask practical questions about cost, eligibility, process
        - Express skepticism about government schemes if skepticism is high
        - Use simple language, avoid technical terms unless education is high
        
        RESPONSE GUIDELINES:
        - Keep responses 1-2 sentences long
        - Show genuine farmer concerns and reactions
        - Ask clarifying questions when confused
        - Express interest if benefits seem genuine and affordable
        - Show hesitation about upfront costs or complex processes
        
        You will receive agent messages about PM-KUSUM solar scheme. Respond as this farmer would naturally react.
        """
    
    def _get_personality_traits(self, profile: FarmerProfile, persona_template: Optional[Dict]) -> str:
        """Generate personality traits based on profile"""
        traits = []
        
        if persona_template:
            # Use template characteristics if available
            characteristics = persona_template.get("characteristics", {})
            concerns = characteristics.get("concerns", [])
            traits.extend([f"Concerned about: {', '.join(concerns)}"])
        
        # Add profile-based traits
        if profile.education == "low":
            traits.append("Cautious about new technology, prefers simple explanations")
        elif profile.education == "high": 
            traits.append("Asks detailed questions, wants to understand technical aspects")
        
        if profile.income == "low":
            traits.append("Very cost-conscious, worried about upfront payments")
        elif profile.income == "high":
            traits.append("Interested in ROI and long-term benefits")
            
        if profile.skepticism > 0.7:
            traits.append("Highly skeptical of government schemes, has been cheated before")
        elif profile.skepticism < 0.3:
            traits.append("Open to new opportunities, trusts government initiatives")
            
        return "; ".join(traits)
    
    async def generate_response(self, farmer_profile: FarmerProfile, agent_message: str, 
                              conversation_context: List[str]) -> str:
        """Generate LLM-based farmer response"""
        
        if not self.openai_api_key:
            return await self._generate_mock_response(farmer_profile, agent_message, conversation_context)
        
        system_prompt = self.create_farmer_persona_prompt(farmer_profile)
        
        # Build conversation context
        context_messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (limit to last 10 messages)
        recent_context = conversation_context[-10:] if len(conversation_context) > 10 else conversation_context
        for i, msg in enumerate(recent_context):
            role = "assistant" if i % 2 == 0 else "user"  # farmer responses are assistant
            context_messages.append({"role": role, "content": msg})
        
        # Add current agent message
        context_messages.append({"role": "user", "content": f"Agent says: {agent_message}"})
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.get("openai", {}).get("model", "gpt-4"),
                messages=context_messages,
                max_tokens=self.config.get("openai", {}).get("max_tokens", 100),
                temperature=self.config.get("openai", {}).get("temperature", 0.8),
                frequency_penalty=0.3
            )
            
            farmer_response = response.choices[0].message.content.strip()
            
            # Clean up and ensure it sounds natural
            farmer_response = self._post_process_response(farmer_response, farmer_profile)
            
            self.performance_tracker.record_api_call("openai", True)
            self.logger.info(f"🤖 Generated farmer response: {farmer_response[:50]}...")
            
            return farmer_response
            
        except Exception as e:
            self.logger.error(f"Error generating LLM response: {e}")
            self.performance_tracker.record_api_call("openai", False)
            # Fallback to mock response
            return await self._generate_mock_response(farmer_profile, agent_message, conversation_context)
    
    async def _generate_mock_response(self, farmer_profile: FarmerProfile, agent_message: str, 
                                    conversation_context: List[str]) -> str:
        """Generate mock farmer response without API calls"""
        
        await asyncio.sleep(0.2)  # Simulate API delay
        
        # Determine farmer type for template selection
        persona_type = farmer_profile.persona_type or self._infer_persona_type(farmer_profile)
        
        # Get response templates
        templates = self.response_templates.get(persona_type, [])
        if not templates:
            templates = ["Haan, sun raha hun.", "Theek hai, batayiye.", "Samajh nahi aaya."]
        
        # Select response based on conversation turn
        turn = len(conversation_context) // 2
        
        if turn < len(templates):
            base_response = templates[turn]
        else:
            base_response = random.choice(templates)
        
        # Add contextual modifications
        base_response = self._add_contextual_modifications(base_response, agent_message, farmer_profile)
        
        self.logger.info(f"🤖 [MOCK] Generated response: {base_response[:50]}...")
        return base_response
    
    def _infer_persona_type(self, profile: FarmerProfile) -> str:
        """Infer persona type from farmer profile"""
        if profile.education.value == "low" and profile.skepticism > 0.7:
            return "skeptical_low_education"
        elif profile.education.value == "high":
            return "progressive_high_education"
        else:
            return "interested_medium_education"
    
    def _add_contextual_modifications(self, base_response: str, agent_message: str, 
                                    profile: FarmerProfile) -> str:
        """Add contextual modifications to mock responses"""
        
        agent_lower = agent_message.lower()
        
        # Modify based on agent message content
        if "subsidy" in agent_lower and profile.income.value == "low":
            base_response += " Sach mein sirf 10% paisa lagega?"
        
        if "solar" in agent_lower and "kya" not in base_response.lower():
            if profile.education.value == "low":
                base_response = "Solar kya hota hai bhai? Simple mein batao."
        
        if "process" in agent_lower:
            base_response += " Kitne din lagenge?"
        
        # Add skepticism based responses
        if profile.skepticism > 0.7 and "government" in agent_lower:
            base_response += " Government ki guarantee hai kya?"
        
        return base_response
    
    def _post_process_response(self, response: str, profile: FarmerProfile) -> str:
        """Clean up and enhance the LLM response"""
        
        # Remove any "As a farmer" type prefixes
        response = re.sub(r"^(As a farmer|As [a-zA-Z\s]+),?\s*", "", response)
        
        # Clean Hindi text
        response = clean_hindi_text(response)
        
        # Add natural Hindi expressions based on education level
        if profile.education.value == "low" and len(response.split()) > 15:
            # Simplify for low education
            sentences = response.split('.')
            response = sentences[0] + "."
            
        # Add emotional indicators based on content
        if any(word in response.lower() for word in ['interested', 'good', 'achha']):
            if profile.skepticism < 0.5:
                response += " Batayiye aur details."
                
        return response
    
    def get_performance_stats(self) -> Dict:
        """Get farmer persona performance statistics"""
        return self.performance_tracker.get_summary()