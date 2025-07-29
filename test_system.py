#!/usr/bin/env python3
"""
Test script for Voice Agent Reinforcement Learning System
Demonstrates various scenarios and system capabilities
"""

import asyncio
import json
from demo_voice_system import (
    VoiceAgentSystem, FarmerProfile, CallAnalysis, 
    SentimentType, InterestLevel, CallOutcome
)

async def test_specific_scenarios():
    """Test specific farmer scenarios to demonstrate system capabilities"""
    
    print("🧪 Testing Voice Agent System - Specific Scenarios")
    print("=" * 60)
    
    # Create system
    system = VoiceAgentSystem()
    
    # Test Scenario 1: Highly Skeptical Farmer
    print("\n📞 SCENARIO 1: Highly Skeptical Farmer")
    print("-" * 40)
    
    skeptical_farmer = FarmerProfile(
        name="Ramesh Kumar",
        age=55,
        education="low",
        income="low",
        location="Uttar Pradesh",
        crops=["wheat", "pulses"],
        land_size="3 acres",
        skepticism=0.85,  # Very high skepticism
        govt_experience="Was cheated by previous government scheme",
        family_size=6
    )
    
    session1 = await system.voice_agent.make_call(skeptical_farmer)
    analysis1 = await system.analyzer.analyze_call(session1)
    
    print(f"Farmer: {skeptical_farmer.name} (Skepticism: {skeptical_farmer.skepticism:.2f})")
    print(f"Sentiment: {analysis1.sentiment.value}")
    print(f"Interest: {analysis1.interest_level.value}")
    print(f"Outcome: {analysis1.call_outcome.value}")
    print(f"Objections: {analysis1.objections}")
    print(f"Improvements: {analysis1.improvement_suggestions}")
    
    # Test Scenario 2: Highly Educated, Low Skepticism Farmer
    print("\n📞 SCENARIO 2: Educated, Interested Farmer")
    print("-" * 40)
    
    educated_farmer = FarmerProfile(
        name="Dr. Sunita Sharma",
        age=42,
        education="high",
        income="high",
        location="Punjab",
        crops=["cotton", "sugarcane"],
        land_size="15 acres",
        skepticism=0.15,  # Very low skepticism
        govt_experience="Multiple successful government schemes",
        family_size=4
    )
    
    session2 = await system.voice_agent.make_call(educated_farmer)
    analysis2 = await system.analyzer.analyze_call(session2)
    
    print(f"Farmer: {educated_farmer.name} (Education: {educated_farmer.education}, Skepticism: {educated_farmer.skepticism:.2f})")
    print(f"Sentiment: {analysis2.sentiment.value}")
    print(f"Interest: {analysis2.interest_level.value}")
    print(f"Outcome: {analysis2.call_outcome.value}")
    print(f"Objections: {analysis2.objections}")
    print(f"Improvements: {analysis2.improvement_suggestions}")
    
    # Test Scenario 3: Confused, Medium Education Farmer
    print("\n📞 SCENARIO 3: Confused, Medium Education Farmer")
    print("-" * 40)
    
    confused_farmer = FarmerProfile(
        name="Mohan Patel",
        age=48,
        education="medium",
        income="medium",
        location="Gujarat",
        crops=["groundnut", "sesame"],
        land_size="8 acres",
        skepticism=0.65,  # Medium-high skepticism
        govt_experience="Mixed experience with government schemes",
        family_size=5
    )
    
    session3 = await system.voice_agent.make_call(confused_farmer)
    analysis3 = await system.analyzer.analyze_call(session3)
    
    print(f"Farmer: {confused_farmer.name} (Education: {confused_farmer.education}, Skepticism: {confused_farmer.skepticism:.2f})")
    print(f"Sentiment: {analysis3.sentiment.value}")
    print(f"Interest: {analysis3.interest_level.value}")
    print(f"Outcome: {analysis3.call_outcome.value}")
    print(f"Objections: {analysis3.objections}")
    print(f"Improvements: {analysis3.improvement_suggestions}")
    
    return [session1, session2, session3], [analysis1, analysis2, analysis3]

