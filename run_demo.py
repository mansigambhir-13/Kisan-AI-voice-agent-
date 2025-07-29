#!/usr/bin/env python3
"""
Voice Agent System - Simple Demo Runner
Demonstrates the complete system functionality with minimal setup
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def create_mock_farmer_profile():
    """Create a sample farmer profile for demo"""
    return {
        'id': 'demo_farmer_001',
        'name': 'राम सिंह',
        'age': 45,
        'education': 'low',
        'income': 'low',
        'location': 'राजस्थान, जोधपुर',
        'crops': ['गेहूं', 'बाजरा'],
        'land_size': '5 एकड़',
        'skepticism': 0.7,
        'govt_experience': 'कुछ योजनाओं में धोखा हुआ है',
        'family_size': 6,
        'preferred_language': 'hindi',
        'best_call_time': 'morning'
    }

async def simulate_voice_call(farmer_profile):
    """Simulate a voice call with the farmer"""
    
    print(f"📞 Initiating call with {farmer_profile['name']}...")
    await asyncio.sleep(1)
    
    # Agent's opening message
    agent_intro = "Namaste ji, main solar scheme ke baare mein baat karne ke liye call kar raha hun. Government ki PM-KUSUM yojana ke through aap apne khet mein solar pump lagwa sakte hain."
    
    print(f"🤖 Agent: {agent_intro}")
    await asyncio.sleep(2)
    
    # Simulate farmer response based on skepticism
    if farmer_profile['skepticism'] > 0.6:
        farmer_response = "Arre bhai, ye sab scheme-veme mein bahut dhokha hota hai. Pehle bhi kaha tha koi, kuch nahi mila."
        sentiment = "negative"
        interest = "low"
    else:
        farmer_response = "Haan bhaiya, batao kya hai ye scheme? Kitna paisa lagega?"
        sentiment = "neutral"
        interest = "medium"
    
    print(f"👨‍🌾 Farmer: {farmer_response}")
    await asyncio.sleep(2)
    
    # Agent's response
    agent_response = "Bilkul samajh sakta hun aapki baat. Lekin ye government ki official scheme hai, 90% subsidy milti hai. Aap sirf 10% paisa lagayenge."
    print(f"🤖 Agent: {agent_response}")
    await asyncio.sleep(2)
    
    # Final farmer response
    if sentiment == "negative":
        final_response = "Nahi bhai, mujhe nahi chahiye. Time waste mat karo."
        outcome = "failure"
    else:
        final_response = "Theek hai, ek baar aur batao. Kya process hai?"
        outcome = "follow_up"
    
    print(f"👨‍🌾 Farmer: {final_response}")
    
    return {
        'conversation': [agent_intro, farmer_response, agent_response, final_response],
        'analysis': {
            'sentiment': sentiment,
            'interest_level': interest,
            'call_outcome': outcome,
            'objections': ['trust_issues'] if sentiment == "negative" else ['cost_concerns'],
            'intro_clarity': 0.7,
            'agent_effectiveness': 0.5 if outcome == "failure" else 0.7
        }
    }

def analyze_call_performance(call_result):
    """Analyze call performance and suggest improvements"""
    
    analysis = call_result['analysis']
    
    print(f"\n📊 CALL ANALYSIS:")
    print(f"   😊 Farmer Sentiment: {analysis['sentiment'].title()}")
    print(f"   🎯 Interest Level: {analysis['interest_level'].title()}")
    print(f"   📞 Call Outcome: {analysis['call_outcome'].title()}")
    print(f"   ⚠️ Objections: {', '.join(analysis['objections'])}")
    print(f"   🎯 Effectiveness: {analysis['agent_effectiveness']:.1f}/1.0")
    
    # Generate improvements
    improvements = []
    
    if analysis['sentiment'] == 'negative':
        improvements.append("Use more empathetic language to build trust")
        improvements.append("Address skepticism directly with success stories")
    
    if 'trust_issues' in analysis['objections']:
        improvements.append("Provide government documentation references")
        improvements.append("Mention local success cases")
    
    if analysis['agent_effectiveness'] < 0.6:
        improvements.append("Simplify technical language")
        improvements.append("Focus on immediate benefits")
    
    return improvements

def generate_improved_prompt(original_prompt, improvements):
    """Generate improved agent prompt based on analysis"""
    
    print(f"\n🧠 LEARNING & IMPROVEMENT:")
    print(f"   📝 Identified {len(improvements)} areas for improvement:")
    
    for i, improvement in enumerate(improvements, 1):
        print(f"      {i}. {improvement}")
    
    # Generate improved prompt
    improved_intro = "Namaste ji, main [Agent Name] bol raha hun. Main aapko government ki official PM-KUSUM solar scheme ke baare mein batana chahta hun. Ye scheme already hazaaron farmers ne successfully use ki hai."
    
    improved_benefits = [
        "Government se 90% subsidy confirmed milegi",
        "Aapka bijli ka bill 80% tak kam ho jayega", 
        "Paani ki problem permanently solve ho jayegi",
        "Local office mein jakar verify kar sakte hain"
    ]
    
    improved_cta = "Kya aap chahenge ki main aapko nearest office ka address aur process detail mein explain karun?"
    
    print(f"\n✨ IMPROVED AGENT PROMPT:")
    print(f"   🎤 Intro: {improved_intro}")
    print(f"   💡 Benefits: {', '.join(improved_benefits[:2])}...")
    print(f"   📞 CTA: {improved_cta}")
    
    return {
        'intro': improved_intro,
        'benefits': improved_benefits,
        'call_to_action': improved_cta,
        'version': '1.1',
        'improvements_applied': improvements
    }

async def run_demo():
    """Run the complete demo"""
    
    print("🎯 VOICE AGENT REINFORCEMENT LEARNING SYSTEM - DEMO")
    print("=" * 60)
    print("🎬 This demo shows the complete learning cycle:")
    print("   1. Voice call simulation")
    print("   2. Call analysis & sentiment detection") 
    print("   3. Learning & prompt improvement")
    print("   4. System evolution")
    print("\n" + "=" * 60)
    
    # Create farmer profile
    farmer = create_mock_farmer_profile()
    
    print(f"\n🎭 FARMER PROFILE:")
    print(f"   👤 Name: {farmer['name']}")
    print(f"   📍 Location: {farmer['location']}")
    print(f"   🌾 Crops: {', '.join(farmer['crops'])}")
    print(f"   🤔 Skepticism Level: {farmer['skepticism']:.1f}/1.0")
    print(f"   📚 Education: {farmer['education'].title()}")
    
    print(f"\n{'='*40}")
    print("📞 VOICE CALL SIMULATION")
    print(f"{'='*40}")
    
    # Simulate the call
    call_result = await simulate_voice_call(farmer)
    
    # Analyze performance
    improvements = analyze_call_performance(call_result)
    
    # Generate improved prompt
    improved_prompt = generate_improved_prompt("original", improvements)
    
    # Show learning progress
    print(f"\n📈 LEARNING PROGRESS:")
    print(f"   🔄 Prompt Version: 1.0 → {improved_prompt['version']}")
    print(f"   📊 Improvements Applied: {len(improvements)}")
    print(f"   🎯 Expected Effectiveness Boost: +0.2")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    demo_result = {
        'timestamp': timestamp,
        'farmer_profile': farmer,
        'call_result': call_result,
        'improvements': improvements,
        'improved_prompt': improved_prompt
    }
    
    # Create output directory
    Path("demo_output").mkdir(exist_ok=True)
    
    with open(f"demo_output/demo_result_{timestamp}.json", 'w', encoding='utf-8') as f:
        json.dump(demo_result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("📁 Results saved to demo_output/")
    print("🔄 System learned and adapted based on farmer interaction")
    print("📈 Ready for next call with improved approach")
    
    print(f"\n🎯 DEMO SUMMARY:")
    print(f"   • Voice call simulated: ✅")
    print(f"   • Sentiment analysis: ✅") 
    print(f"   • Learning applied: ✅")
    print(f"   • Prompt improved: ✅")
    print(f"   • System evolved: ✅")
    
    return demo_result

def main():
    """Main demo function"""
    
    try:
        # Run the async demo
        result = asyncio.run(run_demo())
        
        print(f"\n🎉 Voice Agent Demo completed successfully!")
        print(f"💡 This demonstrates how the system learns from each interaction")
        print(f"🔗 For full functionality with real voice APIs, add API keys to .env")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)