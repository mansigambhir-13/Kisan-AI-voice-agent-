from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class SentimentType(Enum):
    """Farmer sentiment types"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class InterestLevel(Enum):
    """Farmer interest levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    CONFUSED = "confused"

class CallOutcome(Enum):
    """Call outcome types"""
    SUCCESS = "success"
    FAILURE = "failure"
    FOLLOW_UP = "follow_up"

class EducationLevel(Enum):
    """Education levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class IncomeLevel(Enum):
    """Income levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class VoiceSettings:
    """ElevenLabs voice configuration"""
    stability: float = 0.5
    similarity_boost: float = 0.5
    style: float = 0.3
    use_speaker_boost: bool = True

@dataclass
class APIConfig:
    """API configuration settings"""
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 500
    deepgram_model: str = "nova-2"
    deepgram_language: str = "hi"
    elevenlabs_voice_id: str = "pNInz6obpgDQGcFmaJgB"
    voice_settings: VoiceSettings = field(default_factory=VoiceSettings)

@dataclass
class FarmerProfile:
    """Farmer profile data model"""
    id: str
    name: str
    age: int
    education: EducationLevel
    income: IncomeLevel
    location: str
    crops: List[str]
    land_size: str
    skepticism: float  # 0.0 to 1.0
    govt_experience: str
    family_size: int
    phone: Optional[str] = None
    preferred_language: str = "hindi"
    best_call_time: str = "morning"
    persona_type: Optional[str] = None

@dataclass
class AgentPrompt:
    """Voice agent prompt configuration"""
    intro: str
    benefits: List[str]
    call_to_action: str
    version: int
    improvements: List[str] = field(default_factory=list)
    tone_instructions: str = "Speak politely and clearly, use simple Hindi"
    conversation_style: str = "Friendly but professional"
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class ConversationTurn:
    """Single conversation turn"""
    turn_number: int
    agent_message: str
    farmer_response: str
    timestamp: datetime = field(default_factory=datetime.now)
    audio_files: Dict[str, str] = field(default_factory=dict)  # agent/farmer audio paths

@dataclass
class CallAnalysis:
    """Call analysis results"""
    sentiment: SentimentType
    interest_level: InterestLevel
    intro_clarity: bool
    objections: List[str]
    call_outcome: CallOutcome
    farmer_responses: List[str]
    agent_effectiveness: float  # 0.0 to 1.0
    conversation_flow: Dict[str, Any] = field(default_factory=dict)
    emotional_indicators: List[str] = field(default_factory=list)
    analysis_timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class CallRecord:
    """Complete call record"""
    call_id: str
    iteration: int
    farmer_profile: FarmerProfile
    agent_version: int
    conversation_turns: List[ConversationTurn]
    analysis: CallAnalysis
    call_start: datetime
    call_end: Optional[datetime] = None
    total_duration: Optional[float] = None  # seconds
    audio_files: List[str] = field(default_factory=list)

@dataclass
class LearningInsight:
    """Learning insight from analysis"""
    issue_type: str  # trust, cost, clarity, etc.
    severity: float  # 0.0 to 1.0
    suggested_improvement: str
    confidence: float  # 0.0 to 1.0
    evidence: List[str] = field(default_factory=list)

@dataclass
class SystemMetrics:
    """System performance metrics"""
    total_calls: int
    success_rate: float
    average_effectiveness: float
    improvement_rate: float
    common_objections: Dict[str, int]
    learning_insights: List[LearningInsight]
    timestamp: datetime = field(default_factory=datetime.now)

# Pydantic models for API validation
class FarmerProfileAPI(BaseModel):
    """API model for farmer profile"""
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=18, le=100)
    education: str = Field(..., regex="^(low|medium|high)$")
    income: str = Field(..., regex="^(low|medium|high)$")
    location: str = Field(..., min_length=2, max_length=100)
    crops: List[str] = Field(..., min_items=1)
    land_size: str = Field(..., min_length=1)
    skepticism: float = Field(..., ge=0.0, le=1.0)
    govt_experience: str = Field(..., min_length=5)
    family_size: int = Field(..., ge=1, le=20)

class CallAnalysisAPI(BaseModel):
    """API model for call analysis"""
    sentiment: str = Field(..., regex="^(positive|neutral|negative)$")
    interest_level: str = Field(..., regex="^(high|medium|low|confused)$")
    intro_clarity: bool
    objections: List[str] = Field(default_factory=list)
    call_outcome: str = Field(..., regex="^(success|failure|follow_up)$")
    agent_effectiveness: float = Field(..., ge=0.0, le=1.0)
    emotional_indicators: List[str] = Field(default_factory=list)