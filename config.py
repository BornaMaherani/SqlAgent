from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    database_url: str = Field(default="sqlite:///./Messages.db", description="Database connection URL")
    
    # API settings - use deep_api from .env file
    api_key: str = Field(..., description="OpenRouter API key", alias="deep_api")
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1", description="OpenRouter API base URL")
    model_name: str = Field(default="deepseek/deepseek-chat-v3.1:free", description="LLM model name")
    
    # Application settings
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        populate_by_name = True

# Global settings instance
settings = Settings()
