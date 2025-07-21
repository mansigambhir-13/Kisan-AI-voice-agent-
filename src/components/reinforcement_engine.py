import asyncio
import json
import re
from typing import Dict, List, Optional
import openai
import logging

from ..models.data_models import AgentPrompt, CallAnalysis
from ..utils.helpers import PerformanceTracker

class ReinforcementEngine:
    """Enhanced learning engine with LLM-based improvements"""
    
    def __init__(self, openai_api_key: str, config: Dict, prompts_config: Dict):
        self.openai_api_key = openai_api_key
        self.config = config
        self.prompts_config = prompts_config
        self.logger = logging.getLogger(__name__)
        self.performance_tracker = PerformanceTracker()
        
        if openai_api_key:
            openai.api_key = openai_api_key
        else:
            self.logger.warning("OpenAI API key not provided - using rule-based improvements")
        
        # Load improvement templates
        self.improvement_templates = prompts_config.get("improvement_templates", {})
        self.response_templates = prompts_config.get("response_templates", {})
    
    async def learn_and_improve(self, current_prompt: AgentPrompt, analysis: CallAnalysis, 
                              conversation_history: List[str]) -> AgentPrompt:
        """Use LLM to generate improvements based on analysis"""
        
        if self.openai_api_key:
            try:
                return await self._llm_based_improvement(current_prompt, analysis, conversation_history)
            except Exception as e:
                self.logger.error(f"LLM improvement failed: {e}, falling back to rule-based")
                return self._rule_based_improvement(current_prompt, analysis)
        else:
            return self._rule_based_improvement(current_prompt, analysis)
    
    async def _llm_based_improvement(self, current_prompt: AgentPrompt, analysis: CallAnalysis,
                                   conversation_history: List[str]) -> AgentPrompt:
        """Generate improvements using LLM"""
        
        improvement_prompt = f"""
        You are an expert in conversation optimization for agricultural outreach in India.
        
        CURRENT AGENT PROMPT:
        Intro: {current_prompt.intro}
        Benefits: {current_prompt.benefits}
        Call-to-Action: {current_prompt.call_to_action}
        Version: {current_prompt.version}
        Tone Instructions: {current_prompt.tone_instructions}
        
        CALL ANALYSIS:
        - Sentiment: {analysis.sentiment.value}
        - Interest Level: {analysis.interest_level.value}
        - Intro Clarity: {analysis.intro_clarity}
        - Objections: {analysis.objections}
        - Outcome: {analysis.call_outcome.value}
        - Effectiveness: {analysis.agent_effectiveness}
        - Emotional Indicators: {analysis.emotional_indicators}
        
        CONVERSATION SAMPLE:
        {conversation_history[-6:] if conversation_history else []}
        
        Generate an improved agent prompt that addresses the issues found. Provide response in JSON:
        {{
            "intro": "improved introduction in Hindi",
            "benefits": ["list", "of", "improved", "benefits", "in", "Hindi"],
            "call_to_action": "improved CTA in Hindi",
            "tone_instructions": "how agent should speak",
            "conversation_style": "conversation approach",
            "improvements_made": ["list", "of", "specific", "improvements", "applied"]
        }}
        
        IMPROVEMENT FOCUS:
        - Making Hindi more natural and farmer-friendly
        - Addressing specific objections raised ({', '.join(analysis.objections)})
        - Improving clarity if farmer was confused
        - Adjusting tone based on sentiment ({analysis.sentiment.value})
        - Making benefits more compelling and relevant
        - Simplifying language if understanding was poor
        - Building trust if trust issues were detected
        - Emphasizing cost-effectiveness if cost concerns were raised
        
        GUIDELINES:
        - Keep Hindi authentic and simple
        - Use "aap" for respect
        - Include government credibility if trust issues
        - Break down costs clearly if cost concerns
        - Simplify technical terms if confusion detected
        - Add empathy if negative sentiment
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.get("openai", {}).get("model", "gpt-4"),
                messages=[{"role": "user", "content": improvement_prompt}],
                max_tokens=self.config.get("openai", {}).get("max_tokens", 800),
                temperature=0.7
            )
            
            improvement_text = response.choices[0].message.content.strip()
            
            # Extract JSON
            json_match = re.search(r'\{.*\}', improvement_text, re.DOTALL)
            if json_match:
                improvements = json.loads(json_match.group())
                
                # Create new prompt
                new_prompt = AgentPrompt(
                    intro=improvements.get('intro', current_prompt.intro),
                    benefits=improvements.get('benefits', current_prompt.benefits),
                    call_to_action=improvements.get('call_to_action', current_prompt.call_to_action),
                    version=current_prompt.version + 1,
                    improvements=current_prompt.improvements + improvements.get('improvements_made', []),
                    tone_instructions=improvements.get('tone_instructions', current_prompt.tone_instructions),
                    conversation_style=improvements.get('conversation_style', current_prompt.conversation_style)
                )
                
                self.performance_tracker.record_api_call("openai", True)
                self.logger.info(f"🧠 LLM generated {len(improvements.get('improvements_made', []))} improvements")
                
                return new_prompt
            else:
                raise ValueError("Could not extract JSON from LLM response")
            
        except Exception as e:
            self.logger.error(f"LLM improvement error: {e}")
            self.performance_tracker.record_api_call("openai", False)
            raise e
    
    def _rule_based_improvement(self, current_prompt: AgentPrompt, analysis: CallAnalysis) -> AgentPrompt:
        """Fallback rule-based improvements"""
        
        new_prompt = AgentPrompt(
            intro=current_prompt.intro,
            benefits=current_prompt.benefits.copy(),
            call_to_action=current_prompt.call_to_action,
            version=current_prompt.version + 1,
            improvements=current_prompt.improvements.copy(),
            tone_instructions=current_prompt.tone_instructions,
            conversation_style=current_prompt.conversation_style
        )
        
        improvements_made = []
        
        # Apply rule-based improvements
        
        # 1. Trust building
        if 'trust_issues' in analysis.objections:
            trust_template = self.improvement_templates.get("trust_building", {})
            intro_prefix = trust_template.get("intro_prefix", "Namaste ji! Main government authorized solar scheme advisor hun.")
            new_prompt.intro = intro_prefix + " " + new_prompt.intro
            improvements_made.append("Added government authorization and identity for trust building")
        
        # 2. Cost clarity
        if 'cost_concern' in analysis.objections or 'wants_free' in analysis.objections:
            cost_template = self.improvement_templates.get("cost_clarity", {})
            cost_explanations = cost_template.get("cost_explanations", [])
            if cost_explanations:
                new_prompt.benefits = cost_explanations + new_prompt.benefits[1:]
                improvements_made.append("Emphasized exact cost breakdown and subsidies")
        
        # 3. Simplification
        if not analysis.intro_clarity or analysis.interest_level.value == "confused":
            simplification_template = self.improvement_templates.get("simplification", {})
            simple_explanations = simplification_template.get("simple_explanations", [])
            if simple_explanations:
                new_prompt.intro = "Namaste ji! " + simple_explanations[0]
                improvements_made.append("Simplified introduction with basic explanation")
        
        # 4. Tone adjustment
        if analysis.sentiment.value == "negative":
            new_prompt.intro = new_prompt.intro.replace("call kar raha hun", "aapse baat karna chahta hun")
            new_prompt.tone_instructions = "Very polite, patient, build trust first"
            improvements_made.append("Softened tone and approach for negative sentiment")
        
        # 5. Process clarity
        if 'process_complexity' in analysis.objections:
            new_prompt.call_to_action = "Kya main aapko simple process WhatsApp pe bhej sakta hun? Sirf 3 steps hain."
            improvements_made.append("Simplified call-to-action with process clarity")
        
        # 6. Technical explanation
        if 'technical_confusion' in analysis.objections:
            tech_explanation = "Solar pump matlab sun ki energy se paani nikalne waala pump - bijli ki zarurat nahi."
            new_prompt.intro = new_prompt.intro + " " + tech_explanation
            improvements_made.append("Added simple technical explanation")
        
        # 7. Effectiveness-based improvements
        if analysis.agent_effectiveness < 0.4:
            # Major overhaul needed
            new_prompt.intro = "Namaste ji! Main government ki PM-KUSUM scheme ke baare mein 2 minute mein batana chahta hun."
            new_prompt.call_to_action = "Kya aap 2 minute sun sakte hain? Ya main WhatsApp pe details bhej dun?"
            improvements_made.append("Major restructuring due to low effectiveness")
        
        new_prompt.improvements.extend(improvements_made)
        
        self.logger.info(f"🧠 Applied {len(improvements_made)} rule-based improvements")
        
        return new_prompt
    
    def get_improvement_suggestions(self, analysis: CallAnalysis) -> List[str]:
        """Get specific improvement suggestions based on analysis"""
        suggestions = []
        
        if 'trust_issues' in analysis.objections:
            suggestions.append("Add government authorization and credible identity")
        
        if 'cost_concern' in analysis.objections:
            suggestions.append("Provide clear cost breakdown upfront")
        
        if not analysis.intro_clarity:
            suggestions.append("Simplify introduction and technical terms")
        
        if analysis.sentiment.value == "negative":
            suggestions.append("Soften tone and build rapport first")
        
        if analysis.interest_level.value == "confused":
            suggestions.append("Add simple explanations and examples")
        
        if analysis.agent_effectiveness < 0.5:
            suggestions.append("Consider major restructuring of approach")
        
        return suggestions
    
    def get_performance_stats(self) -> Dict:
        """Get reinforcement engine performance statistics"""
        return self.performance_tracker.get_summary()