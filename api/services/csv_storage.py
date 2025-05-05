import pandas as pd
from typing import Optional

csv_memory_store: dict[str, pd.DataFrame] = {}

def save_csv(session_id: str, df: pd.DataFrame):
    csv_memory_store[session_id] = df

def get_csv(session_id: str) -> Optional[pd.DataFrame]:
    return csv_memory_store.get(session_id)