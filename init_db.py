import sqlite3
import json


def init_db():
    conn = sqlite3.connect('faq.db')
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    """)

    # Загрузка данных
    data = {
  "faqs": [
    {
      "question": "Какие услуги предоставляет компания?",
      "answer": "Мы предоставляем IT-услуги, включая разработку ПО, консалтинг и поддержку инфраструктуры."
    },
    {
      "question": "Какие услуги предоставляет компания",
      "answer": "Наш офис расположен в Москве, Россия, на улице Примерная, дом 10."
    },
    {
      "question": "Как связаться с технической поддержкой?",
      "answer": "Вы можете связаться с нами по электронной почте support@company.com или по телефону +7 (495) 123-45-67."
    },
    {
      "question": "Работаете ли вы с зарубежными клиентами?",
      "answer": "Да, мы предоставляем услуги для клиентов по всему миру."
    },
    {
      "question": "Как долго вы работаете на рынке?",
      "answer": "Компания была основана в 2010 году."
    },
    {
      "question": "Какие языки программирования вы используете?",
      "answer": "Мы работаем с языками, включая Python, JavaScript, Java, C#, и другие."
    },
    {
      "question": "Предоставляете ли вы гарантию на свои услуги?",
      "answer": "Да, мы гарантируем качество наших услуг в рамках заключенного договора."
    },
    {
      "question": "Можно ли получить демонстрацию вашего продукта?",
      "answer": "Да, мы предоставляем бесплатные демонстрации для новых клиентов."
    },
    {
      "question": "Какие сертификаты есть у вашей компании?",
      "answer": "Мы сертифицированы по ISO 9001 и ISO 27001."
    },
    {
      "question": "Какой ваш основной продукт?",
      "answer": "Наш основной продукт — платформа для автоматизации бизнес-процессов."
    },
    {
      "question": "Какова политика конфиденциальности вашей компании?",
      "answer": "Мы строго соблюдаем законы о защите данных, включая GDPR."
    },
    {
      "question": "Могу ли я получить индивидуальное решение для моего бизнеса?",
      "answer": "Да, мы разрабатываем индивидуальные решения под потребности клиентов."
    },
    {
      "question": "Какой у вас режим работы?",
      "answer": "Мы работаем с понедельника по пятницу с 9:00 до 18:00 по московскому времени."
    },
    {
      "question": "Какие отрасли обслуживает ваша компания?",
      "answer": "Мы работаем с клиентами из различных отраслей, включая финансы, здравоохранение, ритейл и производство."
    },
    {
      "question": "Какой минимальный бюджет для начала работы?",
      "answer": "Минимальный бюджет зависит от типа проекта, но обычно составляет 500 000 рублей."
    },
    {
      "question": "Как проходят этапы внедрения ваших решений?",
      "answer": "Этапы включают анализ, проектирование, разработку, тестирование и внедрение."
    },
    {
      "question": "Предоставляете ли вы обучение для пользователей?",
      "answer": "Да, мы проводим тренинги и предоставляем документацию."
    },
    {
      "question": "Есть ли у вас пробный период для услуг?",
      "answer": "Да, для некоторых услуг предусмотрен бесплатный пробный период."
    },
    {
      "question": "Могу ли я получить скидку на услуги?",
      "answer": "Скидки обсуждаются индивидуально в зависимости от масштаба проекта."
    },
    {
      "question": "Какие способы оплаты вы принимаете?",
      "answer": "Мы принимаем банковские переводы, кредитные карты и электронные платежи."
    }
  ]
}

    for item in data['faqs']:
        cursor.execute("INSERT INTO faq (question, answer) VALUES (?, ?)", (item['question'], item['answer']))

    conn.commit()
    conn.close()
    print("База данных успешно инициализирована!")


if __name__ == "__main__":
    init_db()