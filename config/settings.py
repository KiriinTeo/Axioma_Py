from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):

    ENV: str = "development"                    # configuração pro ambiente
    DEBUG: bool = True

    SECRET_KEY: str                             # pra segurança
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
                                           
    DATABASE_URL: str | None = None             # pro banco de dados E fallback/local

    ORACLE_USER: str | None = None              # dados pra Oracle OCI
    ORACLE_PASSWORD: str | None = None                        
    ORACLE_DSN: str | None = None                               
    ORACLE_WALLET_PATH: str | None = None                  

    model_config = {
        "env_file": os.getenv("ENV_FILE", ".env"),       # adaptação para separar .env de dev e prod
        "env_file_encoding": "utf-8",
    }

    @property
    def database_url(self) -> str:
        if self.ENV == "production" and self.ORACLE_DSN:
            return (
                f"oracle+oracledb://{self.ORACLE_USER}:"
                f"{self.ORACLE_PASSWORD}@{self.ORACLE_DSN}"
            )
        elif self.DATABASE_URL:
            return self.DATABASE_URL
        else:
            return "sqlite:///./test.db"  # fallback/local

settings = Settings()
