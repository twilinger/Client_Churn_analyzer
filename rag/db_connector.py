from sqlalchemy import create_engine
import pandas as pd
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent 
sys.path.append(str(project_root))

from db.db_config import DATABASE_CONFIG

class DBConnector:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql+psycopg2://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
            f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
        )
    def check_columns(self):
        columns = pd.read_sql(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name = 'customers'", 
        self.engine
    )
        print("Столбцы таблицы customers:")
        print(columns)
    
    def get_churn_data(self, query: str) -> pd.DataFrame:
        return pd.read_sql(query, self.engine)
    