# settings.py

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_THIS_FILE = Path(__file__).resolve()
ROOT_DIR = _THIS_FILE.parent  # settings.py -> root
DEFAULT_ENV = ROOT_DIR / ".env"  # root/.env
ENV_FILE = str(DEFAULT_ENV) if DEFAULT_ENV.exists() else ".env"

if not DEFAULT_ENV.exists():
    print(f".env file not found at: {DEFAULT_ENV}")


class Settings(BaseSettings):
    # region smtpSettings

    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_HOST: str = "smtp.yandex.ru"
    SMTP_PORT: int = 465

    # endregion smtpSettings

    # region emailSettings

    EMAIL_SUBJECT: str = "Доступ к LLM Proxy — API-ключ и документация"

    # endregion emailSettings

    # region pathSettings

    XLS_PATH: Path = ROOT_DIR / "recipients.xls"
    CSV_PATH: Path = ROOT_DIR / "recipients.csv"
    TEMPLATE_PATH: Path = ROOT_DIR / "email_template.md"

    # endregion pathSettings

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
