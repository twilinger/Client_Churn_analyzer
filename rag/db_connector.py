from sqlalchemy import create_engine
import pandas as pd
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent 
sys.path.append(str(project_root))

from data.db.db_config import DATABASE_CONFIG

class DBConnector:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql+psycopg2://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
            f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
        )
    
    def get_churn_data(self, query: str) -> pd.DataFrame:
        return pd.read_sql(query, self.engine)
