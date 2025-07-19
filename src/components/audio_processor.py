import asyncio
import aiohttp
import aiofiles
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from deepgram import Deepgram
import logging

from ..utils.helpers import generate_audio_filename, PerformanceTracker

class AudioProcessor:
    """Handles audio processing with Deepgram and ElevenLabs"""
    
    def __init__(self, deepgram_key: str, elevenlabs_key: str, config: Dict):
        self.deepgram_key = deepgram_key
        self.elevenlabs_key = elevenlabs_key
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.performance_tracker = PerformanceTracker()
        
        # Initialize Deepgram
        if deepgram_key:
            self.deepgram = Deepgram(deepgram_key)
        else:
            self.deepgram = None
            self.logger.warning("Deepgram API key not provided - using mock mode")
        
        # ElevenLabs settings
        self.elevenlabs_voice_id = config.get("elevenlabs", {}).get("voice_id", "pNInz6obpgDQGcFmaJgB")
        self.voice_settings = config.get("elevenlabs", {}).get("voice_settings", {})
        
    async def text_to_speech(self, text: str, output_path: str) -> Optional[str]:
        """Convert text to speech using ElevenLabs"""
        
        if not self.elevenlabs_key:
            return await self._mock_text_to_speech(text, output_path)
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_key
        }
        
        data = {
            "text": text,
            "model_id": self.config.get("elevenlabs", {}).get("model_id", "eleven_multilingual_v2"),
            "voice_settings": {
                "stability": self.voice_settings.get("stability", 0.5),
                "similarity_boost": self.voice_settings.get("similarity_boost", 0.5),
                "style": self.voice_settings.get("style", 0.3),
                "use_speaker_boost": self.voice_settings.get("use_speaker_boost", True)
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as response:
                    if response.status == 200:
                        audio_content = await response.read()
                        
                        # Ensure output directory exists
                        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                        
                        async with aiofiles.open(output_path, 'wb') as f:
                            await f.write(audio_content)
                        
                        self.performance_tracker.record_api_call("elevenlabs", True)
                        self.logger.info(f"🎵 Generated audio: {output_path}")
                        return output_path
                    else:
                        error_text = await response.text()
                        self.logger.error(f"ElevenLabs error {response.status}: {error_text}")
                        self.performance_tracker.record_api_call("elevenlabs", False)
                        return None
                        
        except Exception as e:
            self.logger.error(f"Text-to-speech error: {e}")
            self.performance_tracker.record_api_call("elevenlabs", False)
            return None
    
    async def _mock_text_to_speech(self, text: str, output_path: str) -> str:
        """Mock TTS for demo mode"""
        await asyncio.sleep(0.3)  # Simulate API delay
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Create mock audio file
        async with aiofiles.open(output_path, 'w') as f:
            await f.write(f"Mock audio file for: {text[:100]}...")
        
        self.logger.info(f"🎵 [MOCK] Generated audio: {output_path}")
        return output_path
    
    async def speech_to_text(self, audio_path: str) -> Tuple[str, List[Dict]]:
        """Transcribe audio using Deepgram with speaker diarization"""
        
        if not self.deepgram:
            return await self._mock_speech_to_text(audio_path)
        
        try:
            with open(audio_path, 'rb') as audio_file:
                source = {'buffer': audio_file, 'mimetype': 'audio/mpeg'}
                
                options = {
                    'punctuate': self.config.get("deepgram", {}).get("punctuate", True),
                    'model': self.config.get("deepgram", {}).get("model", "nova-2"),
                    'language': self.config.get("deepgram", {}).get("language", "hi"),
                    'diarize': True,
                    'smart_format': True,
                    'utterances': True
                }
                
                response = await self.deepgram.transcription.prerecorded(source, options)
                
                # Extract transcript and speaker information
                full_transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                
                # Extract utterances with speaker info
                utterances = []
                if 'utterances' in response['results']:
                    for utterance in response['results']['utterances']:
                        utterances.append({
                            'speaker': utterance['speaker'],
                            'text': utterance['transcript'],
                            'start': utterance['start'],
                            'end': utterance['end'],
                            'confidence': utterance.get('confidence', 0.0)
                        })
                
                self.performance_tracker.record_api_call("deepgram", True)
                self.logger.info(f"🎧 Transcribed audio: {len(utterances)} utterances")
                return full_transcript, utterances
                
        except Exception as e:
            self.logger.error(f"Speech-to-text error: {e}")
            self.performance_tracker.record_api_call("deepgram", False)
            return "", []
    
    async def _mock_speech_to_text(self, audio_path: str) -> Tuple[str, List[Dict]]:
        """Mock STT for demo mode"""
        await asyncio.sleep(0.5)  # Simulate API delay
        
        # Mock transcript based on filename
        if "agent" in audio_path:
            transcript = "Namaste ji, main solar scheme ke baare mein baat kar raha hun. PM-KUSUM yojana ke through aap solar pump lagwa sakte hain."
        else:
            transcript = "Haan bhai, sun raha hun. Ye solar pump kaise kaam karta hai?"
        
        # Mock utterances with speaker separation
        utterances = [
            {
                'speaker': 0 if "agent" in audio_path else 1,
                'text': transcript,
                'start': 0.0,
                'end': 5.0,
                'confidence': 0.95
            }
        ]
        
        self.logger.info(f"🎧 [MOCK] Transcribed: {audio_path}")
        return transcript, utterances
    
    def separate_speakers(self, utterances: List[Dict]) -> Tuple[List[str], List[str]]:
        """Separate agent and farmer speech from utterances"""
        
        agent_parts = []
        farmer_parts = []
        
        for utterance in utterances:
            # Assume speaker 0 is agent, speaker 1 is farmer
            # In real implementation, you'd use voice recognition or other methods
            if utterance['speaker'] == 0:
                agent_parts.append(utterance['text'])
            else:
                farmer_parts.append(utterance['text'])
        
        return agent_parts, farmer_parts
    
    def get_performance_stats(self) -> Dict:
        """Get audio processing performance statistics"""
        return self.performance_tracker.get_summary()