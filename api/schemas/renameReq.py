from pydantic import BaseModel 

class RenameRequest(BaseModel):
    name: str