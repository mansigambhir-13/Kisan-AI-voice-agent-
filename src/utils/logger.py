import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console

class VoiceAgentLogger:
    """Enhanced logger for the voice agent system"""
    
    def __init__(self, name: str = "voice_agent", config: Optional[dict] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with file and console handlers"""
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Set logging level
        level = getattr(logging, self.config.get("level", "INFO").upper())
        self.logger.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            self.config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Console handler with Rich
        console_handler = RichHandler(
            console=Console(stderr=True),
            show_time=True,
            show_path=False,
            markup=True
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        log_file = self.config.get("file", "data/output/system.log")
        if log_file:
            # Ensure log directory exists
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            
            # Rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=self._parse_size(self.config.get("max_file_size", "10MB")),
                backupCount=self.config.get("backup_count", 5),
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def _parse_size(self, size_str: str) -> int:
        """Parse size string like '10MB' to bytes"""
        size_str = size_str.upper()
        multipliers = {
            'B': 1,
            'KB': 1024,
            'MB': 1024**2,
            'GB': 1024**3
        }
        
        for suffix, multiplier in multipliers.items():
            if size_str.endswith(suffix):
                return int(size_str[:-len(suffix)]) * multiplier
        
        return int(size_str)  # Assume bytes if no suffix
    
    def get_logger(self) -> logging.Logger:
        """Get the configured logger"""
        return self.logger
    
    def log_call_start(self, call_id: str, farmer_name: str):
        """Log call start"""
        self.logger.info(f"📞 [bold green]Call Started[/bold green] - ID: {call_id}, Farmer: {farmer_name}")
    
    def log_call_end(self, call_id: str, outcome: str, effectiveness: float):
        """Log call end"""
        self.logger.info(f"📞 [bold blue]Call Ended[/bold blue] - ID: {call_id}, Outcome: {outcome}, Effectiveness: {effectiveness:.2f}")
    
    def log_api_call(self, service: str, operation: str, status: str):
        """Log API calls"""
        status_color = "green" if status == "success" else "red" if status == "error" else "yellow"
        self.logger.info(f"🔌 [{status_color}]{service}[/{status_color}] - {operation}: {status}")
    
    def log_learning_improvement(self, version: int, improvements: list):
        """Log learning improvements"""
        self.logger.info(f"🧠 [bold purple]Learning Applied[/bold purple] - Agent v{version}, Improvements: {len(improvements)}")
        for improvement in improvements:
            self.logger.info(f"   ✨ {improvement}")
    
    def log_error_with_context(self, error: Exception, context: dict):
        """Log error with additional context"""
        self.logger.error(f"❌ Error: {str(error)}")
        for key, value in context.items():
            self.logger.error(f"   {key}: {value}")

def setup_logger(name: str = "voice_agent", config: Optional[dict] = None) -> logging.Logger:
    """Setup and return a logger instance"""
    voice_logger = VoiceAgentLogger(name, config)
    return voice_logger.get_logger()