async def test_learning_progression():
    """Test how the system learns and improves over multiple calls"""
    
    print("\n🔄 Testing Learning Progression")
    print("=" * 60)
    
    system = VoiceAgentSystem()
    
    # Run 3 learning cycles
    for i in range(3):
        print(f"\n📞 LEARNING CYCLE {i+1}/3")
        print("-" * 30)
        
        # Generate farmer
        farmer = system._generate_farmer_profile()
        
        # Make call
        session = await system.voice_agent.make_call(farmer)
        
        # Analyze
        analysis = await system.analyzer.analyze_call(session)
        session.analysis = analysis
        
        # Display results
        print(f"Farmer: {farmer.name} (Skepticism: {farmer.skepticism:.2f})")
        print(f"Agent Version: {system.voice_agent.prompt.version}")
        print(f"Sentiment: {analysis.sentiment.value}")
        print(f"Interest: {analysis.interest_level.value}")
        print(f"Outcome: {analysis.call_outcome.value}")
        
        # Improve agent
        improved_prompt = await system.reinforcement_engine.improve_agent(session, analysis)
        system.voice_agent.prompt = improved_prompt
        
        print(f"New Version: {improved_prompt.version}")
        print(f"Improvements: {analysis.improvement_suggestions}")
        
        system.sessions.append(session)
    
    # Show final performance
    print(f"\n📊 FINAL PERFORMANCE:")
    print(f"Total Calls: {len(system.sessions)}")
    successful_calls = sum(1 for s in system.sessions if s.analysis.call_outcome == CallOutcome.SUCCESS)
    print(f"Success Rate: {(successful_calls / len(system.sessions)) * 100:.1f}%")
    print(f"Final Agent Version: {system.voice_agent.prompt.version}")

async def test_analysis_capabilities():
    """Test the analysis capabilities with different conversation patterns"""
    
    print("\n🔍 Testing Analysis Capabilities")
    print("=" * 60)
    
    from demo_voice_system import CallAnalyzer, CallTranscript
    
    analyzer = CallAnalyzer()
    
    # Test Case 1: Positive conversation
    print("\n📝 Test Case 1: Positive Conversation")
    positive_transcript = [
        CallTranscript(speaker="agent", text="Namaste ji, main PM-KUSUM scheme ke baare mein batana chahta hun.", timestamp=0.0),
        CallTranscript(speaker="farmer", text="Haan ji, zaroor batayiye. Main interested hun.", timestamp=2.0),
        CallTranscript(speaker="agent", text="Is scheme mein aapko 90% subsidy milega.", timestamp=3.5),
        CallTranscript(speaker="farmer", text="Bahut acha lag raha hai. Main apply karna chahta hun.", timestamp=6.5)
    ]
    
    # Create a mock session for analysis
    mock_farmer = FarmerProfile(
        name="Test Farmer", age=45, education="medium", income="medium",
        location="Test", crops=["wheat"], land_size="5 acres",
        skepticism=0.3, govt_experience="Good", family_size=5
    )
    
    mock_session = type('MockSession', (), {
        'transcript': positive_transcript,
        'farmer': mock_farmer
    })()
    
    analysis = await analyzer.analyze_call(mock_session)
    print(f"Sentiment: {analysis.sentiment.value}")
    print(f"Interest: {analysis.interest_level.value}")
    print(f"Outcome: {analysis.call_outcome.value}")
    print(f"Confidence: {analysis.confidence_score}")
    
    # Test Case 2: Negative conversation
    print("\n📝 Test Case 2: Negative Conversation")
    negative_transcript = [
        CallTranscript(speaker="agent", text="Namaste ji, main PM-KUSUM scheme ke baare mein batana chahta hun.", timestamp=0.0),
        CallTranscript(speaker="farmer", text="Nahi ji, main busy hun. Ye sab fake hai.", timestamp=2.0),
        CallTranscript(speaker="agent", text="Ye government scheme hai, 100% authentic.", timestamp=3.5),
        CallTranscript(speaker="farmer", text="Sab log yahi bolte hain. Main interested nahi hun.", timestamp=6.5)
    ]
    
    mock_session.transcript = negative_transcript
    analysis = await analyzer.analyze_call(mock_session)
    print(f"Sentiment: {analysis.sentiment.value}")
    print(f"Interest: {analysis.interest_level.value}")
    print(f"Outcome: {analysis.call_outcome.value}")
    print(f"Confidence: {analysis.confidence_score}")
    print(f"Objections: {analysis.objections}")

async def main():
    """Run all tests"""
    print("🚀 Voice Agent System - Comprehensive Testing")
    print("=" * 60)
    
    # Test specific scenarios
    sessions, analyses = await test_specific_scenarios()
    
    # Test learning progression
    await test_learning_progression()
    
    # Test analysis capabilities
    await test_analysis_capabilities()
    
    print("\n✅ All tests completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())