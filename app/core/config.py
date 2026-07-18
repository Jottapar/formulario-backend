from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- App ---
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str

    # --- Database (piezas sueltas del .env) ---
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    # --- Security (para cuando lleguemos a JWT) ---
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # La DATABASE_URL se arma a partir de las piezas
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Le decimos a Pydantic de dónde leer las variables
    model_config = SettingsConfigDict(env_file=".env")


# Una sola instancia que toda la app importará
settings = Settings()