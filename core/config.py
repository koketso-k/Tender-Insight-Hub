from pydantic import BaseSettings

class AppConfig(BaseSettings):
    APP_NAME: str = "Tender Insight Hub"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"
