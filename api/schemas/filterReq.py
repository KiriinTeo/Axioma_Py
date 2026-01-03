from pydantic import BaseModel # pydantic baseModel é mais usado pra dados estruturados, lembrar disso

class FilterRequest(BaseModel):
    dataset_id: int
    column: str
    operator: str
    value: str
