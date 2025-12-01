"""Configuration module for IM connector, including settings and enums."""

import logging
from enum import Enum
from functools import lru_cache
from typing import Annotated, Literal

from fastapi import Depends
from pydantic import AnyHttpUrl, BeforeValidator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevelEnum(int, Enum):
    """Enumeration of supported logging levels."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def get_level(value: int | str | LogLevelEnum) -> int:
    """Convert a string, integer, or LogLevelEnum value to a logging level integer.

    Args:
        value: The log level as a string (case-insensitive), integer, or LogLevelEnum.

    Returns:
        int: The corresponding logging level integer.

    """
    if isinstance(value, str):
        return LogLevelEnum.__getitem__(value.upper())
    return value


class Settings(BaseSettings):
    """Configuration settings for the IM connector."""

    IM_HOST: Annotated[
        str,
        Field(default="", description="IM host URL to connect to the IM API"),
    ]
    ALLOWED_ORIGINS: Annotated[
        list[AnyHttpUrl] | Literal["*"],
        Field(default_factory=list, description="List of allowed CORS origins"),
    ]
    LOG_LEVEL: Annotated[
        LogLevelEnum,
        Field(default=LogLevelEnum.INFO, description="Logs level"),
        BeforeValidator(get_level),
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# LRU-cached getter
@lru_cache
def get_settings() -> Settings:
    """Get the application settings, cached for performance."""
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
