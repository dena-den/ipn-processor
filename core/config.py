from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "ipn_processor"
    CRYPTOCURRENCY_TOKEN: str
    DB_URL: str
    PORT: int

    class Config:
        case_sensitive = True


settings: Settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
