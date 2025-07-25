"""
EMSP Configuration Management
============================

This module provides configuration management for the OCPI-compliant EMSP backend.
It extends the default py_ocpi settings with EMSP-specific configurations and
provides environment variable support for production deployments.

Configuration includes:
- OCPI protocol settings
- EMSP-specific parameters
- Database configuration
- Security settings
- CORS configuration
- Logging configuration
"""

import os
from typing import List, Optional

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

from pydantic import AnyHttpUrl, validator


class EMSPSettings(BaseSettings):
    """
    EMSP Configuration Settings

    This class defines all configuration parameters for the EMSP backend.
    Settings can be overridden using environment variables.
    """

    # Application Settings
    PROJECT_NAME: str = "OCPI EMSP Backend"
    VERSION: str = "2.2.1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # OCPI Protocol Settings
    OCPI_HOST: str = "localhost:8000"
    OCPI_PREFIX: str = "ocpi/emsp/2.2.1"
    PUSH_PREFIX: str = "push"
    PROTOCOL: str = "http"  # Use "https" in production

    # EMSP Identity Settings
    COUNTRY_CODE: str = "US"
    PARTY_ID: str = "EMS"  # 3-character EMSP identifier

    # Authentication Settings
    NO_AUTH: bool = False  # Set to True only for development/testing
    TOKEN_EXPIRY_HOURS: int = 24

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1

    # CORS Settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000",
    ]

    # Database Settings (for production use)
    DATABASE_URL: Optional[str] = None
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Redis Settings (for caching and sessions)
    REDIS_URL: Optional[str] = None
    REDIS_PASSWORD: Optional[str] = None

    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # OCPI Timing Settings
    COMMAND_AWAIT_TIME: int = 30  # seconds
    GET_ACTIVE_PROFILE_AWAIT_TIME: int = 30  # seconds

    # OCPI Behavior Settings
    TRAILING_SLASH: bool = True
    CI_STRING_LOWERCASE_PREFERENCE: bool = True

    # Security Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # External Service URLs (for production integration)
    CPO_ENDPOINTS: List[str] = []  # List of CPO endpoint URLs
    NOTIFICATION_WEBHOOK_URL: Optional[str] = None

    # Feature Flags
    ENABLE_HTTP_PUSH: bool = True
    ENABLE_WEBSOCKET_PUSH: bool = False
    ENABLE_METRICS: bool = True
    ENABLE_HEALTH_CHECKS: bool = True

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """Assemble CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("PROTOCOL")
    def validate_protocol(cls, v):
        """Validate protocol is http or https."""
        if v not in ["http", "https"]:
            raise ValueError("Protocol must be 'http' or 'https'")
        return v

    @validator("COUNTRY_CODE")
    def validate_country_code(cls, v):
        """Validate country code is 2 characters."""
        if len(v) != 2:
            raise ValueError("Country code must be exactly 2 characters")
        return v.upper()

    @validator("PARTY_ID")
    def validate_party_id(cls, v):
        """Validate party ID is 3 characters."""
        if len(v) != 3:
            raise ValueError("Party ID must be exactly 3 characters")
        return v.upper()

    @property
    def base_url(self) -> str:
        """Get the base URL for the EMSP service."""
        return f"{self.PROTOCOL}://{self.OCPI_HOST}"

    @property
    def ocpi_base_url(self) -> str:
        """Get the OCPI base URL."""
        return f"{self.base_url}/{self.OCPI_PREFIX}"

    @property
    def database_url_sync(self) -> Optional[str]:
        """Get synchronous database URL."""
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
        return None

    @property
    def database_url_async(self) -> Optional[str]:
        """Get asynchronous database URL."""
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        return None

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create settings instance
settings = EMSPSettings()


def get_settings() -> EMSPSettings:
    """
    Get the settings instance.

    Returns:
        EMSPSettings instance
    """
    return settings


def print_settings_summary():
    """Print a summary of current settings for debugging."""
    print("=" * 50)
    print("EMSP Configuration Summary")
    print("=" * 50)
    print(f"Project: {settings.PROJECT_NAME}")
    print(f"Version: {settings.VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Base URL: {settings.base_url}")
    print(f"OCPI URL: {settings.ocpi_base_url}")
    print(f"Country Code: {settings.COUNTRY_CODE}")
    print(f"Party ID: {settings.PARTY_ID}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Authentication: {'Disabled' if settings.NO_AUTH else 'Enabled'}")
    print(f"CORS Origins: {len(settings.BACKEND_CORS_ORIGINS)} configured")
    print(f"Database: {'Configured' if settings.DATABASE_URL else 'Not configured'}")
    print(f"Redis: {'Configured' if settings.REDIS_URL else 'Not configured'}")
    print("=" * 50)


if __name__ == "__main__":
    # Print settings when run directly
    print_settings_summary()
