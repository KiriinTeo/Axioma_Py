from datetime import datetime, timedelta
from jose import jwt # grande john doe

SECRET_KEY = "MUDAR_PARA_UMA_CHAVE_SECRETA_SEGURA" #kkkkkkkkkk isso ai
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
