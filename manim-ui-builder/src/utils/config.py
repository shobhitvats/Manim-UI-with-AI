import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    def __init__(self):
        # Load configuration from config.yaml
        config_path = Path(__file__).parent.parent.parent / "config.yaml"
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
        
        # Environment variables take precedence
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.manim_path = os.getenv("MANIM_PATH", "/usr/local/bin/manim")
        self.export_formats = config_data.get("export_formats", ["mp4", "gif", "json"])
        self.default_scene_duration = 5  # seconds
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # UI settings from config
        self.ui_settings = config_data.get("ui_settings", {})

    def validate(self):
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        if not os.path.exists(self.manim_path):
            print(f"Warning: Manim path does not exist: {self.manim_path}")

config = Config()