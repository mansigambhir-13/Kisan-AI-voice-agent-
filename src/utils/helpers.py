import asyncio
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import re

def generate_call_id() -> str:
    """Generate unique call ID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"CALL_{timestamp}_{unique_id}"

def generate_audio_filename(call_id: str, speaker: str, turn: int, extension: str = "mp3") -> str:
    """Generate audio filename"""
    return f"{call_id}_{speaker}_turn{turn:02d}.{extension}"

def clean_hindi_text(text: str) -> str:
    """Clean and normalize Hindi text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters but keep Hindi characters and basic punctuation
    text = re.sub(r'[^\u0900-\u097F\w\s.,!?-]', '', text)
    
    return text

def extract_keywords(text: str, language: str = "hindi") -> List[str]:
    """Extract keywords from text"""
    # Define keyword patterns for Hindi
    hindi_keywords = {
        'positive': ['haan', 'achha', 'theek', 'zaroor', 'batayiye', 'details', 'chahiye', 'interested'],
        'negative': ['nahi', 'mat', 'band', 'pareshan', 'time nahi', 'dhokha', 'problem'],
        'neutral': ['dekhunga', 'sochenge', 'pata nahi', 'maybe', 'shayad'],
        'confused': ['samajh nahi', 'kya bol rahe', 'ye kya', 'kaise', 'simple mein'],
        'objections': ['kitne ka', 'free mein', 'paisa', 'eligible', 'documents', 'process']
    }
    
    found_keywords = {}
    text_lower = text.lower()
    
    for category, keywords in hindi_keywords.items():
        found_keywords[category] = [kw for kw in keywords if kw in text_lower]
    
    return found_keywords

def calculate_effectiveness_score(sentiment: str, interest: str, objections: List[str], 
                                outcome: str, intro_clarity: bool) -> float:
    """Calculate effectiveness score based on conversation analysis"""
    score = 0.0
    
    # Sentiment scoring (30%)
    sentiment_scores = {'positive': 0.3, 'neutral': 0.15, 'negative': 0.0}
    score += sentiment_scores.get(sentiment, 0.0)
    
    # Interest scoring (30%)
    interest_scores = {'high': 0.3, 'medium': 0.2, 'low': 0.1, 'confused': 0.05}
    score += interest_scores.get(interest, 0.0)
    
    # Clarity bonus (10%)
    if intro_clarity:
        score += 0.1
    
    # Objection penalty (10%)
    objection_penalty = min(0.1, len(objections) * 0.02)
    score -= objection_penalty
    
    # Outcome scoring (20%)
    outcome_scores = {'success': 0.2, 'follow_up': 0.1, 'failure': 0.0}
    score += outcome_scores.get(outcome, 0.0)
    
    return max(0.0, min(1.0, score))

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

def save_json_data(data: Any, filepath: Union[str, Path], ensure_ascii: bool = False) -> bool:
    """Save data to JSON file"""
    try:
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=ensure_ascii, indent=2, default=str)
        
        return True
    except Exception as e:
        print(f"Error saving JSON to {filepath}: {e}")
        return False

def load_json_data(filepath: Union[str, Path]) -> Optional[Any]:
    """Load data from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON from {filepath}: {e}")
        return None

def create_output_directories(base_path: str = "data/output") -> Dict[str, Path]:
    """Create output directories and return paths"""
    base = Path(base_path)
    
    directories = {
        'call_logs': base / 'call_logs',
        'audio_files': base / 'audio_files', 
        'reports': base / 'reports',
        'temp': Path('data/temp')
    }
    
    for name, path in directories.items():
        path.mkdir(parents=True, exist_ok=True)
    
    return directories

async def run_with_timeout(coro, timeout_seconds: float):
    """Run coroutine with timeout"""
    try:
        return await asyncio.wait_for(coro, timeout=timeout_seconds)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Operation timed out after {timeout_seconds} seconds")

def validate_farmer_profile(profile: Dict[str, Any]) -> List[str]:
    """Validate farmer profile data"""
    errors = []
    required_fields = ['name', 'age', 'education', 'income', 'location', 'crops', 
                      'land_size', 'skepticism', 'govt_experience', 'family_size']
    
    for field in required_fields:
        if field not in profile:
            errors.append(f"Missing required field: {field}")
    
    # Validate data types and ranges
    if 'age' in profile and (not isinstance(profile['age'], int) or profile['age'] < 18 or profile['age'] > 100):
        errors.append("Age must be an integer between 18 and 100")
    
    if 'skepticism' in profile and (not isinstance(profile['skepticism'], (int, float)) or 
                                   profile['skepticism'] < 0 or profile['skepticism'] > 1):
        errors.append("Skepticism must be a number between 0 and 1")
    
    if 'education' in profile and profile['education'] not in ['low', 'medium', 'high']:
        errors.append("Education must be 'low', 'medium', or 'high'")
    
    if 'income' in profile and profile['income'] not in ['low', 'medium', 'high']:
        errors.append("Income must be 'low', 'medium', or 'high'")
    
    return errors

class PerformanceTracker:
    """Track system performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'api_calls': {'deepgram': 0, 'elevenlabs': 0, 'openai': 0},
            'api_errors': {'deepgram': 0, 'elevenlabs': 0, 'openai': 0},
            'call_durations': [],
            'effectiveness_scores': [],
            'start_time': datetime.now()
        }
    
    def record_api_call(self, service: str, success: bool = True):
        """Record API call"""
        if service in self.metrics['api_calls']:
            self.metrics['api_calls'][service] += 1
            if not success:
                self.metrics['api_errors'][service] += 1
    
    def record_call_duration(self, duration: float):
        """Record call duration"""
        self.metrics['call_durations'].append(duration)
    
    def record_effectiveness(self, score: float):
        """Record effectiveness score"""
        self.metrics['effectiveness_scores'].append(score)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        runtime = datetime.now() - self.metrics['start_time']
        
        return {
            'runtime': str(runtime),
            'total_api_calls': sum(self.metrics['api_calls'].values()),
            'api_success_rate': self._calculate_success_rate(),
            'average_call_duration': sum(self.metrics['call_durations']) / len(self.metrics['call_durations']) if self.metrics['call_durations'] else 0,
            'average_effectiveness': sum(self.metrics['effectiveness_scores']) / len(self.metrics['effectiveness_scores']) if self.metrics['effectiveness_scores'] else 0,
            'total_calls': len(self.metrics['call_durations'])
        }
    
    def _calculate_success_rate(self) -> float:
        """Calculate API success rate"""
        total_calls = sum(self.metrics['api_calls'].values())
        total_errors = sum(self.metrics['api_errors'].values())
        
        if total_calls == 0:
            return 1.0
        
        return (total_calls - total_errors) / total_calls