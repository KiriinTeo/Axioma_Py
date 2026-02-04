from pydantic import BaseModel
from typing import Any


class FilterRequest(BaseModel):
    dataset_id: str
    column: str
    operator: str
    value: Any
