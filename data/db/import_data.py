import pandas as pd
from sqlalchemy import create_engine
import os
from db_config import DATABASE_CONFIG


engine = create_engine(f"postgresql+psycopg2://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}")
file_path = r'C:\Users\rafae\OneDrive\Desktop\projects\Client_Churn_analyzer\data\raw\Telco-Customer-Churn.csv'
df = pd.read_csv(file_path)

df.columns = [col.lower() for col in df.columns] 
df['totalcharges'] = pd.to_numeric(df['totalcharges'], errors='coerce').fillna(0)

df.to_sql(
    name='customers',
    con=engine,
    if_exists='replace',  
    index=False,
    method='multi'
)

print(f"Успешно импортировано {len(df)} записей в таблицу customers")