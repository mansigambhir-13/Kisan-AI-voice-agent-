import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class ConfigManager:
    """Configuration manager for the voice agent system"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self._settings = None
        self._farmer_personas = None
        self._prompts = None
        
        # Load environment variables
        load_dotenv()
        
        # Load all configurations
        self._load_configurations()
    
    def _load_configurations(self):
        """Load all configuration files"""
        try:
            # Load settings.yaml
            with open(self.config_dir / "settings.yaml", 'r', encoding='utf-8') as f:
                self._settings = yaml.safe_load(f)
            
            # Load farmer_personas.json
            with open(self.config_dir / "farmer_personas.json", 'r', encoding='utf-8') as f:
                self._farmer_personas = json.load(f)
            
            # Load prompts.json
            with open(self.config_dir / "prompts.json", 'r', encoding='utf-8') as f:
                self._prompts = json.load(f)
                
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Configuration file not found: {e}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON configuration: {e}")
    
    @property
    def settings(self) -> Dict[str, Any]:
        """Get system settings"""
        return self._settings
    
    @property
    def farmer_personas(self) -> Dict[str, Any]:
        """Get farmer personas configuration"""
        return self._farmer_personas
    
    @property
    def prompts(self) -> Dict[str, Any]:
        """Get prompts configuration"""
        return self._prompts
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration with environment variables"""
        api_config = self._settings.get("apis", {}).copy()
        
        # Override with environment variables if available
        env_mappings = {
            "OPENAI_API_KEY": ("openai", "api_key"),
            "DEEPGRAM_API_KEY": ("deepgram", "api_key"),
            "ELEVENLABS_API_KEY": ("elevenlabs", "api_key"),
            "OPENAI_MODEL": ("openai", "model"),
            "DEEPGRAM_MODEL": ("deepgram", "model"),
            "ELEVENLABS_VOICE_ID": ("elevenlabs", "voice_id")
        }
        
        for env_var, (service, key) in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value:
                if service not in api_config:
                    api_config[service] = {}
                api_config[service][key] = env_value
        
        return api_config
    
    def get_paths(self) -> Dict[str, str]:
        """Get configured paths"""
        paths = self._settings.get("paths", {})
        
        # Ensure all paths exist
        for path_name, path_value in paths.items():
            Path(path_value).mkdir(parents=True, exist_ok=True)
        
        return paths
    
    def get_system_limits(self) -> Dict[str, Any]:
        """Get system limits configuration"""
        return self._settings.get("limits", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self._settings.get("logging", {})
    
    def get_learning_config(self) -> Dict[str, Any]:
        """Get learning configuration"""
        return self._settings.get("learning", {})
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """Validate that required API keys are present"""
        required_keys = ["OPENAI_API_KEY", "DEEPGRAM_API_KEY", "ELEVENLABS_API_KEY"]
        validation_results = {}
        
        for key in required_keys:
            validation_results[key] = bool(os.getenv(key))
        
        return validation_results
    
    def get_missing_api_keys(self) -> List[str]:
        """Get list of missing API keys"""
        validation = self.validate_api_keys()
        return [key for key, is_present in validation.items() if not is_present]