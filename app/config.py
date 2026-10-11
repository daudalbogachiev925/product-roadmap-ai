from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@db:5432/roadmap"
    REDIS_URL: str = "redis://redis:6379/0"
    JIRA_BASE_URL: str = ""
    JIRA_EMAIL: str = ""
    JIRA_TOKEN: str = ""
    LINEAR_API_KEY: str = ""
    DEFAULT_VELOCITY: float = 40.0
    DEFAULT_SIMULATIONS: int = 10000
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
