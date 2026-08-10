from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "DataPilot AI"
    app_env: str = "development"
    debug: bool = True

    openai_api_key: str | None = None

    max_file_size_mb: int = 100

    raw_data_dir: str = "data/raw"
    processed_data_dir: str = "data/processed"
    output_data_dir: str = "data/outputs"

    reports_dir: str = "reports"
    visualizations_dir: str = "visualizations"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def max_file_size_bytes(self) -> int:
        """Return maximum upload size in bytes."""
        return self.max_file_size_mb * 1024 * 1024

    @property
    def project_root(self) -> Path:
        """Return the root directory of the project."""
        return Path(__file__).resolve().parent.parent

    def ensure_directories(self) -> None:
        """Create required application directories if they don't exist."""

        directories = [
            self.raw_data_dir,
            self.processed_data_dir,
            self.output_data_dir,
            self.reports_dir,
            self.visualizations_dir,
        ]

        for directory in directories:
            path = self.project_root / directory
            path.mkdir(parents=True, exist_ok=True)


settings = Settings()