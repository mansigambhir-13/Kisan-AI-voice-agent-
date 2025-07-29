# 🎯 Voice Agent Reinforcement Learning System

A sophisticated AI voice agent system that learns and improves from farmer outreach calls through reinforcement learning. Built for agricultural schemes like PM-KUSUM Yojana.

## 🌟 Features

### 🗣️ Voice Functionality
- **Text-to-Speech (TTS)**: ElevenLabs integration with Hindi voice support
- **Speech-to-Text (STT)**: Deepgram integration with speaker diarization
- **Multi-language Support**: Optimized for Hindi with English fallback
- **Voice Caching**: Intelligent caching to reduce API calls

### 🧠 Intelligent Analysis
- **Sentiment Detection**: Real-time farmer emotion analysis
- **Interest Level Assessment**: Gauges farmer engagement
- **Objection Tracking**: Identifies and categorizes concerns
- **Call Outcome Classification**: Success/Failure/Follow-up determination

### 🔄 Reinforcement Learning
- **Automatic Improvement**: Learns from each call interaction
- **Prompt Evolution**: Adapts conversation scripts based on performance
- **Multi-dimensional Learning**: Improves intro clarity, tone, and CTAs
- **Performance Tracking**: Comprehensive effectiveness scoring

### 📊 Analytics & Reporting
- **Call Analysis**: Detailed conversation breakdowns
- **Learning Trends**: Visual progress tracking
- **Performance Metrics**: Effectiveness scoring and improvement rates
- **Comprehensive Reports**: JSON exports with full conversation data

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd voice-agent-project

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Add your API keys to .env
OPENAI_API_KEY=your_openai_key_here
DEEPGRAM_API_KEY=your_deepgram_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

### 3. Run the Demo

```bash
# Run the complete demonstration
python demo_voice_system.py

# Or run the main system
python src/main_voice_system.py
```

## 🎬 Demo Modes

### 🔧 Mock Mode (No API Keys Required)
- Simulates all voice functionality
- Perfect for testing and development
- Generates realistic conversation flows
- Shows complete learning loop

### 🌐 Full Mode (With API Keys)
- Real TTS/STT processing
- Actual voice generation and transcription
- Production-ready functionality
- Enhanced audio quality

## 📁 Project Structure

```
voice-agent-project/
├── src/
│   ├── components/          # Core system components
│   │   ├── voice_agent.py           # Main voice agent
│   │   ├── audio_processor.py       # TTS/STT handling
│   │   ├── enhanced_audio_processor.py  # Enhanced audio features
│   │   ├── call_analyzer.py         # Call analysis engine
│   │   ├── reinforcement_engine.py  # Learning system
│   │   └── farmer_persona.py        # Farmer simulation
│   ├── models/
│   │   └── data_models.py           # Data structures
│   ├── utils/
│   │   └── helpers.py               # Utility functions
│   ├── main_voice_system.py         # Main system entry
│   └── demo_system.py               # Demo version
├── config/
│   ├── settings.yaml               # System configuration
│   ├── prompts.json               # Agent prompts
│   └── farmer_personas.json      # Farmer profiles
├── data/
│   └── output/                    # Generated outputs
├── demo_voice_system.py           # Complete demo script
├── requirements.txt               # Dependencies
└── .env.example                  # Environment template
```

## 🎭 System Components

### 1. Voice Agent (`VoiceAgent`)
- Conducts simulated voice calls
- Manages conversation flow
- Integrates with audio processing
- Tracks conversation history

### 2. Audio Processor (`EnhancedAudioProcessor`)
- **ElevenLabs TTS**: High-quality voice synthesis
- **Deepgram STT**: Accurate speech transcription
- **Speaker Diarization**: Separates agent and farmer voices
- **Error Handling**: Robust retry mechanisms
- **Caching**: Optimizes API usage

### 3. Call Analyzer (`CallAnalyzer`)
- **Sentiment Analysis**: Detects farmer emotions
- **Interest Assessment**: Measures engagement levels
- **Objection Detection**: Identifies concerns and barriers
- **Effectiveness Scoring**: Quantifies call success

### 4. Reinforcement Engine (`ReinforcementEngine`)
- **LLM-based Learning**: Uses GPT-4 for improvements
- **Rule-based Fallback**: Ensures reliability
- **Multi-dimensional Optimization**: Improves multiple aspects
- **Version Tracking**: Maintains prompt evolution history

### 5. Farmer Persona (`LLMFarmerPersona`)
- **Realistic Simulation**: Generates authentic farmer responses
- **Profile-based Behavior**: Adapts to farmer characteristics
- **Cultural Context**: Incorporates Indian agricultural context
- **Skepticism Modeling**: Varies trust levels realistically

## 📊 Analytics Categories

The system analyzes calls across 5 key dimensions:

