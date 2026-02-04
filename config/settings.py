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
    TNS_ADMIN: str | None = None
    WALLET_PASSWORD: str | None = None          # senha do wallet se necessário                                              

    model_config = {
        "env_file": os.getenv("ENV_FILE", ".env"),       # adaptação para separar .env de dev e prod
        "env_file_encoding": "utf-8",
    }

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return "sqlite:///./test.db"  # fallback para dev

settings = Settings()
