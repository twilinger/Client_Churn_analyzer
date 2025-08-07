from sqlalchemy import create_engine, text
from db_config import DATABASE_CONFIG  # Импорт конфига

def test_connection():
    try:
        # Формируем строку подключения (пример для PostgreSQL)
        connection_str = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
        
        # Подключаемся к БД
        engine = create_engine(connection_str)
        with engine.connect() as conn:
            # Выполняем тестовый запрос (например, проверяем список таблиц)
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
            tables = [row[0] for row in result]
            
            print("✅ Подключение успешно!")
            print(f"Найдены таблицы: {tables}")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

if __name__ == "__main__":
    test_connection()