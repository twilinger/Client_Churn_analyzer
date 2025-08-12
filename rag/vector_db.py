
import chromadb
from sentence_transformers import SentenceTransformer
from rag.db_connector import DBConnector

class VectorDB:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = chromadb.PersistentClient(path="data/rag_db")
        self.collection = self.client.get_or_create_collection("churn_knowledge")
        self.db = DBConnector()
        
    def _load_from_db(self):
        """Загружает ключевые данные из серверной БД"""
        query = """
            SELECT 
                customer_id,
                contract || ' ' || paymentmethod || ' ' || 
                CAST(monthlycharges AS TEXT) AS document_content
            FROM customers
            WHERE churn = 'Yes'
            LIMIT 1000  # Для теста
        """
        df = self.db.get_churn_data(query)
        
        # Добавляем в векторную БД
        self.collection.add(
            ids=df["customer_id"].astype(str).tolist(),
            documents=df["document_content"].tolist()
        )
    
    def query(self, question: str, top_k: int = 3) -> list[str]:
        """Поиск релевантных данных"""
        if len(self.collection.get()["ids"]) == 0:
            self._load_from_db()
            
        results = self.collection.query(
            query_texts=[question],
            n_results=top_k
        )
        return results["documents"][0]