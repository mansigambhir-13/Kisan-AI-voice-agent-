#!/usr/bin/env python3
"""
Voice Agent Reinforcement Learning System - Demo Version
A complete demonstration of the self-improving voice agent system for farmer outreach
"""

import asyncio
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import os

# ============================================================================
# DATA MODELS
# ============================================================================

class SentimentType(Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class InterestLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    CONFUSED = "confused"

class CallOutcome(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    FOLLOW_UP = "follow_up"

@dataclass
class FarmerProfile:
    name: str
    age: int
    education: str  # low, medium, high
    income: str     # low, medium, high
    location: str
    crops: List[str]
    land_size: str
    skepticism: float  # 0.0 to 1.0
    govt_experience: str
    family_size: int

@dataclass
class CallTranscript:
    speaker: str  # "agent" or "farmer"
    text: str
    timestamp: float
    sentiment: Optional[str] = None

@dataclass
class CallAnalysis:
    sentiment: SentimentType
    interest_level: InterestLevel
    intro_clarity: bool
    objections: List[str]
    call_outcome: CallOutcome
    key_insights: List[str]
    improvement_suggestions: List[str]
    confidence_score: float

@dataclass
class VoiceAgentPrompt:
    content: str
    version: str
    performance_metrics: Dict[str, float]
    last_updated: datetime

@dataclass
class CallSession:
    session_id: str
    farmer: FarmerProfile
    agent_prompt: VoiceAgentPrompt
    transcript: List[CallTranscript]
    analysis: Optional[CallAnalysis] = None
    audio_file_path: Optional[str] = None

# ============================================================================
# VOICE AGENT COMPONENT
# ============================================================================

class VoiceAgent:
    """Simulates a voice agent that makes calls to farmers"""
    
    def __init__(self, prompt: VoiceAgentPrompt):
        self.prompt = prompt
        self.call_count = 0
    
    async def make_call(self, farmer: FarmerProfile) -> CallSession:
        """Simulate making a voice call to a farmer"""
        self.call_count += 1
        session_id = f"call_{self.call_count}_{farmer.name}_{int(time.time())}"
        
        print(f"\n🎯 Making call to {farmer.name} ({farmer.age} years old)")
        print(f"📍 Location: {farmer.location}")
        print(f"🌾 Crops: {', '.join(farmer.crops)}")
        print(f"💰 Income level: {farmer.income}")
        print(f"🎓 Education: {farmer.education}")
        print(f"🤔 Skepticism level: {farmer.skepticism:.2f}")
        
        # Simulate the conversation
        transcript = await self._simulate_conversation(farmer)
        
        session = CallSession(
            session_id=session_id,
            farmer=farmer,
            agent_prompt=self.prompt,
            transcript=transcript
        )
        
        return session
    
    async def _simulate_conversation(self, farmer: FarmerProfile) -> List[CallTranscript]:
        """Simulate a realistic conversation between agent and farmer"""
        transcript = []
        current_time = 0.0
        
        # Agent introduction
        intro_text = self._generate_intro(farmer)
        transcript.append(CallTranscript(
            speaker="agent",
            text=intro_text,
            timestamp=current_time
        ))
        current_time += 2.0
        
        # Farmer's initial response (based on skepticism)
        farmer_response = self._generate_farmer_response(farmer, "intro")
        transcript.append(CallTranscript(
            speaker="farmer",
            text=farmer_response,
            timestamp=current_time
        ))
        current_time += 1.5
        
        # Agent explains benefits
        benefits_text = self._generate_benefits_explanation(farmer)
        transcript.append(CallTranscript(
            speaker="agent",
            text=benefits_text,
            timestamp=current_time
        ))
        current_time += 3.0
        
        # Farmer's reaction to benefits
        farmer_reaction = self._generate_farmer_response(farmer, "benefits")
        transcript.append(CallTranscript(
            speaker="farmer",
            text=farmer_reaction,
            timestamp=current_time
        ))
        current_time += 1.0
        
        # Agent addresses objections or asks for interest
        if farmer.skepticism > 0.6:
            objection_response = self._generate_objection_handling(farmer)
            transcript.append(CallTranscript(
                speaker="agent",
                text=objection_response,
                timestamp=current_time
            ))
            current_time += 2.5
            
            # Farmer's final response
            final_response = self._generate_farmer_response(farmer, "objection")
            transcript.append(CallTranscript(
                speaker="farmer",
                text=final_response,
                timestamp=current_time
            ))
        else:
            # Direct call to action
            cta_text = self._generate_call_to_action(farmer)
            transcript.append(CallTranscript(
                speaker="agent",
                text=cta_text,
                timestamp=current_time
            ))
            current_time += 2.0
            
            # Farmer's final response
            final_response = self._generate_farmer_response(farmer, "cta")
            transcript.append(CallTranscript(
                speaker="farmer",
                text=final_response,
                timestamp=current_time
            ))
        
        return transcript
    
    def _generate_intro(self, farmer: FarmerProfile) -> str:
        """Generate personalized introduction"""
        templates = [
            f"Namaste {farmer.name} ji, main PM-KUSUM Yojana ke baare mein aapko batane ke liye call kar raha hoon. Kya aap 5 minute de sakte hain?",
            f"Hello {farmer.name} ji, main government solar scheme ke baare mein aapko information dena chahta hoon. Kya aap interested hain?",
            f"Namaste {farmer.name} ji, main aapko solar pump scheme ke baare mein batana chahta hoon. Ye aapke liye bahut beneficial ho sakta hai."
        ]
        return random.choice(templates)
    
    def _generate_benefits_explanation(self, farmer: FarmerProfile) -> str:
        """Generate benefits explanation based on farmer profile"""
        if farmer.income == "low":
            return "Is scheme mein aapko 90% subsidy milega. Aap sirf 10% pay karenge aur solar pump free mein milega. Electricity bill bhi 90% kam ho jayega."
        elif farmer.income == "medium":
            return "Is scheme mein aapko 60% subsidy milega. Solar pump installation ke baad aapki electricity cost 80% tak kam ho jayegi. Plus maintenance cost bhi bahut kam hai."
        else:
            return "Is scheme mein aapko 50% subsidy milega. Solar pump se aap apne farm ko modernize kar sakte hain aur long term mein bahut save kar sakte hain."
    
    def _generate_objection_handling(self, farmer: FarmerProfile) -> str:
        """Handle common objections"""
        objections = [
            "Aapko lagta hai ki ye scheme fake hai? Main aapko government website ka link de sakta hoon. Ye 100% authentic scheme hai.",
            "Aapko lagta hai ki process complicated hai? Main aapko step by step guide karunga. Sirf 2-3 documents chahiye.",
            "Aapko lagta hai ki ye time waste hai? Sirf 10 minute ka call hai. Agar aap interested nahi hain to main aapko disturb nahi karunga."
        ]
        return random.choice(objections)
    
    def _generate_call_to_action(self, farmer: FarmerProfile) -> str:
        """Generate call to action"""
        return "To kya aap is scheme ke baare mein aur details chahte hain? Main aapko application process bhi bata sakta hoon."
    
    def _generate_farmer_response(self, farmer: FarmerProfile, context: str) -> str:
        """Generate realistic farmer responses based on profile"""
        skepticism = farmer.skepticism
        education = farmer.education
        
        if context == "intro":
            if skepticism > 0.7:
                return "Haan bolo, lekin jaldi bolo. Main busy hoon."
            elif skepticism > 0.4:
                return "Haan theek hai, batao kya hai."
            else:
                return "Haan ji, zaroor bataiye. Main interested hoon."
        
        elif context == "benefits":
            if skepticism > 0.6:
                return "Sab log yahi bolte hain. Koi real benefit nahi hai."
            elif skepticism > 0.3:
                return "Acha lag raha hai, lekin main sochunga."
            else:
                return "Bahut acha lag raha hai. Main interested hoon."
        
        elif context == "objection":
            if skepticism > 0.5:
                return "Theek hai, main dekh leta hoon. Abhi kuch nahi."
            else:
                return "Acha, to main try kar sakta hoon. Process kya hai?"
        
        else:  # cta
            if skepticism > 0.6:
                return "Nahi ji, abhi nahi. Baad mein dekhte hain."
            elif skepticism > 0.3:
                return "Haan, details bataiye. Main interested hoon."
            else:
                return "Bilkul ji, main apply karna chahta hoon. Process batayein."

# ============================================================================
# CALL ANALYSIS COMPONENT
# ============================================================================

class CallAnalyzer:
    """Analyzes call transcripts to extract insights"""
    
    def __init__(self):
        self.positive_keywords = ["acha", "good", "interested", "apply", "details", "subsidy", "benefit"]
        self.negative_keywords = ["nahi", "no", "fake", "waste", "busy", "complicated", "expensive"]
        self.confusion_keywords = ["samajh nahi aaya", "confused", "complicated", "kaise", "kya"]
    
    async def analyze_call(self, session: CallSession) -> CallAnalysis:
        """Analyze the call transcript and extract insights"""
        transcript = session.transcript
        farmer = session.farmer
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(transcript)
        
        # Analyze interest level
        interest_level = self._analyze_interest_level(transcript, farmer)
        
        # Check intro clarity
        intro_clarity = self._check_intro_clarity(transcript)
        
        # Extract objections
        objections = self._extract_objections(transcript)
        
        # Determine call outcome
        call_outcome = self._determine_call_outcome(sentiment, interest_level, objections)
        
        # Generate key insights
        key_insights = self._generate_key_insights(transcript, farmer, sentiment, interest_level)
        
        # Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(
            transcript, farmer, sentiment, interest_level, objections
        )
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(transcript)
        
        return CallAnalysis(
            sentiment=sentiment,
            interest_level=interest_level,
            intro_clarity=intro_clarity,
            objections=objections,
            call_outcome=call_outcome,
            key_insights=key_insights,
            improvement_suggestions=improvement_suggestions,
            confidence_score=confidence_score
        )
    
    def _analyze_sentiment(self, transcript: List[CallTranscript]) -> SentimentType:
        """Analyze overall sentiment of the conversation"""
        farmer_text = " ".join([t.text.lower() for t in transcript if t.speaker == "farmer"])
        
        positive_count = sum(1 for keyword in self.positive_keywords if keyword in farmer_text)
        negative_count = sum(1 for keyword in self.negative_keywords if keyword in farmer_text)
        
        if positive_count > negative_count:
            return SentimentType.POSITIVE
        elif negative_count > positive_count:
            return SentimentType.NEGATIVE
        else:
            return SentimentType.NEUTRAL
    
    def _analyze_interest_level(self, transcript: List[CallTranscript], farmer: FarmerProfile) -> InterestLevel:
        """Analyze farmer's interest level"""
        farmer_text = " ".join([t.text.lower() for t in transcript if t.speaker == "farmer"])
        
        # Check for confusion
        if any(keyword in farmer_text for keyword in self.confusion_keywords):
            return InterestLevel.CONFUSED
        
        # Check for high interest
        high_interest_indicators = ["interested", "apply", "details", "process", "subsidy"]
        if any(indicator in farmer_text for indicator in high_interest_indicators):
            return InterestLevel.HIGH
        
        # Check for low interest
        low_interest_indicators = ["nahi", "no", "busy", "waste", "fake"]
        if any(indicator in farmer_text for indicator in low_interest_indicators):
            return InterestLevel.LOW
        
        return InterestLevel.MEDIUM
    
    def _check_intro_clarity(self, transcript: List[CallTranscript]) -> bool:
        """Check if the introduction was clear and engaging"""
        if not transcript:
            return False
        
        intro_text = transcript[0].text.lower()
        clarity_indicators = ["namaste", "hello", "pm-kusum", "solar", "scheme"]
        return any(indicator in intro_text for indicator in clarity_indicators)
    
    def _extract_objections(self, transcript: List[CallTranscript]) -> List[str]:
        """Extract objections from farmer responses"""
        objections = []
        farmer_texts = [t.text.lower() for t in transcript if t.speaker == "farmer"]
        
        objection_patterns = [
            "fake", "waste", "complicated", "expensive", "busy", "nahi", "no",
            "samajh nahi", "confused", "time waste", "difficult"
        ]
        
        for text in farmer_texts:
            for pattern in objection_patterns:
                if pattern in text:
                    objections.append(pattern)
        
        return list(set(objections))
    
    def _determine_call_outcome(self, sentiment: SentimentType, interest: InterestLevel, objections: List[str]) -> CallOutcome:
        """Determine the overall call outcome"""
        if sentiment == SentimentType.POSITIVE and interest in [InterestLevel.HIGH, InterestLevel.MEDIUM]:
            return CallOutcome.SUCCESS
        elif sentiment == SentimentType.NEGATIVE or interest == InterestLevel.LOW:
            return CallOutcome.FAILURE
        else:
            return CallOutcome.FOLLOW_UP
    
    def _generate_key_insights(self, transcript: List[CallTranscript], farmer: FarmerProfile, 
                              sentiment: SentimentType, interest: InterestLevel) -> List[str]:
        """Generate key insights from the call"""
        insights = []
        
        if sentiment == SentimentType.POSITIVE:
            insights.append("Farmer showed positive sentiment towards the scheme")
        
        if interest == InterestLevel.HIGH:
            insights.append("Farmer expressed high interest in applying")
        elif interest == InterestLevel.CONFUSED:
            insights.append("Farmer seemed confused about the process")
        
        if farmer.skepticism > 0.6:
            insights.append("High skepticism level - needs more trust-building")
        
        if farmer.education == "low":
            insights.append("Low education level - needs simpler explanations")
        
        return insights
    
    def _generate_improvement_suggestions(self, transcript: List[CallTranscript], farmer: FarmerProfile,
                                        sentiment: SentimentType, interest: InterestLevel, objections: List[str]) -> List[str]:
        """Generate suggestions for improving future calls"""
        suggestions = []
        
        if sentiment == SentimentType.NEGATIVE:
            suggestions.append("Improve trust-building in introduction")
        
        if interest == InterestLevel.CONFUSED:
            suggestions.append("Simplify explanation of benefits")
            suggestions.append("Add more concrete examples")
        
        if "fake" in objections:
            suggestions.append("Add government verification details")
        
        if "complicated" in objections:
            suggestions.append("Simplify application process explanation")
        
        if farmer.skepticism > 0.6:
            suggestions.append("Address skepticism more directly")
        
        return suggestions
    
    def _calculate_confidence_score(self, transcript: List[CallTranscript]) -> float:
        """Calculate confidence score for the analysis"""
        # Simple heuristic based on transcript length and content
        farmer_turns = len([t for t in transcript if t.speaker == "farmer"])
        total_length = sum(len(t.text) for t in transcript)
        
        # More interaction = higher confidence
        confidence = min(0.9, 0.3 + (farmer_turns * 0.1) + (total_length / 1000))
        return round(confidence, 2)

# ============================================================================
# REINFORCEMENT LEARNING ENGINE
# ============================================================================

class ReinforcementEngine:
    """Improves the voice agent based on call analysis"""
    
    def __init__(self):
        self.performance_history = []
        self.prompt_versions = []
    
    async def improve_agent(self, session: CallSession, analysis: CallAnalysis) -> VoiceAgentPrompt:
        """Improve the agent prompt based on call analysis"""
        # Store performance data
        performance_data = {
            "session_id": session.session_id,
            "sentiment": analysis.sentiment.value,
            "interest_level": analysis.interest_level.value,
            "call_outcome": analysis.call_outcome.value,
            "confidence_score": analysis.confidence_score,
            "timestamp": datetime.now()
        }
        self.performance_history.append(performance_data)
        
        # Generate improved prompt
        improved_prompt = self._generate_improved_prompt(session.agent_prompt, analysis)
        
        # Store prompt version
        self.prompt_versions.append({
            "version": improved_prompt.version,
            "performance": performance_data,
            "improvements": analysis.improvement_suggestions
        })
        
        return improved_prompt
    
    def _generate_improved_prompt(self, current_prompt: VoiceAgentPrompt, analysis: CallAnalysis) -> VoiceAgentPrompt:
        """Generate an improved prompt based on analysis"""
        improvements = analysis.improvement_suggestions
        
        # Base prompt template
        base_prompt = """You are a helpful voice agent calling farmers about the PM-KUSUM solar scheme. 
Your goal is to explain the benefits and encourage farmers to apply.

Key points to cover:
1. Introduce yourself and the scheme
2. Explain the subsidy benefits (50-90% depending on income)
3. Address common concerns about government schemes
4. Provide clear next steps for application

Be respectful, patient, and address farmer concerns directly."""

        # Add specific improvements based on analysis
        if "Improve trust-building in introduction" in improvements:
            base_prompt += "\n\nIMPROVEMENT: Start with government verification details to build trust."
        
        if "Simplify explanation of benefits" in improvements:
            base_prompt += "\n\nIMPROVEMENT: Use simple, concrete examples when explaining benefits."
        
        if "Address skepticism more directly" in improvements:
            base_prompt += "\n\nIMPROVEMENT: Acknowledge skepticism upfront and provide proof points."
        
        if "Add government verification details" in improvements:
            base_prompt += "\n\nIMPROVEMENT: Mention official government website and verification process."
        
        # Create new version
        new_version = f"v{len(self.prompt_versions) + 1}.{len(improvements)}"
        
        # Calculate performance metrics
        recent_performance = self._calculate_recent_performance()
        
        return VoiceAgentPrompt(
            content=base_prompt,
            version=new_version,
            performance_metrics=recent_performance,
            last_updated=datetime.now()
        )
    
    def _calculate_recent_performance(self) -> Dict[str, float]:
        """Calculate recent performance metrics"""
        if not self.performance_history:
            return {"success_rate": 0.0, "avg_confidence": 0.0}
        
        recent_calls = self.performance_history[-10:]  # Last 10 calls
        
        success_count = sum(1 for call in recent_calls if call["call_outcome"] == "success")
        success_rate = success_count / len(recent_calls)
        
        avg_confidence = sum(call["confidence_score"] for call in recent_calls) / len(recent_calls)
        
        return {
            "success_rate": round(success_rate, 3),
            "avg_confidence": round(avg_confidence, 3)
        }

# ============================================================================
# MAIN SYSTEM
# ============================================================================

class VoiceAgentSystem:
    """Main system that orchestrates the voice agent, analysis, and improvement"""
    
    def __init__(self):
        self.voice_agent = None
        self.analyzer = CallAnalyzer()
        self.reinforcement_engine = ReinforcementEngine()
        self.sessions = []
        
        # Initialize with base prompt
        base_prompt = VoiceAgentPrompt(
            content="""You are a helpful voice agent calling farmers about the PM-KUSUM solar scheme. 
Your goal is to explain the benefits and encourage farmers to apply.

Key points to cover:
1. Introduce yourself and the scheme
2. Explain the subsidy benefits (50-90% depending on income)
3. Address common concerns about government schemes
4. Provide clear next steps for application

Be respectful, patient, and address farmer concerns directly.""",
            version="v1.0",
            performance_metrics={"success_rate": 0.0, "avg_confidence": 0.0},
            last_updated=datetime.now()
        )
        
        self.voice_agent = VoiceAgent(base_prompt)
    
    async def run_learning_cycle(self, num_calls: int = 5):
        """Run multiple calls to demonstrate learning and improvement"""
        print("🚀 Starting Voice Agent Reinforcement Learning System")
        print("=" * 60)
        
        for i in range(num_calls):
            print(f"\n📞 CYCLE {i+1}/{num_calls}")
            print("-" * 40)
            
            # Generate a farmer profile
            farmer = self._generate_farmer_profile()
            
            # Make the call
            session = await self.voice_agent.make_call(farmer)
            
            # Analyze the call
            analysis = await self.analyzer.analyze_call(session)
            session.analysis = analysis
            
            # Display results
            self._display_call_results(session, analysis)
            
            # Improve the agent
            improved_prompt = await self.reinforcement_engine.improve_agent(session, analysis)
            self.voice_agent.prompt = improved_prompt
            
            # Store session
            self.sessions.append(session)
            
            # Show improvement
            if i > 0:
                self._show_improvement_progress()
            
            print("\n" + "=" * 60)
        
        # Final summary
        self._display_final_summary()
    
    def _generate_farmer_profile(self) -> FarmerProfile:
        """Generate a realistic farmer profile"""
        names = ["Ram Singh", "Lakshmi Devi", "Mohan Kumar", "Sita Ram", "Ramesh Patel"]
        locations = ["Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", "Rajasthan"]
        crops = [["wheat", "rice"], ["cotton", "sugarcane"], ["pulses", "vegetables"], ["maize", "wheat"], ["bajra", "jowar"]]
        
        return FarmerProfile(
            name=random.choice(names),
            age=random.randint(35, 65),
            education=random.choice(["low", "medium", "high"]),
            income=random.choice(["low", "medium", "high"]),
            location=random.choice(locations),
            crops=random.choice(crops),
            land_size=f"{random.randint(2, 20)} acres",
            skepticism=random.uniform(0.2, 0.8),
            govt_experience="Mixed experience with government schemes",
            family_size=random.randint(4, 8)
        )
    
    def _display_call_results(self, session: CallSession, analysis: CallAnalysis):
        """Display call results in a formatted way"""
        print(f"\n📊 CALL ANALYSIS RESULTS:")
        print(f"   Sentiment: {analysis.sentiment.value.upper()}")
        print(f"   Interest Level: {analysis.interest_level.value.upper()}")
        print(f"   Call Outcome: {analysis.call_outcome.value.upper()}")
        print(f"   Confidence Score: {analysis.confidence_score}")
        print(f"   Intro Clarity: {'✅' if analysis.intro_clarity else '❌'}")
        
        if analysis.objections:
            print(f"   Objections: {', '.join(analysis.objections)}")
        
        print(f"\n💡 KEY INSIGHTS:")
        for insight in analysis.key_insights:
            print(f"   • {insight}")
        
        print(f"\n🔧 IMPROVEMENT SUGGESTIONS:")
        for suggestion in analysis.improvement_suggestions:
            print(f"   • {suggestion}")
    
    def _show_improvement_progress(self):
        """Show improvement progress"""
        if len(self.reinforcement_engine.performance_history) >= 2:
            current = self.reinforcement_engine.performance_history[-1]
            previous = self.reinforcement_engine.performance_history[-2]
            
            print(f"\n📈 IMPROVEMENT PROGRESS:")
            print(f"   Success Rate: {previous['call_outcome']} → {current['call_outcome']}")
            print(f"   Confidence: {previous['confidence_score']:.2f} → {current['confidence_score']:.2f}")
    
    def _display_final_summary(self):
        """Display final system summary"""
        print(f"\n🎯 FINAL SYSTEM SUMMARY")
        print("=" * 60)
        
        total_calls = len(self.sessions)
        successful_calls = sum(1 for s in self.sessions if s.analysis.call_outcome == CallOutcome.SUCCESS)
        success_rate = (successful_calls / total_calls) * 100
        
        print(f"📞 Total Calls Made: {total_calls}")
        print(f"✅ Successful Calls: {successful_calls}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        print(f"🔄 Prompt Versions: {len(self.reinforcement_engine.prompt_versions)}")
        
        print(f"\n📈 PERFORMANCE METRICS:")
        for metric, value in self.voice_agent.prompt.performance_metrics.items():
            print(f"   {metric}: {value}")
        
        print(f"\n🔧 KEY IMPROVEMENTS MADE:")
        all_improvements = set()
        for session in self.sessions:
            if session.analysis:
                all_improvements.update(session.analysis.improvement_suggestions)
        
        for improvement in all_improvements:
            print(f"   • {improvement}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Main function to run the voice agent system"""
    system = VoiceAgentSystem()
    await system.run_learning_cycle(num_calls=5)

if __name__ == "__main__":
    asyncio.run(main())