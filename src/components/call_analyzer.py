import asyncio
import json
import re
from typing import Dict, List, Optional
import openai
import logging

from ..models.data_models import CallAnalysis, SentimentType, InterestLevel, CallOutcome
from ..utils.helpers import extract_keywords, calculate_effectiveness_score, PerformanceTracker

class CallAnalyzer:
    """Enhanced analyzer with LLM-based conversation analysis"""
    
    def __init__(self, openai_api_key: str, config: Dict):
        self.openai_api_key = openai_api_key
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.performance_tracker = PerformanceTracker()
        
        if openai_api_key:
            openai.api_key = openai_api_key
        else:
            self.logger.warning("OpenAI API key not provided - using rule-based analysis")
        
        # Hindi keywords for rule-based analysis
        self.hindi_keywords = {
            'positive': ['haan', 'achha', 'theek', 'zaroor', 'batayiye', 'details', 'chahiye', 'interested'],
            'negative': ['nahi', 'mat', 'band', 'pareshan', 'time nahi', 'dhokha', 'problem'],
            'neutral': ['dekhunga', 'sochenge', 'pata nahi', 'maybe', 'shayad'],
            'confused': ['samajh nahi', 'kya bol rahe', 'ye kya', 'kaise', 'simple mein'],
            'interested': ['details', 'batao', 'kaise milega', 'process kya', 'zaroor', 'interested'],
            'objections': ['kitne ka', 'free mein', 'paisa', 'eligible', 'documents', 'process']
        }
    
    async def analyze_conversation(self, agent_messages: List[str], 
                                 farmer_responses: List[str]) -> CallAnalysis:
        """Analyze conversation using LLM and rule-based methods"""
        
        # Combine conversation for analysis
        conversation_text = self._format_conversation(agent_messages, farmer_responses)
        
        if self.openai_api_key:
            # Get LLM analysis
            try:
                llm_analysis = await self._get_llm_analysis(conversation_text)
                # Combine with rule-based analysis for validation
                rule_analysis = self._rule_based_analysis(farmer_responses)
                
                # Merge analyses (prefer LLM but validate with rules)
                final_analysis = self._merge_analyses(llm_analysis, rule_analysis)
            except Exception as e:
                self.logger.error(f"LLM analysis failed: {e}, falling back to rule-based")
                final_analysis = self._rule_based_analysis(farmer_responses)
        else:
            # Use only rule-based analysis
            final_analysis = self._rule_based_analysis(farmer_responses)
        
        # Calculate effectiveness score
        effectiveness = calculate_effectiveness_score(
            final_analysis['sentiment'],
            final_analysis['interest_level'],
            final_analysis['objections'],
            final_analysis['call_outcome'],
            final_analysis['intro_clarity']
        )
        
        return CallAnalysis(
            sentiment=SentimentType(final_analysis['sentiment']),
            interest_level=InterestLevel(final_analysis['interest_level']),
            intro_clarity=final_analysis['intro_clarity'],
            objections=final_analysis['objections'],
            call_outcome=CallOutcome(final_analysis['call_outcome']),
            farmer_responses=farmer_responses,
            agent_effectiveness=effectiveness,
            conversation_flow=final_analysis.get('conversation_flow', {}),
            emotional_indicators=final_analysis.get('emotional_indicators', [])
        )
    
    def _format_conversation(self, agent_messages: List[str], farmer_responses: List[str]) -> str:
        """Format conversation for LLM analysis"""
        conversation_text = ""
        
        for i, (agent_msg, farmer_msg) in enumerate(zip(agent_messages, farmer_responses)):
            conversation_text += f"Agent {i+1}: {agent_msg}\nFarmer {i+1}: {farmer_msg}\n\n"
        
        return conversation_text
    
    async def _get_llm_analysis(self, conversation_text: str) -> Dict:
        """Use LLM to analyze conversation"""
        
        analysis_prompt = f"""
        Analyze this conversation between a solar scheme agent and a farmer. Provide analysis in JSON format:

        CONVERSATION:
        {conversation_text}

        Analyze and provide JSON with these exact keys:
        {{
            "sentiment": "positive|neutral|negative",
            "interest_level": "high|medium|low|confused", 
            "intro_clarity": true/false,
            "objections": ["list", "of", "objections"],
            "call_outcome": "success|failure|follow_up",
            "conversation_flow": {{
                "farmer_engagement": "high|medium|low",
                "question_quality": "good|average|poor",
                "understanding_level": "clear|partial|confused"
            }},
            "emotional_indicators": ["list", "of", "emotions", "detected"]
        }}

        Consider:
        - Farmer's Hindi responses and tone
        - Questions asked by farmer about cost, process, eligibility
        - Level of engagement and interest shown
        - Any objections or concerns raised
        - Overall conversation flow and outcome
        - Trust and skepticism indicators
        - Understanding of the solar scheme concept

        Objection categories: "cost_concern", "trust_issues", "technical_confusion", "time_constraints", "eligibility_doubt", "process_complexity"
        Emotional indicators: "skeptical", "confused", "interested", "excited", "worried", "trusting", "engaged"
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.get("openai", {}).get("model", "gpt-4"),
                messages=[{"role": "user", "content": analysis_prompt}],
                max_tokens=self.config.get("openai", {}).get("max_tokens", 500),
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis_result = json.loads(json_match.group())
                self.performance_tracker.record_api_call("openai", True)
                self.logger.info("🧠 LLM conversation analysis completed")
                return analysis_result
            else:
                raise ValueError("Could not extract JSON from LLM response")
                
        except Exception as e:
            self.logger.error(f"LLM analysis error: {e}")
            self.performance_tracker.record_api_call("openai", False)
            raise e
    
    def _rule_based_analysis(self, farmer_responses: List[str]) -> Dict:
        """Fallback rule-based analysis"""
        
        all_text = " ".join(farmer_responses).lower()
        
        # Extract keywords
        keywords = extract_keywords(all_text)
        
        # Sentiment analysis
        pos_count = len(keywords.get('positive', []))
        neg_count = len(keywords.get('negative', []))
        
        if pos_count > neg_count:
            sentiment = 'positive'
        elif neg_count > pos_count:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Interest level analysis
        confused_count = len(keywords.get('confused', []))
        interested_count = len(keywords.get('interested', []))
        
        if confused_count > 1:
            interest_level = 'confused'
        elif interested_count >= 2:
            interest_level = 'high'
        elif interested_count == 1 or pos_count > 0:
            interest_level = 'medium'
        else:
            interest_level = 'low'
        
        # Intro clarity
        intro_clarity = not any(phrase in all_text for phrase in ['samajh nahi', 'kya bol rahe', 'simple mein'])
        
        # Objections detection
        objections = []
        if any(word in all_text for word in ['kitne paise', 'paisa', 'cost']):
            objections.append('cost_concern')
        if any(word in all_text for word in ['free mein', 'bilkul free']):
            objections.append('wants_free')
        if any(word in all_text for word in ['kaun ho', 'sach hai', 'government']):
            objections.append('trust_issues')
        if any(word in all_text for word in ['eligible', 'qualification']):
            objections.append('eligibility_doubt')
        if any(word in all_text for word in ['time nahi', 'busy']):
            objections.append('time_constraints')
        if confused_count > 0:
            objections.append('technical_confusion')
        
        # Call outcome
        if any(phrase in all_text for phrase in ['dobara call', 'baad mein call']):
            call_outcome = 'follow_up'
        elif sentiment == 'positive' and interest_level in ['high', 'medium'] and len(objections) <= 1:
            call_outcome = 'success'
        elif any(phrase in all_text for phrase in ['nahi chahiye', 'band karo', 'interested nahi']):
            call_outcome = 'failure'
        else:
            call_outcome = 'follow_up'
        
        # Conversation flow
        conversation_flow = {
            'farmer_engagement': 'high' if interested_count > 1 else 'medium' if interested_count > 0 else 'low',
            'question_quality': 'good' if len(objections) > 0 else 'average',
            'understanding_level': 'confused' if confused_count > 1 else 'clear' if intro_clarity else 'partial'
        }
        
        # Emotional indicators
        emotional_indicators = []
        if 'trust_issues' in objections:
            emotional_indicators.append('skeptical')
        if confused_count > 0:
            emotional_indicators.append('confused')
        if sentiment == 'positive':
            emotional_indicators.append('interested')
        if 'cost_concern' in objections:
            emotional_indicators.append('worried')
        
        self.logger.info("🧠 Rule-based conversation analysis completed")
        
        return {
            'sentiment': sentiment,
            'interest_level': interest_level,
            'intro_clarity': intro_clarity,
            'objections': objections,
            'call_outcome': call_outcome,
            'conversation_flow': conversation_flow,
            'emotional_indicators': emotional_indicators
        }
    
    def _merge_analyses(self, llm_analysis: Dict, rule_analysis: Dict) -> Dict:
        """Merge LLM and rule-based analyses"""
        
        # Use LLM as primary, but validate with rules
        merged = llm_analysis.copy()
        
        # Cross-validate objections
        rule_objections = set(rule_analysis.get('objections', []))
        llm_objections = set(llm_analysis.get('objections', []))
        
        # Combine unique objections from both analyses
        merged['objections'] = list(rule_objections.union(llm_objections))
        
        # Validate sentiment consistency
        if (llm_analysis.get('sentiment') == 'positive' and 
            rule_analysis.get('sentiment') == 'negative'):
            # If there's strong disagreement, use neutral
            merged['sentiment'] = 'neutral'
        
        self.logger.info("🧠 Merged LLM and rule-based analyses")
        return merged
    
    def get_performance_stats(self) -> Dict:
        """Get call analyzer performance statistics"""
        return self.performance_tracker.get_summary()