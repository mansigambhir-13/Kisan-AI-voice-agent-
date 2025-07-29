import asyncio
import aiohttp
import aiofiles
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
import time

from ..utils.helpers import generate_audio_filename, PerformanceTracker

class EnhancedAudioProcessor:
    """Enhanced audio processor with improved voice functionality"""
    
    def __init__(self, deepgram_key: str, elevenlabs_key: str, config: Dict):
        self.deepgram_key = deepgram_key
        self.elevenlabs_key = elevenlabs_key
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.performance_tracker = PerformanceTracker()
        
        # ElevenLabs settings
        self.elevenlabs_voice_id = config.get("apis", {}).get("elevenlabs", {}).get("voice_id", "pNInz6obpgDQGcFmaJgB")
        self.voice_settings = config.get("apis", {}).get("elevenlabs", {}).get("voice_settings", {})
        
        # Deepgram settings
        self.deepgram_config = config.get("apis", {}).get("deepgram", {})
        
        # Cache for generated audio to avoid regenerating same text
        self.audio_cache = {}
        
        self.logger.info("🎵 Enhanced Audio Processor initialized")
    
    async def text_to_speech(self, text: str, output_path: str, voice_type: str = "agent") -> Optional[str]:
        """Convert text to speech using ElevenLabs with enhanced error handling"""
        
        # Check cache first
        cache_key = f"{text[:50]}_{voice_type}"
        if cache_key in self.audio_cache:
            self.logger.info(f"🎵 Using cached audio for: {text[:50]}...")
            return self.audio_cache[cache_key]
        
        if not self.elevenlabs_key:
            return await self._mock_text_to_speech(text, output_path, voice_type)
        
        # Select voice based on type
        voice_id = self._get_voice_id(voice_type)
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_key
        }
        
        # Enhanced voice settings based on voice type
        voice_settings = self._get_voice_settings(voice_type)
        
        data = {
            "text": text,
            "model_id": self.config.get("apis", {}).get("elevenlabs", {}).get("model_id", "eleven_multilingual_v2"),
            "voice_settings": voice_settings
        }
        
        max_retries = 3
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                    async with session.post(url, json=data, headers=headers) as response:
                        if response.status == 200:
                            audio_content = await response.read()
                            
                            # Ensure output directory exists
                            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                            
                            async with aiofiles.open(output_path, 'wb') as f:
                                await f.write(audio_content)
                            
                            # Cache the result
                            self.audio_cache[cache_key] = output_path
                            
                            self.performance_tracker.record_api_call("elevenlabs", True)
                            self.logger.info(f"🎵 Generated audio ({len(audio_content)} bytes): {output_path}")
                            return output_path
                        
                        elif response.status == 429:  # Rate limit
                            self.logger.warning(f"Rate limited, retrying in {retry_delay * 2} seconds...")
                            await asyncio.sleep(retry_delay * 2)
                            retry_delay *= 2
                            continue
                        
                        else:
                            error_text = await response.text()
                            self.logger.error(f"ElevenLabs error {response.status}: {error_text}")
                            
                            if attempt == max_retries - 1:
                                self.performance_tracker.record_api_call("elevenlabs", False)
                                return await self._mock_text_to_speech(text, output_path, voice_type)
                            
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2
                            
            except asyncio.TimeoutError:
                self.logger.error(f"Timeout on attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    return await self._mock_text_to_speech(text, output_path, voice_type)
                await asyncio.sleep(retry_delay)
                
            except Exception as e:
                self.logger.error(f"Text-to-speech error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    self.performance_tracker.record_api_call("elevenlabs", False)
                    return await self._mock_text_to_speech(text, output_path, voice_type)
                await asyncio.sleep(retry_delay)
        
        return None
    
    def _get_voice_id(self, voice_type: str) -> str:
        """Get appropriate voice ID based on voice type"""
        voice_mapping = {
            "agent": self.elevenlabs_voice_id,  # Professional Hindi voice
            "farmer": "21m00Tcm4TlvDq8ikWAM",  # Different voice for farmer simulation
            "default": self.elevenlabs_voice_id
        }
        return voice_mapping.get(voice_type, voice_mapping["default"])
    
    def _get_voice_settings(self, voice_type: str) -> Dict:
        """Get voice settings optimized for different voice types"""
        if voice_type == "agent":
            return {
                "stability": 0.6,
                "similarity_boost": 0.7,
                "style": 0.2,
                "use_speaker_boost": True
            }
        elif voice_type == "farmer":
            return {
                "stability": 0.4,
                "similarity_boost": 0.5,
                "style": 0.5,
                "use_speaker_boost": True
            }
        else:
            return self.voice_settings or {
                "stability": 0.5,
                "similarity_boost": 0.5,
                "style": 0.3,
                "use_speaker_boost": True
            }
    
    async def _mock_text_to_speech(self, text: str, output_path: str, voice_type: str = "agent") -> str:
        """Enhanced mock TTS for demo mode with realistic timing"""
        
        # Simulate realistic API delay based on text length
        text_length = len(text)
        delay = min(0.5 + (text_length / 200), 3.0)  # 0.5-3 seconds based on length
        await asyncio.sleep(delay)
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Create enhanced mock audio file with metadata
        mock_data = {
            "text": text,
            "voice_type": voice_type,
            "generated_at": time.time(),
            "duration_estimate": text_length / 10,  # Rough estimate: 10 chars per second
            "voice_settings": self._get_voice_settings(voice_type)
        }
        
        async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(mock_data, indent=2, ensure_ascii=False))
        
        self.logger.info(f"🎵 [MOCK] Generated {voice_type} audio ({len(text)} chars): {output_path}")
        return output_path
    
    async def speech_to_text(self, audio_path: str) -> Tuple[str, List[Dict]]:
        """Enhanced speech-to-text with speaker diarization"""
        
        if not self.deepgram_key:
            return await self._mock_speech_to_text(audio_path)
        
        # Read audio file
        try:
            async with aiofiles.open(audio_path, 'rb') as f:
                audio_data = await f.read()
        except Exception as e:
            self.logger.error(f"Failed to read audio file {audio_path}: {e}")
            return await self._mock_speech_to_text(audio_path)
        
        url = "https://api.deepgram.com/v1/listen"
        
        headers = {
            "Authorization": f"Token {self.deepgram_key}",
            "Content-Type": "audio/mpeg"
        }
        
        params = {
            "model": self.deepgram_config.get("model", "nova-2"),
            "language": self.deepgram_config.get("language", "hi"),
            "punctuate": "true",
            "diarize": "true",
            "smart_format": "true",
            "paragraphs": "true",
            "utterances": "true"
        }
        
        max_retries = 3
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
                    async with session.post(url, data=audio_data, headers=headers, params=params) as response:
                        if response.status == 200:
                            result = await response.json()
                            
                            # Extract transcript and speaker information
                            transcript, speakers = self._process_deepgram_response(result)
                            
                            self.performance_tracker.record_api_call("deepgram", True)
                            self.logger.info(f"🎤 Transcribed audio: {len(transcript)} characters")
                            return transcript, speakers
                        
                        elif response.status == 429:  # Rate limit
                            self.logger.warning(f"Deepgram rate limited, retrying in {retry_delay * 2} seconds...")
                            await asyncio.sleep(retry_delay * 2)
                            retry_delay *= 2
                            continue
                        
                        else:
                            error_text = await response.text()
                            self.logger.error(f"Deepgram error {response.status}: {error_text}")
                            
                            if attempt == max_retries - 1:
                                self.performance_tracker.record_api_call("deepgram", False)
                                return await self._mock_speech_to_text(audio_path)
                            
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2
                            
            except Exception as e:
                self.logger.error(f"Speech-to-text error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    self.performance_tracker.record_api_call("deepgram", False)
                    return await self._mock_speech_to_text(audio_path)
                await asyncio.sleep(retry_delay)
        
        return await self._mock_speech_to_text(audio_path)
    
    def _process_deepgram_response(self, result: Dict) -> Tuple[str, List[Dict]]:
        """Process Deepgram API response to extract transcript and speaker info"""
        
        full_transcript = ""
        speakers = []
        
        try:
            if "results" in result and "channels" in result["results"]:
                channel = result["results"]["channels"][0]
                
                if "alternatives" in channel:
                    alternative = channel["alternatives"][0]
                    full_transcript = alternative.get("transcript", "")
                    
                    # Extract speaker information from paragraphs
                    if "paragraphs" in alternative:
                        for paragraph in alternative["paragraphs"]["paragraphs"]:
                            for sentence in paragraph["sentences"]:
                                speaker_info = {
                                    "speaker": sentence.get("speaker", 0),
                                    "text": sentence.get("text", ""),
                                    "start": sentence.get("start", 0),
                                    "end": sentence.get("end", 0)
                                }
                                speakers.append(speaker_info)
        
        except Exception as e:
            self.logger.error(f"Error processing Deepgram response: {e}")
        
        return full_transcript, speakers
    
    async def _mock_speech_to_text(self, audio_path: str) -> Tuple[str, List[Dict]]:
        """Enhanced mock STT that reads from mock audio files"""
        
        await asyncio.sleep(0.5)  # Simulate processing time
        
        try:
            # Try to read mock audio file
            async with aiofiles.open(audio_path, 'r', encoding='utf-8') as f:
                mock_data = json.loads(await f.read())
                text = mock_data.get("text", "Mock transcription")
                voice_type = mock_data.get("voice_type", "unknown")
                
                # Create mock speaker data
                speakers = [{
                    "speaker": 0 if voice_type == "agent" else 1,
                    "text": text,
                    "start": 0.0,
                    "end": mock_data.get("duration_estimate", 5.0)
                }]
                
                self.logger.info(f"🎤 [MOCK] Transcribed {voice_type}: {text[:100]}...")
                return text, speakers
                
        except Exception:
            # Fallback for non-mock files
            mock_text = f"Mock transcription for {Path(audio_path).name}"
            speakers = [{"speaker": 0, "text": mock_text, "start": 0.0, "end": 5.0}]
            
            self.logger.info(f"🎤 [MOCK] Fallback transcription: {mock_text}")
            return mock_text, speakers
    
    async def combine_audio_files(self, audio_files: List[str], output_path: str) -> Optional[str]:
        """Combine multiple audio files into a single conversation file"""
        
        if not audio_files:
            return None
        
        # For mock mode, combine the text content
        if not self.elevenlabs_key:
            return await self._mock_combine_audio(audio_files, output_path)
        
        # For real audio files, you would use audio processing libraries like pydub
        # This is a simplified version
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            combined_data = []
            total_duration = 0
            
            for audio_file in audio_files:
                try:
                    async with aiofiles.open(audio_file, 'rb') as f:
                        audio_content = await f.read()
                        combined_data.append(audio_content)
                        # Estimate duration (simplified)
                        total_duration += len(audio_content) / 1000  # rough estimate
                except Exception as e:
                    self.logger.warning(f"Failed to read audio file {audio_file}: {e}")
            
            if combined_data:
                # Simple concatenation (in real implementation, use proper audio processing)
                async with aiofiles.open(output_path, 'wb') as f:
                    for data in combined_data:
                        await f.write(data)
                
                self.logger.info(f"🎵 Combined {len(audio_files)} audio files into {output_path}")
                return output_path
        
        except Exception as e:
            self.logger.error(f"Failed to combine audio files: {e}")
            return await self._mock_combine_audio(audio_files, output_path)
        
        return None
    
    async def _mock_combine_audio(self, audio_files: List[str], output_path: str) -> str:
        """Mock audio combination for demo mode"""
        
        combined_content = {
            "type": "combined_conversation",
            "source_files": audio_files,
            "combined_at": time.time(),
            "segments": []
        }
        
        for i, audio_file in enumerate(audio_files):
            try:
                async with aiofiles.open(audio_file, 'r', encoding='utf-8') as f:
                    segment_data = json.loads(await f.read())
                    segment_data["segment_index"] = i
                    combined_content["segments"].append(segment_data)
            except Exception as e:
                self.logger.warning(f"Failed to read mock audio file {audio_file}: {e}")
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(combined_content, indent=2, ensure_ascii=False))
        
        self.logger.info(f"🎵 [MOCK] Combined {len(audio_files)} audio segments into {output_path}")
        return output_path
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics for the audio processor"""
        return {
            "cache_size": len(self.audio_cache),
            "api_stats": self.performance_tracker.get_stats()
        }