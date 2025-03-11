from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str
    OPENAI_API_KEY: str
    OPENAI_ORGANIZATION: str
    OPENAI_PROJECT: str
    YANDEX_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings: Settings = Settings()
