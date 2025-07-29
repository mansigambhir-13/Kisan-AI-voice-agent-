# Voice Agent Reinforcement Learning System

A self-improving voice agent system designed for farmer outreach campaigns, specifically for government solar schemes like PM-KUSUM Yojana.

## 🎯 Overview

This system demonstrates a complete reinforcement learning loop for voice-based outreach:

1. **Voice Agent** makes calls to farmers with personalized scripts
2. **Call Analysis** extracts insights from conversations (sentiment, interest, objections)
3. **Reinforcement Learning** improves the agent based on call outcomes
4. **Continuous Improvement** cycle repeats to optimize performance

## 🏗️ System Architecture

### Core Components

#### 1. Voice Agent (`VoiceAgent`)
- Simulates outbound calls to farmers
- Generates personalized conversations based on farmer profiles
- Adapts responses based on farmer skepticism and education levels
- Handles objections and provides relevant information

#### 2. Call Analyzer (`CallAnalyzer`)
- Analyzes conversation transcripts for sentiment and interest
- Extracts key insights and objections
- Identifies areas for improvement
- Calculates confidence scores for analysis

#### 3. Reinforcement Engine (`ReinforcementEngine`)
- Learns from call outcomes and farmer responses
- Generates improved prompts based on analysis
- Tracks performance metrics over time
- Implements continuous improvement strategies

#### 4. Main System (`VoiceAgentSystem`)
- Orchestrates all components
- Manages the learning cycle
- Provides comprehensive reporting
- Demonstrates system evolution

### Data Models

- **FarmerProfile**: Complete farmer demographics and characteristics
- **CallTranscript**: Conversation turn-by-turn with timestamps
- **CallAnalysis**: Structured insights from conversation analysis
- **VoiceAgentPrompt**: Evolving agent instructions with version tracking

## 🚀 Quick Start

### Prerequisites
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the Demo
```bash
python demo_voice_system.py
```

## 📊 System Features

### Voice Agent Capabilities
- **Personalized Introductions**: Adapts to farmer name and location
- **Dynamic Benefits Explanation**: Tailored based on income level
- **Objection Handling**: Addresses common concerns (cost, trust, complexity)
- **Context-Aware Responses**: Considers farmer skepticism and education

### Analysis Capabilities
- **Sentiment Analysis**: Positive, neutral, or negative farmer sentiment
- **Interest Level Detection**: High, medium, low, or confused interest
- **Objection Extraction**: Identifies specific concerns and objections
- **Confidence Scoring**: Measures analysis reliability

### Learning Capabilities
- **Performance Tracking**: Success rates and confidence metrics
- **Prompt Evolution**: Version-controlled prompt improvements
- **Insight Generation**: Actionable improvement suggestions
- **Continuous Optimization**: Iterative system enhancement

## 🔄 Learning Cycle

### 1. Call Execution
```
Farmer Profile → Voice Agent → Conversation → Transcript
```

### 2. Analysis Phase
```
Transcript → Call Analyzer → Sentiment + Interest + Objections
```

### 3. Learning Phase
```
Analysis → Reinforcement Engine → Improved Prompt → Next Call
```

### 4. Improvement Tracking
```
Performance Metrics → Version Control → Success Rate Optimization
```

## 📈 Example Output

```
🎯 Making call to Lakshmi Devi (39 years old)
📍 Location: Haryana
🌾 Crops: cotton, sugarcane
💰 Income level: medium
🎓 Education: high
🤔 Skepticism level: 0.37

📊 CALL ANALYSIS RESULTS:
   Sentiment: POSITIVE
   Interest Level: HIGH
   Call Outcome: SUCCESS
   Confidence Score: 0.9
   Intro Clarity: ✅

💡 KEY INSIGHTS:
   • Farmer showed positive sentiment towards the scheme
   • Farmer expressed high interest in applying

🔧 IMPROVEMENT SUGGESTIONS:
   • Address skepticism more directly
   • Add more concrete examples
```

## 🎛️ Configuration

### Farmer Profiles
The system generates realistic farmer profiles with:
- **Demographics**: Age, education, income level
- **Location**: Geographic distribution across states
- **Crops**: Realistic crop combinations
- **Skepticism**: Varying trust levels in government schemes
- **Experience**: Previous government scheme interactions

### Agent Prompts
Evolving prompts that include:
- **Base Instructions**: Core communication guidelines
- **Improvement History**: Tracked enhancements over time
- **Performance Metrics**: Success rates and confidence scores
- **Version Control**: Systematic prompt evolution

## 🔧 Customization

### Adding New Farmer Types
```python
def _generate_farmer_profile(self) -> FarmerProfile:
    # Add new names, locations, crops, etc.
    names = ["New Name", "Another Name"]
    locations = ["New State", "Another State"]
    # ... customize as needed
```

### Extending Analysis
```python
def _analyze_sentiment(self, transcript: List[CallTranscript]) -> SentimentType:
    # Add new keywords or analysis logic
    self.positive_keywords.extend(["new_positive_word"])
    self.negative_keywords.extend(["new_negative_word"])
```

### Custom Learning Rules
```python
def _generate_improved_prompt(self, current_prompt: VoiceAgentPrompt, analysis: CallAnalysis) -> VoiceAgentPrompt:
    # Add custom improvement logic based on analysis
    if "custom_condition" in analysis.improvement_suggestions:
        base_prompt += "\n\nCUSTOM IMPROVEMENT: Your custom enhancement"
```

## 📊 Performance Metrics

The system tracks:
- **Success Rate**: Percentage of successful calls
- **Average Confidence**: Reliability of analysis
- **Improvement Progress**: Version-to-version enhancements
- **Objection Patterns**: Common farmer concerns
- **Learning Effectiveness**: System adaptation speed

## 🎯 Use Cases

### Government Outreach
- **PM-KUSUM Yojana**: Solar pump scheme promotion
- **Agricultural Subsidies**: Various government benefit programs
- **Rural Development**: Infrastructure and modernization schemes

### Business Applications
- **Customer Service**: Automated call center optimization
- **Sales Outreach**: Product promotion and lead generation
- **Market Research**: Automated survey and feedback collection

## 🔮 Future Enhancements

### Planned Features
- **Real Audio Integration**: Connect with actual TTS/STT services
- **Advanced NLP**: More sophisticated conversation analysis
- **Multi-language Support**: Regional language adaptation
- **Real-time Learning**: Live prompt updates during calls
- **A/B Testing**: Systematic prompt comparison
- **Emotional Intelligence**: Tone and emotion detection

### Integration Possibilities
- **CRM Systems**: Customer relationship management
- **Analytics Platforms**: Advanced reporting and insights
- **Voice Platforms**: Twilio, Vapi, or similar services
- **AI Services**: OpenAI, Google AI, or custom models

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

### Testing
```bash
# Run the demo system
python demo_voice_system.py

# Run with custom parameters
python demo_voice_system.py --calls 10 --verbose
```

## 📄 License

This project is designed for educational and demonstration purposes. Feel free to adapt and extend for your specific use cases.

## 🙏 Acknowledgments

- **PM-KUSUM Yojana**: Government solar scheme inspiration
- **Farmer Communities**: Real-world feedback and insights
- **AI/ML Community**: Reinforcement learning methodologies
- **Voice Technology**: Modern speech processing capabilities

---

**Note**: This is a demonstration system that simulates voice calls. For production use, integrate with actual voice services and ensure compliance with local regulations and privacy laws.