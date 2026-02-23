from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost:5432/chair_recommender"
    anthropic_api_key: str = ""
    youtube_api_key: str = ""
    admin_password: str = "admin"
    session_secret: str = "change-me-in-production"
    frontend_url: str = "http://localhost:3000"

    model_config = {"env_file": ".env"}


settings = Settings()
