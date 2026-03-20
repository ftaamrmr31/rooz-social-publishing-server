from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # App Configuration
    APP_NAME: str = "Rooz Social Publishing Server"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Environment
    ENVIRONMENT: str = "development"

    # Telegram Integration
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


# Global settings instance
settings = Settings()