from pydantic import BaseModel

class RenameRequest(BaseModel):
    new_name: str