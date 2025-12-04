import pandas as pd
from fastapi import HTTPException

def load_csv(path: str):
    try:
        return pd.read_csv(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading CSV {path}: {e}")
    
def validate_agent_id(agent_id: str):
    if not agent_id or not agent_id.startswith("agent-"):
        raise HTTPException(status_code=401, detail="Invalid or missing Agent ID")