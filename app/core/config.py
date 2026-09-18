from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NovaBite"
    app_env: str = "development"
    debug: bool = True

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "novabite"
    postgres_user: str = "novabite"
    postgres_password: str = "change_me"

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "novabite"

    faiss_index_path: str = "./faiss_index"
    embedding_model_name: str = "findme"
    GROQ_API_KEY: str = "YOUR_API_KEY"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()