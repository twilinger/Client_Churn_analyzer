import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from db_config import DATABASE_CONFIG

def generate_faq_from_db():
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
            f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
        )
        analysis_queries = {
            "Общая статистика оттока": """
                SELECT 
                    ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_rate,
                    AVG(monthlycharges) AS avg_monthly_payment,
                    AVG(tenure) AS avg_tenure_months
                FROM customers
            """,
            
            "Топ-5 факторов оттока": """
                SELECT 
                    paymentmethod, 
                    ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_rate
                FROM customers
                GROUP BY paymentmethod
                ORDER BY churn_rate DESC
                LIMIT 5
            """
        }

        md_content = [
            "# Анализ оттока клиентов",
            f"*Сгенерировано {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        ]

        for section, query in analysis_queries.items():
            df = pd.read_sql(query, engine)
            md_content.append(f"\n## {section}\n")
            md_content.append(df.to_markdown(index=False))

        os.makedirs("data/knowledge", exist_ok=True)
        with open("data/knowledge/churn_faq.md", "w", encoding="utf-8") as f:
            f.write("\n".join(md_content))

        print("Файл faq успешно создан")
        return True

    except Exception as e:
        print(f"Ошибка генерации faq {e}")
        return False

if __name__ == "__main__":
    generate_faq_from_db()