| Category | Description | Examples |
|----------|-------------|----------|
| **Farmer Sentiment** | Emotional tone detection | Positive: "haan haan", Negative: "mat batana" |
| **Interest Level** | Engagement measurement | High: "batao", Low: "nahi chahiye" |
| **Intro Clarity** | Opening pitch effectiveness | Confusion: "samajh nahi aaya" |
| **Objections** | Concerns and barriers | Cost: "Kitne ka hai?", Eligibility: "Main eligible hoon?" |
| **Call Outcome** | Final result classification | Success, Failure, Follow-up needed |

## 🔄 Reinforcement Learning Loop

### Learning Triggers & Actions

| Trigger Condition | Improvement Action |
|-------------------|-------------------|
| Farmer confusion in first 30s | Simplify introduction |
| Negative sentiment detected | Soften tone, add empathy |
| Repeated clarification questions | Rewrite in simpler language |
| Ignored call-to-action | Reframe as yes/no question |
| "Call me later" response | Add to follow-up list |

### Learning Process

1. **Call Execution**: Voice agent conducts call
2. **Analysis**: Multi-dimensional performance assessment
3. **Learning**: LLM generates improvements
4. **Application**: Updated prompts for next call
5. **Tracking**: Performance metrics recorded

## 🎯 Usage Examples

### Basic Usage

```python
from src.main_voice_system import VoiceAgentSystem
from src.models.data_models import FarmerProfile, EducationLevel, IncomeLevel

# Initialize system
system = VoiceAgentSystem()

# Create farmer profile
farmer = FarmerProfile(
    id="farmer_001",
    name="राम सिंह",
    age=45,
    education=EducationLevel.LOW,
    income=IncomeLevel.LOW,
    location="राजस्थान",
    crops=["गेहूं", "बाजरा"],
    land_size="5 एकड़",
    skepticism=0.7,
    govt_experience="कुछ योजनाओं का अनुभव",
    family_size=5
)

# Run voice call simulation
result = await system.run_voice_call_simulation(farmer)

# Access results
effectiveness = result['effectiveness_score']
analysis = result['analysis']
conversation = result['conversation']
```

### Batch Processing

```python
# Run multiple simulations
results = await system.run_multiple_simulations(num_simulations=10)

# Generate comprehensive report
await system.generate_final_report(results)
```

## 🔧 Configuration

### API Settings (`config/settings.yaml`)

```yaml
apis:
  openai:
    model: "gpt-4"
    temperature: 0.7
    max_tokens: 500
  
  deepgram:
    model: "nova-2"
    language: "hi"  # Hindi
    diarize: true
  
  elevenlabs:
    voice_id: "pNInz6obpgDQGcFmaJgB"  # Hindi voice
    model_id: "eleven_multilingual_v2"
```

### Farmer Personas (`config/farmer_personas.json`)

```json
{
  "skeptical_traditional": {
    "characteristics": ["High skepticism", "Traditional approach"],
    "common_responses": ["सच में?", "पहले भी ऐसा कहा था"],
    "objection_patterns": ["Cost concerns", "Trust issues"]
  }
}
```

## 📈 Performance Metrics

### Effectiveness Scoring

The system calculates effectiveness based on:
- **Sentiment Score** (30%): Farmer's emotional response
- **Interest Level** (25%): Engagement and curiosity
- **Intro Clarity** (20%): Understanding of opening pitch
- **Objection Handling** (15%): Success in addressing concerns
- **Call Outcome** (10%): Final result achievement

### Learning Metrics

- **Improvement Rate**: Percentage of calls showing improvement
- **Learning Velocity**: Speed of adaptation over iterations
- **Consistency Score**: Stability of performance gains
- **Retention Rate**: Maintenance of learned improvements

## 🎨 Customization

### Adding New Farmer Personas

```python
# Create custom farmer profile
custom_farmer = FarmerProfile(
    id="custom_001",
    name="Your Farmer Name",
    # ... other attributes
    persona_type="your_custom_type"
)

# Add persona configuration to config/farmer_personas.json
```

### Custom Learning Rules

```python
# Extend ReinforcementEngine
class CustomReinforcementEngine(ReinforcementEngine):
    def custom_learning_rule(self, analysis):
        # Your custom learning logic
        pass
```

## 🚨 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure `.env` file exists with valid keys
   - Check API key permissions and quotas

2. **Audio Generation Failures**
   - System automatically falls back to mock mode
   - Check ElevenLabs account limits

3. **Transcription Issues**
   - Verify Deepgram API key validity
   - Ensure audio files are in supported format

4. **Learning Not Improving**
   - Check OpenAI API connectivity
   - Verify conversation data quality

### Debug Mode

```bash
# Run with debug logging
LOG_LEVEL=DEBUG python demo_voice_system.py

# Check system logs
tail -f demo_voice_system.log
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **ElevenLabs** for high-quality text-to-speech
- **Deepgram** for accurate speech recognition
- **OpenAI** for powerful language models
- **Indian Agricultural Community** for inspiration and context

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Check the documentation
- Review the demo logs for debugging

---

**Built with ❤️ for Indian farmers and agricultural development**