import sqlite3
from sentence_transformers import SentenceTransformer, util

class FAQSearch:
    def __init__(self, db_path: str):
        self.db_path = 'faq.db'
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Компактная модель для быстрого поиска
        self.questions = []
        self.answers = []
        self.embeddings = []

        # Загрузка данных и создание векторных представлений
        self._load_data()

    def _load_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT question, answer FROM faq")
            faqs = cursor.fetchall()
            self.questions = [question for question, _ in faqs]
            self.answers = [answer for _, answer in faqs]

            # Преобразуем все вопросы в векторное представление
            self.embeddings = self.model.encode(self.questions, convert_to_tensor=True)

        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
        finally:
            conn.close()

    def search(self, query: str):
        try:
            # Преобразуем запрос в векторное представление
            query_embedding = self.model.encode(query, convert_to_tensor=True)

            # Сравниваем запрос с векторами вопросов в базе
            scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
            best_match_idx = scores.argmax().item()
            best_score = scores[best_match_idx].item()
            print(best_score)
            # Пороговое значение для определения релевантности ответа
            if best_score > 0.8:  # Установите подходящий порог (0.5 — разумное значение)
                return {"question": self.questions[best_match_idx], "answer": self.answers[best_match_idx]}

            return {"question": self.questions[best_match_idx], "answer": "Извините, я не знаю ответа на этот вопрос."}

        except Exception as e:
            print(f"Ошибка при поиске: {e}")
            return {"question": None, "answer": f"Произошла ошибка при поиске: {e}"}
