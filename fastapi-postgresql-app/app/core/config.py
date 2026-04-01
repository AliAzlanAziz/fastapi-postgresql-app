from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Option A: single URL (takes precedence if set)
    DATABASE_URL: str | None = None

    # Option B: individual components (used if DATABASE_URL is not set)
    POSTGRES_DB: str = "app"
    POSTGRES_USER: str = "app"
    POSTGRES_PASSWORD: str = "change-me"
    POSTGRES_HOST: str = "localhost"   # use "db" if your app runs in Docker alongside Postgres
    POSTGRES_PORT: int = 5432
    
    # Auth
    SECRET_KEY: str = "change-me"              # set in .env for production!
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",          # read vars exactly as named above
        extra="ignore",         # ignore unknown/extra env keys instead of erroring
        case_sensitive=False,   # allow lowercase keys like postgres_db
    )

    @property
    def db_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()
