#!/usr/bin/env python3
"""
Voice Agent Reinforcement Learning System - Demo Version
Works without API keys - perfect for presentations and testing
"""

import asyncio
import sys
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import logging

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from models.data_models import (
    AgentPrompt, CallAnalysis, SentimentType, InterestLevel, 
    CallOutcome, FarmerProfile, EducationLevel, IncomeLevel
)
from utils.helpers import save_json_data, calculate_effectiveness_score

class MockVoiceAgentSystem:
    """Demo system that works without API keys"""
    
    def __init__(self):
        self.setup_logging()
        self.initialize_demo_data()
        self.call_log = []
        
        self.logger.info("🎬 Demo Voice Agent System initialized")
    
    def setup_logging(self):
        """Setup simple logging for demo"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(message)s',
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger(__name__)
    
    def initialize_demo_data(self):
        """Initialize demo data and prompts"""
        
        # Initial agent prompt
        self.current_prompt = AgentPrompt(
            intro="Namaste ji, main solar scheme ke baare mein baat karne ke liye call kar raha hun. Government ki PM-KUSUM yojana ke through aap apne khet mein solar pump lagwa sakte hain.",
            benefits=[
                "90% subsidy milegi government se",
                "Bijli ka bill kam ho jayega, aur income bhi badh sakti hai",
                "5 saal mein paisa recover ho jayega"
            ],
            call_to_action="Kya aap is scheme ke baare mein aur jaanna chahenge?",
            version=1,
            tone_instructions="Speak politely and clearly, use simple Hindi",
            conversation_style="Friendly but professional"
        )
        
        # Demo farmer profiles
        self.demo_farmers = [
            FarmerProfile(
                id="F001",
                name="Skeptical Ramesh",
                age=45,
                education=EducationLevel.LOW,
                income=IncomeLevel.LOW,
                location="Meerut, UP",
                crops=["wheat", "sugarcane"],
                land_size="2 acres",
                skepticism=0.9,
                govt_experience="was cheated before",
                family_size=6
            ),
            FarmerProfile(
                id="F002",
                name="Interested Suresh",
                age=38,
                education=EducationLevel.MEDIUM,
                income=IncomeLevel.MEDIUM,
                location="Anand, Gujarat",
                crops=["cotton", "groundnut"],
                land_size="5 acres",
                skepticism=0.4,
                govt_experience="some positive experience",
                family_size=4
            ),
            FarmerProfile(
                id="F003",
                name="Progressive Mahesh",
                age=35,
                education=EducationLevel.HIGH,
                income=IncomeLevel.HIGH,
                location="Ludhiana, Punjab",
                crops=["rice", "wheat"],
                land_size="10 acres",
                skepticism=0.2,
                govt_experience="multiple successful schemes",
                family_size=5
            )
        ]
        
        # Response templates for different farmer types
        self.response_templates = {
            "skeptical_low": [
                "Kaun ho tum? Government se ho kya?",
                "Pehle tum batao, ye sach hai ya jhooth?",
                "Kitne paise lagenge? Main gareeb kisan hun",
                "Mujhe koi paisa nahi dena, bilkul free mein chahiye"
            ],
            "interested_medium": [
                "Haan, sun raha hun. Batayiye details",
                "90% subsidy matlab kitne paise bachenge?",
                "Process kya hai? Kaise apply karna hai?",
                "Achha lagta hai. Aur bhi koi benefits hain?"
            ],
            "progressive_high": [
                "Interesting. What's the ROI on this investment?",
                "Technical specifications kya hain is solar pump ke?",
                "Government ki guarantee hai kya? Documentation milega?",
                "Haan, main interested hun. Next steps kya hain?"
            ]
        }
    
    async def conduct_demo_call(self, farmer: FarmerProfile, max_turns: int = 4) -> Tuple[List[str], List[str]]:
        """Conduct a demo call with mock interactions"""
        
        agent_messages = []
        farmer_responses = []
        conversation_context = []
        
        # Build opening message
        opening_message = self._build_agent_message()
        
        # Determine farmer type for responses
        if farmer.education == EducationLevel.LOW and farmer.skepticism > 0.7:
            template_key = "skeptical_low"
        elif farmer.education == EducationLevel.HIGH:
            template_key = "progressive_high"
        else:
            template_key = "interested_medium"
        
        templates = self.response_templates[template_key]
        
        for turn in range(max_turns):
            self.logger.info(f"\n🎤 Turn {turn + 1}/{max_turns}")
            
            # Agent speaks
            current_agent_message = opening_message if turn == 0 else self._generate_followup_message(
                farmer_responses[-1], turn, farmer
            )
            
            self.logger.info(f"🤖 Agent: {current_agent_message}")
            agent_messages.append(current_agent_message)
            
            # Simulate audio generation
            await asyncio.sleep(0.2)
            self.logger.info(f"🎵 [Audio Generated] agent_turn_{turn}.mp3")
            
            # Get farmer response
            if turn < len(templates):
                base_response = templates[turn]
            else:
                base_response = random.choice(templates)
            
            # Add contextual modifications
            farmer_response = self._add_context_to_response(base_response, current_agent_message, farmer)
            
            self.logger.info(f"👨‍🌾 Farmer: {farmer_response}")
            farmer_responses.append(farmer_response)
            
            # Simulate audio generation
            await asyncio.sleep(0.2)
            self.logger.info(f"🎵 [Audio Generated] farmer_turn_{turn}.mp3")
            
            conversation_context.extend([current_agent_message, farmer_response])
            
            # Check if should end
            if self._should_end_conversation(farmer_response, turn):
                break
        
        return agent_messages, farmer_responses
    
    def _build_agent_message(self) -> str:
        """Build agent message from current prompt"""
        message = self.current_prompt.intro + " "
        
        if self.current_prompt.benefits:
            message += "Main benefits ye hain: "
            for benefit in self.current_prompt.benefits:
                message += f"{benefit}. "
        
        message += self.current_prompt.call_to_action
        return message
    
    def _generate_followup_message(self, farmer_response: str, turn: int, farmer: FarmerProfile) -> str:
        """Generate contextual followup message"""
        
        farmer_lower = farmer_response.lower()
        
        if any(word in farmer_lower for word in ['kaun ho', 'government']):
            return "Ji haan, main government ki taraf se authorized hun. Mera naam Raj hai aur main PM-KUSUM scheme coordinator hun."
            
        elif any(word in farmer_lower for word in ['kitne paise', 'cost', 'paisa']):
            return "Bilkul sahi sawaal! Dekho ji, agar pump ki total cost 1 lakh hai, to aapko sirf 10,000 rupaye dene honge. Baaki 90,000 government degi."
            
        elif any(word in farmer_lower for word in ['roi', 'specifications', 'technical']):
            return "ROI bahut achha hai sir. 5 saal mein investment recover ho jayega. Technical specs: 5HP solar pump with 20-year warranty."
            
        elif any(word in farmer_lower for word in ['process', 'apply']):
            return "Process bilkul simple hai. Online application, 15 din mein approval, 1 mahine mein installation. Total 45 din ka kaam."
            
        else:
            return "Aur koi questions hain? Main sab detail mein bata sakta hun."
    
    def _add_context_to_response(self, base_response: str, agent_message: str, farmer: FarmerProfile) -> str:
        """Add contextual modifications to farmer response"""
        
        agent_lower = agent_message.lower()
        
        # Add cost concerns for low income farmers
        if farmer.income == IncomeLevel.LOW and "subsidy" in agent_lower:
            base_response += " Sach mein sirf 10% paisa lagega?"
        
        # Add technical questions for high education farmers
        if farmer.education == EducationLevel.HIGH and "solar" in agent_lower:
            base_response += " Aur maintenance cost kya hoga?"
        
        # Add skepticism for high skepticism farmers
        if farmer.skepticism > 0.7 and "government" in agent_lower:
            base_response += " Government ki guarantee hai kya?"
        
        return base_response
    
    def _should_end_conversation(self, farmer_response: str, turn: int) -> bool:
        """Check if conversation should end"""
        farmer_lower = farmer_response.lower()
        
        if any(word in farmer_lower for word in ['nahi chahiye', 'band karo']):
            return True
        if any(word in farmer_lower for word in ['interested hun', 'kar do']):
            return True
        if turn >= 3:
            return True
        return False
    
    async def analyze_conversation(self, agent_messages: List[str], farmer_responses: List[str], 
                                 farmer: FarmerProfile) -> CallAnalysis:
        """Mock conversation analysis"""
        
        await asyncio.sleep(0.3)  # Simulate AI processing
        
        all_farmer_text = " ".join(farmer_responses).lower()
        
        # Mock sentiment analysis
        if any(word in all_farmer_text for word in ['achha', 'interested', 'haan']):
            sentiment = SentimentType.POSITIVE
        elif any(word in all_farmer_text for word in ['nahi', 'problem', 'jhooth']):
            sentiment = SentimentType.NEGATIVE
        else:
            sentiment = SentimentType.NEUTRAL
        
        # Mock interest level
        if any(word in all_farmer_text for word in ['details', 'batayiye', 'interested']):
            interest = InterestLevel.HIGH
        elif any(word in all_farmer_text for word in ['kya hai', 'samajh nahi']):
            interest = InterestLevel.CONFUSED
        else:
            interest = InterestLevel.MEDIUM
        
        # Mock objections
        objections = []
        if any(word in all_farmer_text for word in ['kitne paise', 'paisa']):
            objections.append('cost_concern')
        if any(word in all_farmer_text for word in ['kaun ho', 'sach hai']):
            objections.append('trust_issues')
        if any(word in all_farmer_text for word in ['free mein']):
            objections.append('wants_free')
        
        # Mock outcome
        if sentiment == SentimentType.POSITIVE and interest == InterestLevel.HIGH:
            outcome = CallOutcome.SUCCESS
        elif any(word in all_farmer_text for word in ['nahi chahiye']):
            outcome = CallOutcome.FAILURE
        else:
            outcome = CallOutcome.FOLLOW_UP
        
        # Calculate effectiveness
        effectiveness = calculate_effectiveness_score(
            sentiment.value, interest.value, objections, outcome.value, 
            'samajh nahi' not in all_farmer_text
        )
        
        return CallAnalysis(
            sentiment=sentiment,
            interest_level=interest,
            intro_clarity='samajh nahi' not in all_farmer_text,
            objections=objections,
            call_outcome=outcome,
            farmer_responses=farmer_responses,
            agent_effectiveness=effectiveness,
            conversation_flow={
                'farmer_engagement': interest.value,
                'understanding_level': 'clear' if interest != InterestLevel.CONFUSED else 'confused'
            },
            emotional_indicators=['skeptical' if 'trust_issues' in objections else 'engaged']
        )
    
    async def apply_learning(self, analysis: CallAnalysis) -> AgentPrompt:
        """Mock learning and improvement"""
        
        await asyncio.sleep(0.4)  # Simulate AI processing
        
        new_prompt = AgentPrompt(
            intro=self.current_prompt.intro,
            benefits=self.current_prompt.benefits.copy(),
            call_to_action=self.current_prompt.call_to_action,
            version=self.current_prompt.version + 1,
            improvements=self.current_prompt.improvements.copy(),
            tone_instructions=self.current_prompt.tone_instructions,
            conversation_style=self.current_prompt.conversation_style
        )
        
        improvements_made = []
        
        # Apply improvements based on analysis
        if 'trust_issues' in analysis.objections:
            new_prompt.intro = "Namaste ji! Main government authorized solar scheme advisor hun. " + new_prompt.intro
            improvements_made.append("Added government authorization for trust building")
        
        if 'cost_concern' in analysis.objections:
            new_prompt.benefits = ["Sirf 10% paisa aapko dena hai - matlab 1 lakh mein sirf 10,000 rupaye"] + new_prompt.benefits[1:]
            improvements_made.append("Emphasized exact cost breakdown upfront")
        
        if not analysis.intro_clarity:
            new_prompt.intro = "Namaste ji! Solar pump matlab sun ki energy se paani nikalne waala pump. " + new_prompt.intro
            improvements_made.append("Added simple technical explanation")
        
        if analysis.sentiment == SentimentType.NEGATIVE:
            new_prompt.intro = new_prompt.intro.replace("call kar raha hun", "aapse baat karna chahta hun")
            improvements_made.append("Softened tone for better reception")
        
        new_prompt.improvements.extend(improvements_made)
        return new_prompt
    
    async def run_demo_simulation(self, num_iterations: int = 3):
        """Run complete demo simulation"""
        
        self.logger.info("🎬 DEMO: Enhanced Voice Agent System")
        self.logger.info("🔧 Running without API keys - using intelligent mocks")
        self.logger.info("=" * 60)
        
        for iteration in range(num_iterations):
            self.logger.info(f"\n📞 ITERATION {iteration + 1}")
            self.logger.info("-" * 40)
            
            farmer = self.demo_farmers[iteration % len(self.demo_farmers)]
            self.logger.info(f"📱 Calling: {farmer.name} ({farmer.location})")
            self.logger.info(f"📊 Profile: {farmer.education.value} education, "
                           f"{farmer.income.value} income, skepticism {farmer.skepticism:.1f}")
            
            # Conduct call
            agent_messages, farmer_responses = await self.conduct_demo_call(farmer)
            
            # Analyze conversation
            self.logger.info(f"\n🧠 Analyzing conversation...")
            analysis = await self.analyze_conversation(agent_messages, farmer_responses, farmer)
            
            # Display results
            self._display_results(analysis, iteration + 1)
            
            # Store call
            self.call_log.append({
                'iteration': iteration + 1,
                'farmer': farmer.name,
                'agent_version': self.current_prompt.version,
                'effectiveness': analysis.agent_effectiveness,
                'sentiment': analysis.sentiment.value,
                'outcome': analysis.call_outcome.value,
                'objections': analysis.objections
            })
            
            # Apply learning
            if iteration < num_iterations - 1:
                self.logger.info(f"\n🧠 AI LEARNING ENGINE:")
                old_version = self.current_prompt.version
                
                self.current_prompt = await self.apply_learning(analysis)
                
                self.logger.info(f"   ⬆️  Agent upgraded: v{old_version} → v{self.current_prompt.version}")
                
                if self.current_prompt.improvements:
                    recent_improvements = self.current_prompt.improvements[-2:]
                    for improvement in recent_improvements:
                        self.logger.info(f"   ✨ {improvement}")
        
        # Final summary
        await self._show_demo_summary()
    
    def _display_results(self, analysis: CallAnalysis, iteration: int):
        """Display analysis results"""
        
        sentiment_emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}
        
        self.logger.info(f"\n📊 AI ANALYSIS:")
        self.logger.info(f"   Sentiment: {analysis.sentiment.value} {sentiment_emoji.get(analysis.sentiment.value, '')}")
        self.logger.info(f"   Interest: {analysis.interest_level.value}")
        self.logger.info(f"   Clarity: {'✅ Clear' if analysis.intro_clarity else '❌ Confused'}")
        self.logger.info(f"   Objections: {analysis.objections if analysis.objections else 'None'}")
        self.logger.info(f"   Outcome: {analysis.call_outcome.value}")
        self.logger.info(f"   Effectiveness: {analysis.agent_effectiveness:.2f}/1.00")
    
    async def _show_demo_summary(self):
        """Show final demo summary"""
        
        self.logger.info(f"\n🎯 DEMO SIMULATION COMPLETE")
        self.logger.info("=" * 50)
        
        effectiveness_scores = [call['effectiveness'] for call in self.call_log]
        
        self.logger.info(f"📈 Performance Progression:")
        for i, call in enumerate(self.call_log, 1):
            trend = ""
            if i > 1:
                change = call['effectiveness'] - self.call_log[i-2]['effectiveness']
                if change > 0:
                    trend = f"📈 +{change:.2f}"
                elif change < 0:
                    trend = f"📉 {change:.2f}"
                else:
                    trend = "➡️  0.00"
            
            self.logger.info(f"   Iteration {i}: {call['effectiveness']:.2f} {trend}")
        
        if len(effectiveness_scores) > 1:
            total_improvement = effectiveness_scores[-1] - effectiveness_scores[0]
            improvement_pct = (total_improvement / effectiveness_scores[0]) * 100
            self.logger.info(f"\n🚀 Overall Improvement: {total_improvement:+.2f} ({improvement_pct:+.1f}%)")
        
        success_rate = sum(1 for call in self.call_log if call['outcome'] == 'success') / len(self.call_log) * 100
        
        self.logger.info(f"\n🎓 Final Metrics:")
        self.logger.info(f"   Success Rate: {success_rate:.1f}%")
        self.logger.info(f"   Final Agent Version: v{self.current_prompt.version}")
        self.logger.info(f"   Total Improvements: {len(self.current_prompt.improvements)}")
        
        # Save demo results
        demo_report = {
            "demo_summary": {
                "total_iterations": len(self.call_log),
                "success_rate": success_rate / 100,
                "final_effectiveness": effectiveness_scores[-1],
                "improvement_achieved": total_improvement if len(effectiveness_scores) > 1 else 0
            },
            "call_progression": self.call_log,
            "final_agent_prompt": {
                "intro": self.current_prompt.intro,
                "benefits": self.current_prompt.benefits,
                "improvements": self.current_prompt.improvements
            }
        }
        
        if save_json_data(demo_report, "data/output/reports/demo_results.json"):
            self.logger.info(f"\n💾 Demo results saved: data/output/reports/demo_results.json")
        
        self.logger.info(f"\n🎉 Demo completed! Ready for production with real APIs.")

async def main():
    """Main function for demo system"""
    print("🎬 Voice Agent Demo System - No API Keys Required!")
    print("🎯 Perfect for presentations and testing")
    print("=" * 60)
    
    try:
        system = MockVoiceAgentSystem()
        await system.run_demo_simulation(num_iterations=3)
        
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    asyncio.run(main())