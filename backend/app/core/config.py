from pydantic_settings import BaseSettings


# Define a Settings class that inherits from BaseSettings to handle
# configuration from environment variables
class Settings(BaseSettings):
    # Type hints for each environment variable that will be read
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    DATABASE_URL: str

    # Configuration class for Pydantic to specify how to read environment
    # variables
    class Config:
        env_file = ".env"


# Instantiate the Settings class to load the configuration
settings = Settings()
