#!/usr/bin/env python3
"""
Voice Agent Reinforcement Learning System - Production Version
Uses real APIs: Deepgram, ElevenLabs, OpenAI GPT-4
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import logging

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from models.data_models import AgentPrompt, CallRecord
from models.farmer_profiles import FarmerProfileManager
from components.audio_processor import AudioProcessor
from components.farmer_persona import LLMFarmerPersona
from components.call_analyzer import CallAnalyzer
from components.reinforcement_engine import ReinforcementEngine
from components.voice_agent import VoiceAgent
from utils.config import ConfigManager
from utils.logger import setup_logger
from utils.helpers import save_json_data, create_output_directories, PerformanceTracker

class VoiceAgentSystem:
    """Complete Voice Agent Reinforcement Learning System"""
    
    def __init__(self):
        # Initialize configuration
        self.config_manager = ConfigManager()
        self.setup_logging()
        
        # Check API keys
        self.validate_setup()
        
        # Initialize components
        self.initialize_components()
        
        # System state
        self.call_log = []
        self.system_metrics = PerformanceTracker()
        
        self.logger.info("🚀 Voice Agent System initialized successfully")
    
    def setup_logging(self):
        """Setup system logging"""
        logging_config = self.config_manager.get_logging_config()
        self.logger = setup_logger("voice_agent_system", logging_config)
    
    def validate_setup(self):
        """Validate system setup and API keys"""
        missing_keys = self.config_manager.get_missing_api_keys()
        
        if missing_keys:
            self.logger.warning(f"⚠️  Missing API keys: {', '.join(missing_keys)}")
            self.logger.warning("System will use fallback/mock modes for missing services")
        else:
            self.logger.info("✅ All API keys present")
        
        # Create output directories
        create_output_directories()
        self.logger.info("✅ Output directories created")
    
    def initialize_components(self):
        """Initialize all system components"""
        api_config = self.config_manager.get_api_config()
        
        # Initialize audio processor
        self.audio_processor = AudioProcessor(
            deepgram_key=api_config.get("deepgram", {}).get("api_key"),
            elevenlabs_key=api_config.get("elevenlabs", {}).get("api_key"),
            config=api_config
        )
        
        # Initialize farmer persona
        self.farmer_persona = LLMFarmerPersona(
            openai_api_key=api_config.get("openai", {}).get("api_key"),
            config=api_config,
            personas_config=self.config_manager.farmer_personas
        )
        
        # Initialize call analyzer
        self.call_analyzer = CallAnalyzer(
            openai_api_key=api_config.get("openai", {}).get("api_key"),
            config=api_config
        )
        
        # Initialize reinforcement engine
        self.reinforcement_engine = ReinforcementEngine(
            openai_api_key=api_config.get("openai", {}).get("api_key"),
            config=api_config,
            prompts_config=self.config_manager.prompts
        )
        
        # Initialize farmer profile manager
        self.farmer_profile_manager = FarmerProfileManager(
            self.config_manager.farmer_personas
        )
        
        # Create initial agent prompt
        initial_prompt_config = self.config_manager.prompts["initial_agent_prompt"]
        initial_prompt = AgentPrompt(
            intro=initial_prompt_config["intro"],
            benefits=initial_prompt_config["benefits"],
            call_to_action=initial_prompt_config["call_to_action"],
            version=initial_prompt_config["version"],
            tone_instructions=initial_prompt_config["tone_instructions"],
            conversation_style=initial_prompt_config["conversation_style"]
        )
        
        # Initialize voice agent
        self.voice_agent = VoiceAgent(
            audio_processor=self.audio_processor,
            farmer_persona=self.farmer_persona,
            initial_prompt=initial_prompt
        )
        
        self.logger.info("✅ All components initialized")
    
    async def run_simulation(self, num_iterations: int = 3, max_turns_per_call: int = 5):
        """Run the complete reinforcement learning simulation"""
        
        self.logger.info(f"🎯 Starting {num_iterations}-iteration simulation")
        self.logger.info("=" * 60)
        
        # Get sample farmers
        sample_farmers = self.farmer_profile_manager.sample_farmers
        
        for iteration in range(num_iterations):
            self.logger.info(f"\n📞 ITERATION {iteration + 1}")
            self.logger.info("-" * 40)
            
            # Select farmer for this iteration
            farmer = sample_farmers[iteration % len(sample_farmers)]
            self.logger.info(f"📱 Calling: {farmer.name} ({farmer.location})")
            self.logger.info(f"📊 Profile: {farmer.education.value} education, "
                           f"{farmer.income.value} income, skepticism {farmer.skepticism:.1f}")
            
            # Record call start
            call_start_time = datetime.now()
            
            try:
                # Conduct voice call
                agent_messages, farmer_responses, audio_files = await self.voice_agent.conduct_voice_call(
                    farmer, max_turns_per_call
                )
                
                # Analyze conversation
                self.logger.info("🧠 Analyzing conversation...")
                analysis = await self.call_analyzer.analyze_conversation(
                    agent_messages, farmer_responses
                )
                
                # Display results
                self._display_call_results(agent_messages, farmer_responses, analysis, iteration + 1)
                
                # Record call duration
                call_duration = (datetime.now() - call_start_time).total_seconds()
                self.system_metrics.record_call_duration(call_duration)
                self.system_metrics.record_effectiveness(analysis.agent_effectiveness)
                
                # Store call record
                call_record = CallRecord(
                    call_id=f"CALL_{iteration+1:03d}",
                    iteration=iteration + 1,
                    farmer_profile=farmer,
                    agent_version=self.voice_agent.current_prompt.version,
                    conversation_turns=[],  # Populated by voice_agent
                    analysis=analysis,
                    call_start=call_start_time,
                    call_end=datetime.now(),
                    total_duration=call_duration,
                    audio_files=audio_files
                )
                
                self.call_log.append(call_record)
                
                # Apply learning (except for last iteration)
                if iteration < num_iterations - 1:
                    await self._apply_learning(analysis, agent_messages + farmer_responses)
                
            except Exception as e:
                self.logger.error(f"❌ Error in iteration {iteration + 1}: {e}")
                continue
        
        # Generate final report
        await self._generate_final_report()
    
    def _display_call_results(self, agent_messages: List[str], farmer_responses: List[str], 
                            analysis, iteration: int):
        """Display formatted call results"""
        
        self.logger.info(f"\n💬 CONVERSATION TRANSCRIPT:")
        for i, (agent_msg, farmer_msg) in enumerate(zip(agent_messages, farmer_responses)):
            self.logger.info(f"   🤖 Agent {i+1}: {agent_msg}")
            self.logger.info(f"   👨‍🌾 Farmer {i+1}: {farmer_msg}")
            self.logger.info("")
        
        # Analysis results
        sentiment_emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}
        
        self.logger.info(f"📊 AI ANALYSIS RESULTS:")
        self.logger.info(f"   Sentiment: {analysis.sentiment.value} {sentiment_emoji.get(analysis.sentiment.value, '')}")
        self.logger.info(f"   Interest: {analysis.interest_level.value}")
        self.logger.info(f"   Clarity: {'✅ Clear' if analysis.intro_clarity else '❌ Confused'}")
        self.logger.info(f"   Objections: {analysis.objections if analysis.objections else 'None'}")
        self.logger.info(f"   Outcome: {analysis.call_outcome.value}")
        self.logger.info(f"   Effectiveness: {analysis.agent_effectiveness:.2f}/1.00")
        
        if analysis.emotional_indicators:
            self.logger.info(f"   Emotions: {', '.join(analysis.emotional_indicators)}")
    
    async def _apply_learning(self, analysis, conversation_history: List[str]):
        """Apply reinforcement learning"""
        
        self.logger.info(f"\n🧠 APPLYING AI LEARNING:")
        old_version = self.voice_agent.current_prompt.version
        
        # Generate improvements
        improved_prompt = await self.reinforcement_engine.learn_and_improve(
            self.voice_agent.current_prompt,
            analysis,
            conversation_history
        )
        
        # Update agent
        self.voice_agent.update_prompt(improved_prompt)
        
        self.logger.info(f"   ⬆️  Agent upgraded: v{old_version} → v{improved_prompt.version}")
        
        # Show improvements
        if improved_prompt.improvements:
            recent_improvements = improved_prompt.improvements[-3:]  # Show last 3
            for improvement in recent_improvements:
                self.logger.info(f"   ✨ {improvement}")
    
    async def _generate_final_report(self):
        """Generate comprehensive final report"""
        
        self.logger.info(f"\n📈 FINAL SYSTEM REPORT")
        self.logger.info("=" * 50)
        
        if not self.call_log:
            self.logger.warning("No successful calls to analyze")
            return
        
        # Performance metrics
        effectiveness_scores = [call.analysis.agent_effectiveness for call in self.call_log]
        
        self.logger.info(f"🎯 PERFORMANCE SUMMARY:")
        self.logger.info(f"   Total Calls: {len(self.call_log)}")
        self.logger.info(f"   Success Rate: {sum(1 for call in self.call_log if call.analysis.call_outcome.value == 'success') / len(self.call_log) * 100:.1f}%")
        self.logger.info(f"   Average Effectiveness: {sum(effectiveness_scores) / len(effectiveness_scores):.2f}")
        
        if len(effectiveness_scores) > 1:
            improvement = effectiveness_scores[-1] - effectiveness_scores[0]
            improvement_pct = (improvement / effectiveness_scores[0]) * 100
            self.logger.info(f"   Overall Improvement: {improvement:+.2f} ({improvement_pct:+.1f}%)")
        
        # Learning insights
        self.logger.info(f"\n🧠 LEARNING INSIGHTS:")
        self.logger.info(f"   Final Agent Version: v{self.voice_agent.current_prompt.version}")
        self.logger.info(f"   Total Improvements: {len(self.voice_agent.current_prompt.improvements)}")
        
        # Objection analysis
        all_objections = []
        for call in self.call_log:
            all_objections.extend(call.analysis.objections)
        
        if all_objections:
            from collections import Counter
            common_objections = Counter(all_objections).most_common(3)
            self.logger.info(f"   Common Objections:")
            for objection, count in common_objections:
                self.logger.info(f"      • {objection}: {count} times")
        
        # Save detailed report
        report_data = {
            "summary": {
                "total_calls": len(self.call_log),
                "success_rate": sum(1 for call in self.call_log if call.analysis.call_outcome.value == 'success') / len(self.call_log),
                "average_effectiveness": sum(effectiveness_scores) / len(effectiveness_scores),
                "improvement_achieved": effectiveness_scores[-1] - effectiveness_scores[0] if len(effectiveness_scores) > 1 else 0,
                "final_agent_version": self.voice_agent.current_prompt.version
            },
            "effectiveness_progression": effectiveness_scores,
            "call_details": [
                {
                    "iteration": call.iteration,
                    "farmer_name": call.farmer_profile.name,
                    "farmer_education": call.farmer_profile.education.value,
                    "farmer_skepticism": call.farmer_profile.skepticism,
                    "agent_version": call.agent_version,
                    "sentiment": call.analysis.sentiment.value,
                    "interest_level": call.analysis.interest_level.value,
                    "objections": call.analysis.objections,
                    "outcome": call.analysis.call_outcome.value,
                    "effectiveness": call.analysis.agent_effectiveness,
                    "duration": call.total_duration
                }
                for call in self.call_log
            ],
            "final_agent_prompt": {
                "intro": self.voice_agent.current_prompt.intro,
                "benefits": self.voice_agent.current_prompt.benefits,
                "call_to_action": self.voice_agent.current_prompt.call_to_action,
                "improvements_made": self.voice_agent.current_prompt.improvements
            },
            "system_performance": self.system_metrics.get_summary(),
            "component_performance": {
                "audio_processor": self.audio_processor.get_performance_stats(),
                "farmer_persona": self.farmer_persona.get_performance_stats(),
                "call_analyzer": self.call_analyzer.get_performance_stats(),
                "reinforcement_engine": self.reinforcement_engine.get_performance_stats()
            }
        }
        
        # Save report
        report_path = f"data/output/reports/system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        if save_json_data(report_data, report_path):
            self.logger.info(f"\n💾 Detailed report saved: {report_path}")
        
        self.logger.info(f"\n🎉 Simulation completed successfully!")

async def main():
    """Main function for production system"""
    print("🚀 Voice Agent Reinforcement Learning System - Production Version")
    print("🔧 Using real APIs: Deepgram, ElevenLabs, OpenAI GPT-4")
    print("=" * 70)
    
    try:
        # Create and run system
        system = VoiceAgentSystem()
        await system.run_simulation(num_iterations=3, max_turns_per_call=5)
        
    except KeyboardInterrupt:
        print("\n⚠️  Simulation interrupted by user")
    except Exception as e:
        print(f"\n❌ System error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())