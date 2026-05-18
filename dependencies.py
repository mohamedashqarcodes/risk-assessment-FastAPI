from fastapi import Depends, HTTPException, status
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_key:     str
    app_name:    str
    max_risk:    str = "HIGH"
    model_config = SettingsConfigDict(env_file=".env")

settings=Settings()

def get_settings()->Settings:
    return settings

def verify_api_key(api_key: str) -> str: #why cannot use field validator
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return api_key
