import asyncio
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

from ..models.data_models import AgentPrompt, FarmerProfile, ConversationTurn, CallRecord
from ..utils.helpers import generate_call_id, generate_audio_filename
from .audio_processor import AudioProcessor
from .farmer_persona import LLMFarmerPersona

class VoiceAgent:
    """Enhanced voice agent with real audio capabilities"""
    
    def __init__(self, audio_processor: AudioProcessor, farmer_persona: LLMFarmerPersona, 
                 initial_prompt: AgentPrompt):
        self.current_prompt = initial_prompt
        self.audio_processor = audio_processor
        self.farmer_persona = farmer_persona
        self.call_history = []
        self.logger = logging.getLogger(__name__)
        
    async def conduct_voice_call(self, farmer_profile: FarmerProfile, 
                               max_turns: int = 5) -> Tuple[List[str], List[str], List[str]]:
        """Conduct a complete voice call simulation with real audio"""
        
        call_id = generate_call_id()
        conversation_turns = []
        agent_messages = []
        farmer_responses = []
        audio_files = []
        conversation_context = []
        
        self.logger.info(f"📞 Starting call {call_id} with {farmer_profile.name}")
        
        # Start conversation
        current_agent_message = self._build_opening_message()
        
        for turn in range(max_turns):
            self.logger.info(f"🎤 Turn {turn + 1}/{max_turns}")
            
            # Agent speaks
            self.logger.info(f"🤖 Agent: {current_agent_message[:100]}...")
            agent_messages.append(current_agent_message)
            
            # Generate audio for agent
            agent_audio_path = generate_audio_filename(call_id, "agent", turn)
            await self.audio_processor.text_to_speech(current_agent_message, 
                                                    f"data/temp/{agent_audio_path}")
            audio_files.append(agent_audio_path)
            
            # Get farmer response using LLM
            farmer_response = await self.farmer_persona.generate_response(
                farmer_profile, 
                current_agent_message,
                conversation_context
            )
            
            self.logger.info(f"👨‍🌾 Farmer: {farmer_response}")
            farmer_responses.append(farmer_response)
            
            # Generate audio for farmer response (for simulation)
            farmer_audio_path = generate_audio_filename(call_id, "farmer", turn)
            await self.audio_processor.text_to_speech(farmer_response, 
                                                    f"data/temp/{farmer_audio_path}")
            audio_files.append(farmer_audio_path)
            
            # Create conversation turn
            turn_record = ConversationTurn(
                turn_number=turn + 1,
                agent_message=current_agent_message,
                farmer_response=farmer_response,
                audio_files={
                    'agent': agent_audio_path,
                    'farmer': farmer_audio_path
                }
            )
            conversation_turns.append(turn_record)
            
            # Update conversation context
            conversation_context.extend([current_agent_message, farmer_response])
            
            # Generate next agent message
            if turn < max_turns - 1:  # Don't generate for last turn
                current_agent_message = self._generate_next_agent_message(
                    farmer_response, turn, conversation_context
                )
            
            # Check if conversation should end
            if self._should_end_conversation(farmer_response, turn):
                self.logger.info(f"📞 Call ended naturally at turn {turn + 1}")
                break
        
        # Create call record
        call_record = CallRecord(
            call_id=call_id,
            iteration=len(self.call_history) + 1,
            farmer_profile=farmer_profile,
            agent_version=self.current_prompt.version,
            conversation_turns=conversation_turns,
            analysis=None,  # Will be filled by analyzer
            call_start=datetime.now(),
            audio_files=audio_files
        )
        
        self.call_history.append(call_record)
        
        return agent_messages, farmer_responses, audio_files
    
    def _build_opening_message(self) -> str:
        """Build the opening message from current prompt"""
        message = self.current_prompt.intro + " "
        
        if self.current_prompt.benefits:
            message += "Main benefits ye hain: "
            for benefit in self.current_prompt.benefits:
                message += f"{benefit}. "
        
        message += self.current_prompt.call_to_action
        return message
    
    def _generate_next_agent_message(self, farmer_response: str, turn: int, 
                                   conversation_context: List[str]) -> str:
        """Generate next agent message based on farmer response"""
        
        farmer_lower = farmer_response.lower()
        
        # Handle different types of responses
        if any(word in farmer_lower for word in ['kaun ho', 'government', 'identity']):
            return "Ji haan, main government ki taraf se authorized hun. Mera naam Raj hai aur main PM-KUSUM scheme coordinator hun. Aap PM Modi ji ke website pe bhi check kar sakte hain."
            
        elif any(word in farmer_lower for word in ['kya', 'samajh nahi', 'explain', 'simple']):
            return "Main aapko simple mein samjhata hun. Solar pump ka matlab ye hai ki aapko bijli ki jarurat nahi hogi. Sun ki energy se pump chalega. Bilkul free energy."
            
        elif any(word in farmer_lower for word in ['kitne', 'paisa', 'cost', 'paise']):
            return "Bilkul sahi sawaal! Dekho ji, agar pump ki total cost 1 lakh hai, to aapko sirf 10,000 rupaye dene honge. Baaki 90,000 government degi. Monthly installment bhi available hai."
            
        elif any(word in farmer_lower for word in ['eligible', 'qualify', 'documents']):
            return "Eligibility bilkul simple hai. Bas aapke paas khet hona chahiye aur aap farmer hona chahiye. Documents sirf Aadhaar aur khet ke kagaz chahiye. Koi extra formality nahi."
            
        elif any(word in farmer_lower for word in ['process', 'kaise', 'steps']):
            return "Process bahut aasan hai. Pehle online application submit karni hai, phir 15 din mein approval. Uske baad 1 mahine mein installation. Total 45 din ka kaam."
            
        elif any(word in farmer_lower for word in ['time nahi', 'busy', 'baad']):
            return "Koi baat nahi ji. Main aapko WhatsApp pe details bhej deta hun. Sirf 2 minute ka video hai. Aap free time mein dekh sakte hain. Aur koi question ho to direct call kar sakte hain."
            
        elif turn >= 3:  # Wrap up conversation
            if any(word in farmer_lower for word in ['interested', 'chahiye', 'lagwana']):
                return "Bahut achha ji! Main aapka naam register kar deta hun aur officer aapse 2 din mein contact karenge. Aapko sirf form fill karna hai."
            else:
                return "Toh sir, kya aap sochenge? Main aapka number note kar leta hun. Officer aapse detail mein baat karenge."
            
        else:
            return "Aur koi questions hain aapke? Main sab kuch detail mein bata sakta hun. Cost, process, documents - jo bhi jaanna ho."
    
    def _should_end_conversation(self, farmer_response: str, turn: int) -> bool:
        """Determine if conversation should end"""
        farmer_lower = farmer_response.lower()
        
        # End if farmer clearly rejects
        if any(word in farmer_lower for word in ['nahi chahiye', 'interested nahi', 'band karo', 'problem hai']):
            return True
            
        # End if farmer agrees to proceed
        if any(word in farmer_lower for word in ['haan kar do', 'register karo', 'proceed', 'lagwana hai']):
            return True
            
        # End if farmer asks to call later
        if any(word in farmer_lower for word in ['baad mein call', 'time nahi', 'busy hun']):
            return True
            
        # End after max turns
        if turn >= 4:
            return True
            
        return False
    
    def update_prompt(self, new_prompt: AgentPrompt):
        """Update the agent's prompt"""
        old_version = self.current_prompt.version
        self.current_prompt = new_prompt
        self.logger.info(f"🔄 Agent prompt updated: v{old_version} → v{new_prompt.version}")
    
    def get_call_history(self) -> List[CallRecord]:
        """Get call history"""
        return self.call_history
    
    def get_current_prompt(self) -> AgentPrompt:
        """Get current prompt"""
        return self.current_prompt
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary"""
        if not self.call_history:
            return {"total_calls": 0}
        
        total_calls = len(self.call_history)
        avg_turns = sum(len(call.conversation_turns) for call in self.call_history) / total_calls
        
        return {
            "total_calls": total_calls,
            "current_version": self.current_prompt.version,
            "average_conversation_turns": avg_turns,
            "total_improvements": len(self.current_prompt.improvements)
        }