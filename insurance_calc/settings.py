import enum
import multiprocessing
import secrets
from pathlib import Path
from tempfile import gettempdir
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    secret_key: str = secrets.token_urlsafe(32)
    algorithm: str = "HS256"

    host: str = "127.0.0.1"
    port: int = 8000

    # Current environment
    environment: str = "dev"

    # Mapping for environment-specific settings
    _env_config: dict[str, Any] = {
        "dev": {"reload": True, "workers_count": 1},
        "prod": {
            "reload": False,
            "workers_count": multiprocessing.cpu_count()
            if multiprocessing.cpu_count() <= 8
            else 8,
        },
    }

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "insurance_calc"
    db_pass: str = "insurance_calc"
    db_base: str = "admin"
    db_echo: bool = False

    # Variables for Redis
    redis_host: str = "insurance-calc-redis"
    redis_port: int = 6379
    redis_user: str | None = None
    redis_pass: str | None = None
    redis_base: int | None = None

    access_token_expire_minutes: int = 10080
    admin_email: str = "admin@admin.com"
    admin_password: str = "root"
    kafka_bootstrap_servers: list[str] = ["insurance-calc-kafka:9092"]

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )

    @property
    def reload(self) -> bool:
        """
        Reload the application on changes.

        :return: reload flag.
        """
        return self._env_config[self.environment].get("reload", False)

    @property
    def workers_count(self) -> int:
        """
        Number of worker processes (only for gunicorn).

        :return: number of worker processes.
        """
        return self._env_config[self.environment].get("workers_count", 1)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="INSURANCE_CALC_",
        env_file_encoding="utf-8",
    )


settings = Settings()
