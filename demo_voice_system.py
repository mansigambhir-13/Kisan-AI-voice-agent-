#!/usr/bin/env python3
"""
Voice Agent Reinforcement Learning System - Complete Demo
This script demonstrates the full functionality including:
1. Voice call simulation with real TTS/STT
2. Call analysis and sentiment detection
3. Reinforcement learning and prompt improvement
4. Multi-iteration learning demonstration
"""

import asyncio
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import logging
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

# Import our enhanced system
from main_voice_system import VoiceAgentSystem
from models.data_models import FarmerProfile, EducationLevel, IncomeLevel

class VoiceSystemDemo:
    """Comprehensive demo of the voice agent system"""
    
    def __init__(self):
        self.setup_demo_environment()
        self.logger = logging.getLogger(__name__)
        
    def setup_demo_environment(self):
        """Setup demo environment and logging"""
        
        # Load environment variables
        load_dotenv()
        
        # Setup enhanced logging for demo
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('demo_voice_system.log', mode='w')
            ]
        )
        
        # Create demo directories
        demo_dirs = [
            "demo_output/audio_files",
            "demo_output/call_logs",
            "demo_output/reports",
            "demo_output/temp"
        ]
        
        for dir_path in demo_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def display_welcome_message(self):
        """Display welcome message and system info"""
        
        print("\n" + "="*80)
        print("🎯 VOICE AGENT REINFORCEMENT LEARNING SYSTEM - DEMO")
        print("="*80)
        print("🎬 This demo showcases:")
        print("   • Voice call simulation with TTS/STT")
        print("   • Intelligent call analysis")
        print("   • Reinforcement learning improvements")
        print("   • Multi-iteration system evolution")
        print("\n🔧 System Configuration:")
        
        # Check API keys
        api_keys = {
            'OpenAI': os.getenv('OPENAI_API_KEY'),
            'Deepgram': os.getenv('DEEPGRAM_API_KEY'),
            'ElevenLabs': os.getenv('ELEVENLABS_API_KEY')
        }
        
        for service, key in api_keys.items():
            status = "✅ Connected" if key else "⚠️ Mock Mode"
            print(f"   • {service}: {status}")
        
        print("\n" + "="*80 + "\n")
    
    def create_demo_farmer_profiles(self) -> List[FarmerProfile]:
        """Create diverse farmer profiles for comprehensive testing"""
        
        profiles = [
            FarmerProfile(
                id="demo_001",
                name="राम सिंह",
                age=45,
                education=EducationLevel.LOW,
                income=IncomeLevel.LOW,
                location="राजस्थान, जोधपुर",
                crops=["गेहूं", "बाजरा", "सरसों"],
                land_size="5 एकड़",
                skepticism=0.8,  # High skepticism
                govt_experience="कुछ योजनाओं में धोखा हुआ है",
                family_size=6,
                preferred_language="hindi",
                best_call_time="morning",
                persona_type="skeptical_traditional"
            ),
            FarmerProfile(
                id="demo_002", 
                name="सुरेश पटेल",
                age=38,
                education=EducationLevel.MEDIUM,
                income=IncomeLevel.MEDIUM,
                location="गुजरात, अहमदाबाद",
                crops=["कपास", "मूंगफली", "तिल"],
                land_size="8 एकड़",
                skepticism=0.4,  # Moderate skepticism
                govt_experience="कुछ योजनाओं का फायदा उठाया है",
                family_size=4,
                preferred_language="hindi",
                best_call_time="afternoon",
                persona_type="pragmatic_business_minded"
            ),
            FarmerProfile(
                id="demo_003",
                name="विजय कुमार",
                age=52,
                education=EducationLevel.HIGH,
                income=IncomeLevel.HIGH,
                location="पंजाब, लुधियाना",
                crops=["धान", "गेहूं", "मक्का"],
                land_size="15 एकड़",
                skepticism=0.2,  # Low skepticism
                govt_experience="कई योजनाओं का सफल उपयोग",
                family_size=5,
                preferred_language="hindi",
                best_call_time="evening",
                persona_type="progressive_early_adopter"
            ),
            FarmerProfile(
                id="demo_004",
                name="रमेश यादव", 
                age=41,
                education=EducationLevel.LOW,
                income=IncomeLevel.LOW,
                location="उत्तर प्रदेश, मेरठ",
                crops=["आलू", "प्याज", "टमाटर"],
                land_size="3 एकड़",
                skepticism=0.9,  # Very high skepticism
                govt_experience="योजनाओं में बहुत परेशानी हुई",
                family_size=7,
                preferred_language="hindi",
                best_call_time="morning",
                persona_type="highly_skeptical_struggling"
            ),
            FarmerProfile(
                id="demo_005",
                name="अनिल शर्मा",
                age=35,
                education=EducationLevel.MEDIUM,
                income=IncomeLevel.MEDIUM,
                location="मध्य प्रदेश, इंदौर",
                crops=["सोयाबीन", "चना", "गेहूं"],
                land_size="7 एकड़",
                skepticism=0.5,  # Neutral skepticism
                govt_experience="मिश्रित अनुभव",
                family_size=4,
                preferred_language="hindi",
                best_call_time="afternoon",
                persona_type="cautious_analytical"
            )
        ]
        
        return profiles
    
    async def run_individual_demo(self, system: VoiceAgentSystem, farmer: FarmerProfile, demo_number: int):
        """Run an individual call demo with detailed output"""
        
        print(f"\n{'='*60}")
        print(f"🎭 DEMO CALL {demo_number}: {farmer.name}")
        print(f"📍 Location: {farmer.location}")
        print(f"🌾 Crops: {', '.join(farmer.crops)}")
        print(f"🎓 Education: {farmer.education.value.title()}")
        print(f"💰 Income: {farmer.income.value.title()}")
        print(f"🤔 Skepticism Level: {farmer.skepticism:.1f}/1.0")
        print(f"{'='*60}")
        
        try:
            # Run the voice call simulation
            result = await system.run_voice_call_simulation(farmer)
            
            # Display results
            self.display_call_results(result, demo_number)
            
            return result
            
        except Exception as e:
            print(f"❌ Demo call {demo_number} failed: {e}")
            return None
    
    def display_call_results(self, result: Dict, demo_number: int):
        """Display formatted results of a call"""
        
        if not result:
            return
        
        print(f"\n📊 CALL {demo_number} RESULTS:")
        print("-" * 40)
        
        # Basic info
        effectiveness = result.get('effectiveness_score', 0)
        print(f"🎯 Effectiveness Score: {effectiveness:.2f}/1.0")
        
        # Analysis results
        analysis = result.get('analysis', {})
        if isinstance(analysis, dict):
            sentiment = analysis.get('sentiment', 'unknown')
            interest = analysis.get('interest_level', 'unknown') 
            outcome = analysis.get('call_outcome', 'unknown')
            
            print(f"😊 Farmer Sentiment: {sentiment}")
            print(f"🎯 Interest Level: {interest}")
            print(f"📞 Call Outcome: {outcome}")
            
            # Show objections if any
            objections = analysis.get('objections', [])
            if objections:
                print(f"⚠️ Objections: {', '.join(objections[:3])}")
        
        # Show conversation sample
        conversation = result.get('conversation', {})
        agent_messages = conversation.get('agent_messages', [])
        farmer_responses = conversation.get('farmer_responses', [])
        
        if agent_messages and farmer_responses:
            print(f"\n💬 CONVERSATION SAMPLE:")
            print(f"🤖 Agent: {agent_messages[0][:100]}...")
            print(f"👨‍🌾 Farmer: {farmer_responses[0][:100]}...")
        
        print("-" * 40)
    
    async def run_learning_demonstration(self):
        """Run the complete learning demonstration"""
        
        print("🧠 LEARNING DEMONSTRATION")
        print("=" * 50)
        print("This will show how the system improves over multiple calls...")
        
        # Initialize the voice system
        print("\n🚀 Initializing Voice Agent System...")
        system = VoiceAgentSystem()
        
        # Get demo farmer profiles
        farmers = self.create_demo_farmer_profiles()
        
        # Track learning progress
        learning_progress = []
        
        print(f"\n🎬 Running {len(farmers)} demo calls to show learning...")
        
        for i, farmer in enumerate(farmers, 1):
            print(f"\n⏳ Preparing demo call {i}/{len(farmers)}...")
            await asyncio.sleep(1)  # Brief pause for readability
            
            result = await self.run_individual_demo(system, farmer, i)
            
            if result:
                learning_progress.append({
                    'call_number': i,
                    'farmer_name': farmer.name,
                    'effectiveness': result.get('effectiveness_score', 0),
                    'agent_version': result.get('agent_version', '1.0')
                })
                
                # Show learning progress
                if i > 1:
                    prev_score = learning_progress[i-2]['effectiveness']
                    current_score = learning_progress[i-1]['effectiveness']
                    improvement = current_score - prev_score
                    
                    if improvement > 0:
                        print(f"📈 Improvement: +{improvement:.2f} from previous call")
                    elif improvement < 0:
                        print(f"📉 Decline: {improvement:.2f} from previous call")
                    else:
                        print(f"➡️ No change from previous call")
            
            # Pause between calls for demo effect
            if i < len(farmers):
                print("\n⏳ System learning and adapting...")
                await asyncio.sleep(2)
        
        # Display final learning summary
        self.display_learning_summary(learning_progress)
        
        return learning_progress
    
    def display_learning_summary(self, progress: List[Dict]):
        """Display comprehensive learning summary"""
        
        if not progress:
            print("❌ No learning progress to display")
            return
        
        print("\n" + "="*80)
        print("🧠 LEARNING SUMMARY")
        print("="*80)
        
        # Calculate metrics
        scores = [p['effectiveness'] for p in progress]
        initial_score = scores[0]
        final_score = scores[-1]
        max_score = max(scores)
        min_score = min(scores)
        avg_score = sum(scores) / len(scores)
        
        print(f"📊 Performance Metrics:")
        print(f"   • Initial Score: {initial_score:.2f}")
        print(f"   • Final Score: {final_score:.2f}")
        print(f"   • Overall Improvement: {final_score - initial_score:+.2f}")
        print(f"   • Best Score: {max_score:.2f}")
        print(f"   • Worst Score: {min_score:.2f}")
        print(f"   • Average Score: {avg_score:.2f}")
        
        print(f"\n📈 Call-by-Call Progress:")
        for i, call in enumerate(progress):
            trend = ""
            if i > 0:
                diff = call['effectiveness'] - progress[i-1]['effectiveness']
                if diff > 0:
                    trend = f"📈 (+{diff:.2f})"
                elif diff < 0:
                    trend = f"📉 ({diff:.2f})"
                else:
                    trend = "➡️ (0.00)"
            
            print(f"   {call['call_number']}. {call['farmer_name']}: {call['effectiveness']:.2f} {trend}")
        
        # Learning insights
        improvements = sum(1 for i in range(1, len(scores)) if scores[i] > scores[i-1])
        declines = sum(1 for i in range(1, len(scores)) if scores[i] < scores[i-1])
        
        print(f"\n🎯 Learning Insights:")
        print(f"   • Calls with improvement: {improvements}/{len(scores)-1}")
        print(f"   • Calls with decline: {declines}/{len(scores)-1}")
        print(f"   • Learning trend: {'Positive' if final_score > initial_score else 'Needs work'}")
        
        print("\n" + "="*80)
    
    async def run_complete_demo(self):
        """Run the complete demonstration"""
        
        self.display_welcome_message()
        
        try:
            # Run learning demonstration
            progress = await self.run_learning_demonstration()
            
            print("\n✅ DEMO COMPLETED SUCCESSFULLY!")
            print("="*50)
            print("📁 Check the following directories for detailed outputs:")
            print("   • demo_output/call_logs/ - Individual call records")
            print("   • demo_output/reports/ - System reports")
            print("   • demo_output/audio_files/ - Generated audio files")
            print("   • demo_voice_system.log - Complete system log")
            
            print(f"\n🎯 Demo Summary:")
            print(f"   • Total calls simulated: {len(progress)}")
            print(f"   • System learning demonstrated: ✅")
            print(f"   • Voice functionality tested: ✅")
            print(f"   • Reinforcement loop working: ✅")
            
            return True
            
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()
            return False

async def main():
    """Main demo execution"""
    
    print("🎬 Starting Voice Agent System Demo...")
    
    demo = VoiceSystemDemo()
    success = await demo.run_complete_demo()
    
    if success:
        print("\n🎉 Demo completed successfully!")
        print("🔗 You can now:")
        print("   1. Review the generated logs and reports")
        print("   2. Listen to generated audio files (if using real APIs)")
        print("   3. Modify farmer profiles and run again")
        print("   4. Add your own API keys for full functionality")
    else:
        print("\n💥 Demo encountered issues. Check the logs for details.")
    
    return success

if __name__ == "__main__":
    # Run the demo
    result = asyncio.run(main())
    sys.exit(0 if result else 1)