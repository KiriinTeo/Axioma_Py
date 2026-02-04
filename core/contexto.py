from dataclasses import dataclass
import pandas as pd
from typing import Optional, Dict, Any

@dataclass
class DatasetContext:
    name: str
    dataframe: pd.DataFrame
    metadata: Optional[Dict[str, Any]] = None
    dataset_id: Optional[int] = None

    def shape(self):
        return self.dataframe.shape

    def columns(self):
        return self.dataframe.columns.tolist()
