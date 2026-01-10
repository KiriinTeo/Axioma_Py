from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    ENV: str = "development"                    # configuração pro ambiente
    DEBUG: bool = True

    SECRET_KEY: str                             # pra segurança
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
                                           
    DATABASE_URL: str                           # pro banco de dados

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()
