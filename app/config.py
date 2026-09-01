import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class DBSettings(BaseModel):
    host: str
    internal_host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
    
class RedisSettings(BaseModel):
    host: str
    internal_host: str
    port: int
    password: str

class LLMSettings(BaseModel):
    provider: str
    api_base: str
    api_key: str
    key_alias: str
    models: list[str]
    max_budget: Optional[float] = None
    expires: Optional[str] = None

class Credentials(BaseModel):
    db: DBSettings
    redis: RedisSettings
    llm: LLMSettings

class Settings(BaseSettings):
    credentials: Credentials

    model_config = SettingsConfigDict(extra="ignore")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        json_path = Path(".env.json")
        if json_path.exists():
            return (lambda: json.loads(json_path.read_text()),)
        return ()

settings = Settings()
