#!/usr/bin/env python3
"""
Enhanced Voice Agent Reinforcement Learning System
Complete system with real voice functionality using ElevenLabs and Deepgram
"""

import asyncio
import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import logging
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from models.data_models import (
    AgentPrompt, CallAnalysis, SentimentType, InterestLevel, 
    CallOutcome, FarmerProfile, EducationLevel, IncomeLevel,
    APIConfig
)
from components.voice_agent import VoiceAgent
from components.audio_processor import AudioProcessor
from components.call_analyzer import CallAnalyzer
from components.reinforcement_engine import ReinforcementEngine
from components.farmer_persona import LLMFarmerPersona
from utils.helpers import (
    save_json_data, calculate_effectiveness_score, 
    PerformanceTracker, create_directories
)

class VoiceAgentSystem:
    """Complete voice agent system with reinforcement learning"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        # Load environment variables
        load_dotenv()
        
        # Setup logging first
        self.setup_logging()
        
        # Load configuration
        self.config = self.load_configuration(config_path)
        
        # Initialize API keys
        self.api_keys = self.load_api_keys()
        
        # Initialize components
        self.initialize_components()
        
        # System state
        self.call_history = []
        self.current_iteration = 1
        self.performance_tracker = PerformanceTracker()
        
        # Create necessary directories
        create_directories([
            "data/output/audio_files",
            "data/output/call_logs", 
            "data/output/reports",
            "data/temp"
        ])
        
        self.logger.info("🚀 Voice Agent System initialized successfully")
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('data/output/system.log', mode='a')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_configuration(self, config_path: str) -> Dict:
        """Load system configuration from YAML"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            self.logger.info(f"✅ Configuration loaded from {config_path}")
            return config
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Return default configuration if file loading fails"""
        return {
            "apis": {
                "openai": {"model": "gpt-4", "temperature": 0.7, "max_tokens": 500},
                "deepgram": {"model": "nova-2", "language": "hi"},
                "elevenlabs": {"voice_id": "pNInz6obpgDQGcFmaJgB", "model_id": "eleven_multilingual_v2"}
            },
            "limits": {"max_conversation_turns": 6, "effectiveness_threshold": 0.6}
        }
    
    def load_api_keys(self) -> Dict[str, Optional[str]]:
        """Load API keys from environment variables"""
        keys = {
            'openai': os.getenv('OPENAI_API_KEY'),
            'deepgram': os.getenv('DEEPGRAM_API_KEY'),
            'elevenlabs': os.getenv('ELEVENLABS_API_KEY')
        }
        
        # Log which keys are available (without exposing the actual keys)
        for service, key in keys.items():
            if key:
                self.logger.info(f"✅ {service.capitalize()} API key loaded")
            else:
                self.logger.warning(f"⚠️ {service.capitalize()} API key not found - will use mock mode")
        
        return keys
    
    def initialize_components(self):
        """Initialize all system components"""
        
        # Load prompts and personas configuration
        prompts_config = self.load_json_config("config/prompts.json")
        personas_config = self.load_json_config("config/farmer_personas.json")
        
        # Initialize audio processor
        self.audio_processor = AudioProcessor(
            deepgram_key=self.api_keys['deepgram'],
            elevenlabs_key=self.api_keys['elevenlabs'],
            config=self.config
        )
        
        # Initialize farmer persona generator
        self.farmer_persona = LLMFarmerPersona(
            openai_api_key=self.api_keys['openai'],
            config=self.config,
            personas_config=personas_config
        )
        
        # Initialize call analyzer
        self.call_analyzer = CallAnalyzer(
            openai_api_key=self.api_keys['openai'],
            config=self.config
        )
        
        # Initialize reinforcement engine
        self.reinforcement_engine = ReinforcementEngine(
            openai_api_key=self.api_keys['openai'],
            config=self.config,
            prompts_config=prompts_config
        )
        
        # Initialize agent with base prompt
        self.current_prompt = AgentPrompt(
            intro="Namaste ji, main solar scheme ke baare mein baat karne ke liye call kar raha hun. Government ki PM-KUSUM yojana ke through aap apne khet mein solar pump lagwa sakte hain.",
            benefits=[
                "90% subsidy milegi government se",
                "Bijli ka bill kam ho jayega",
                "Paani ki problem solve ho jayegi"
            ],
            call_to_action="Kya aap is scheme ke baare mein aur jaanna chahenge?",
            version="1.0",
            tone_instructions="Respectful, clear, and farmer-friendly Hindi",
            conversation_style="Patient and informative"
        )
        
        # Initialize voice agent
        self.voice_agent = VoiceAgent(
            audio_processor=self.audio_processor,
            farmer_persona=self.farmer_persona,
            initial_prompt=self.current_prompt
        )
        
        self.logger.info("🔧 All components initialized successfully")
    
    def load_json_config(self, file_path: str) -> Dict:
        """Load JSON configuration file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load {file_path}: {e}")
            return {}
    
    async def run_voice_call_simulation(self, farmer_profile: FarmerProfile) -> Dict:
        """Run a complete voice call simulation with analysis and learning"""
        
        call_start_time = datetime.now()
        self.logger.info(f"🎬 Starting call simulation {self.current_iteration}")
        
        try:
            # Step 1: Conduct voice call
            self.logger.info("📞 Conducting voice call...")
            agent_messages, farmer_responses, audio_files = await self.voice_agent.conduct_voice_call(
                farmer_profile, 
                max_turns=self.config.get("limits", {}).get("max_conversation_turns", 6)
            )
            
            # Step 2: Analyze the call
            self.logger.info("🔍 Analyzing call...")
            call_analysis = await self.call_analyzer.analyze_call(
                agent_messages, 
                farmer_responses, 
                farmer_profile
            )
            
            # Step 3: Learn and improve
            self.logger.info("🧠 Learning and improving...")
            improved_prompt = await self.reinforcement_engine.learn_and_improve(
                self.current_prompt, 
                call_analysis, 
                agent_messages + farmer_responses
            )
            
            # Step 4: Update system state
            self.current_prompt = improved_prompt
            self.voice_agent.update_prompt(improved_prompt)
            
            # Step 5: Create call record
            call_record = {
                'iteration': self.current_iteration,
                'timestamp': call_start_time.isoformat(),
                'farmer_profile': farmer_profile.__dict__,
                'agent_version': self.current_prompt.version,
                'conversation': {
                    'agent_messages': agent_messages,
                    'farmer_responses': farmer_responses,
                    'audio_files': audio_files
                },
                'analysis': call_analysis.__dict__ if hasattr(call_analysis, '__dict__') else call_analysis,
                'improvements': improved_prompt.__dict__ if hasattr(improved_prompt, '__dict__') else improved_prompt,
                'effectiveness_score': calculate_effectiveness_score(call_analysis)
            }
            
            # Save call record
            await self.save_call_record(call_record)
            
            # Update system metrics
            self.call_history.append(call_record)
            self.current_iteration += 1
            
            self.logger.info(f"✅ Call simulation completed successfully")
            return call_record
            
        except Exception as e:
            self.logger.error(f"❌ Call simulation failed: {e}")
            raise
    
    async def save_call_record(self, call_record: Dict):
        """Save call record to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/output/call_logs/call_{call_record['iteration']}_{timestamp}.json"
        
        await save_json_data(call_record, filename)
        self.logger.info(f"💾 Call record saved to {filename}")
    
    async def run_multiple_simulations(self, num_simulations: int = 5):
        """Run multiple call simulations to demonstrate learning"""
        
        self.logger.info(f"🎯 Starting {num_simulations} call simulations...")
        
        # Generate diverse farmer profiles
        farmer_profiles = await self.generate_diverse_farmer_profiles(num_simulations)
        
        simulation_results = []
        
        for i, farmer_profile in enumerate(farmer_profiles, 1):
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"🎭 SIMULATION {i}/{num_simulations}: {farmer_profile.name}")
            self.logger.info(f"{'='*60}")
            
            try:
                result = await self.run_voice_call_simulation(farmer_profile)
                simulation_results.append(result)
                
                # Show progress
                effectiveness = result.get('effectiveness_score', 0)
                self.logger.info(f"📊 Simulation {i} effectiveness: {effectiveness:.2f}")
                
                # Small delay between simulations
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"❌ Simulation {i} failed: {e}")
                continue
        
        # Generate final report
        await self.generate_final_report(simulation_results)
        
        return simulation_results
    
    async def generate_diverse_farmer_profiles(self, count: int) -> List[FarmerProfile]:
        """Generate diverse farmer profiles for testing"""
        
        profiles = []
        base_profiles = [
            {
                'name': 'राम सिंह', 'age': 45, 'education': EducationLevel.LOW, 
                'income': IncomeLevel.LOW, 'location': 'राजस्थान', 
                'crops': ['गेहूं', 'बाजरा'], 'skepticism': 0.7
            },
            {
                'name': 'सुरेश पटेल', 'age': 38, 'education': EducationLevel.MEDIUM,
                'income': IncomeLevel.MEDIUM, 'location': 'गुजरात',
                'crops': ['कपास', 'मूंगफली'], 'skepticism': 0.4
            },
            {
                'name': 'विजय कुमार', 'age': 52, 'education': EducationLevel.HIGH,
                'income': IncomeLevel.HIGH, 'location': 'पंजाब',
                'crops': ['धान', 'गेहूं'], 'skepticism': 0.2
            },
            {
                'name': 'रमेश यादव', 'age': 41, 'education': EducationLevel.LOW,
                'income': IncomeLevel.LOW, 'location': 'उत्तर प्रदेश',
                'crops': ['आलू', 'प्याज'], 'skepticism': 0.8
            },
            {
                'name': 'अनिल शर्मा', 'age': 35, 'education': EducationLevel.MEDIUM,
                'income': IncomeLevel.MEDIUM, 'location': 'मध्य प्रदेश',
                'crops': ['सोयाबीन', 'चना'], 'skepticism': 0.5
            }
        ]
        
        for i in range(count):
            base = base_profiles[i % len(base_profiles)]
            profile = FarmerProfile(
                id=f"farmer_{i+1:03d}",
                name=base['name'],
                age=base['age'],
                education=base['education'],
                income=base['income'],
                location=base['location'],
                crops=base['crops'],
                land_size=f"{2 + i}  एकड़",
                skepticism=base['skepticism'],
                govt_experience="कुछ योजनाओं का अनुभव",
                family_size=4 + (i % 3),
                preferred_language="hindi",
                best_call_time="morning"
            )
            profiles.append(profile)
        
        return profiles
    
    async def generate_final_report(self, simulation_results: List[Dict]):
        """Generate comprehensive final report"""
        
        if not simulation_results:
            self.logger.warning("No simulation results to report")
            return
        
        report = {
            'system_summary': {
                'total_simulations': len(simulation_results),
                'timestamp': datetime.now().isoformat(),
                'system_version': self.config.get('system', {}).get('version', '1.0.0')
            },
            'performance_metrics': {
                'effectiveness_scores': [r.get('effectiveness_score', 0) for r in simulation_results],
                'average_effectiveness': sum(r.get('effectiveness_score', 0) for r in simulation_results) / len(simulation_results),
                'improvement_trend': self.calculate_improvement_trend(simulation_results)
            },
            'learning_insights': {
                'prompt_evolution': self.track_prompt_evolution(),
                'common_objections': self.extract_common_objections(simulation_results),
                'successful_patterns': self.identify_successful_patterns(simulation_results)
            },
            'detailed_results': simulation_results
        }
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"data/output/reports/final_report_{timestamp}.json"
        await save_json_data(report, report_file)
        
        # Display summary
        self.display_report_summary(report)
        
        self.logger.info(f"📊 Final report saved to {report_file}")
    
    def calculate_improvement_trend(self, results: List[Dict]) -> List[float]:
        """Calculate effectiveness improvement trend"""
        scores = [r.get('effectiveness_score', 0) for r in results]
        return scores
    
    def track_prompt_evolution(self) -> Dict:
        """Track how the prompt evolved over iterations"""
        return {
            'initial_version': "1.0",
            'final_version': self.current_prompt.version,
            'total_improvements': self.current_iteration - 1
        }
    
    def extract_common_objections(self, results: List[Dict]) -> List[str]:
        """Extract common farmer objections from results"""
        objections = []
        for result in results:
            analysis = result.get('analysis', {})
            if isinstance(analysis, dict) and 'objections' in analysis:
                objections.extend(analysis['objections'])
        return list(set(objections))
    
    def identify_successful_patterns(self, results: List[Dict]) -> List[str]:
        """Identify patterns in successful calls"""
        successful_calls = [r for r in results if r.get('effectiveness_score', 0) > 0.7]
        patterns = []
        
        if successful_calls:
            patterns.append(f"High success rate with {len(successful_calls)}/{len(results)} calls")
            # Add more pattern analysis here
        
        return patterns
    
    def display_report_summary(self, report: Dict):
        """Display a formatted report summary"""
        print("\n" + "="*80)
        print("🎯 VOICE AGENT SYSTEM - FINAL REPORT SUMMARY")
        print("="*80)
        
        metrics = report['performance_metrics']
        print(f"📊 Total Simulations: {report['system_summary']['total_simulations']}")
        print(f"📈 Average Effectiveness: {metrics['average_effectiveness']:.2f}")
        print(f"🎭 Effectiveness Range: {min(metrics['effectiveness_scores']):.2f} - {max(metrics['effectiveness_scores']):.2f}")
        
        insights = report['learning_insights']
        print(f"\n🧠 Learning Insights:")
        print(f"   • Prompt Evolution: v{insights['prompt_evolution']['initial_version']} → v{insights['prompt_evolution']['final_version']}")
        print(f"   • Total Improvements: {insights['prompt_evolution']['total_improvements']}")
        print(f"   • Common Objections: {len(insights['common_objections'])} identified")
        print(f"   • Success Patterns: {len(insights['successful_patterns'])} identified")
        
        print("\n" + "="*80)

async def main():
    """Main function to run the voice agent system"""
    
    print("🚀 Starting Enhanced Voice Agent Reinforcement Learning System")
    print("="*80)
    
    try:
        # Initialize system
        system = VoiceAgentSystem()
        
        # Run multiple simulations
        results = await system.run_multiple_simulations(num_simulations=5)
        
        print(f"\n✅ System completed successfully!")
        print(f"📊 Processed {len(results)} simulations")
        print(f"📁 Check 'data/output/' for detailed logs and reports")
        
    except Exception as e:
        print(f"❌ System failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())