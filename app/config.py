# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/hygen?options=-csearch_path=hygen_re"
    WHATSAPP_VERIFY_TOKEN: str = "your_verify_token"
    WHATSAPP_ACCESS_TOKEN: str = "your_long_lived_token"
    WHATSAPP_PHONE_NUMBER_ID: str = "your_phone_number_id"  # from Meta
    DEFAULT_PROJECT_ID: int = 1  # for MVP1: one project

    class Config:
        env_file = ".env"


settings = Settings()