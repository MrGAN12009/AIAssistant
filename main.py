import time

import telebot
from vector_search import FAQSearch
import requests

# Укажите ваш токен Telegram-бота
TOKEN = "5480073812:AAFAJeBEU8VEyrBqRLRznD_dzhDxI82-ju0"
bot = telebot.TeleBot(TOKEN)

# Путь к базе данных
DATABASE_PATH = "faq.db"

# Инициализация поисковой системы
search_engine = FAQSearch(DATABASE_PATH)


#функция поиска чекрез api запрос к gen-api
def req(question):
    # Заголовки для авторизации и указания формата данных
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer sk-udLseozVcSNZtAH7qO58d82hc5O3luNZDiT59DoOS6t8Y8l0FVNqblFu24OW'
    }

    # URL эндпоинта API
    url_endpoint = "https://api.gen-api.ru/api/v1/networks/gpt-4o"





    # Входные данные для запроса
    input_data = {
        "messages": [
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"ИЗ СПИСКА ВОПРОСОВ ВЫБЕРИ НАИБОЛЛЕ ПОДХОДЯЩИЙ. СПИСОК:Какие услуги предоставляет компания?, Какие услуги предоставляет компания, Как связаться с технической поддержкой?, Работаете ли вы с зарубежными клиентами?, Как долго вы работаете на рынке?, Какие языки программирования вы используете?, Предоставляете ли вы гарантию на свои услуги?, Можно ли получить демонстрацию вашего продукта?, Какие сертификаты есть у вашей компании?, Какой ваш основной продукт?, Какова политика конфиденциальности вашей компании?, Могу ли я получить индивидуальное решение для моего бизнеса?, Какой у вас режим работы?, Какие отрасли обслуживает ваша компания?, Какой минимальный бюджет для начала работы?, Как проходят этапы внедрения ваших решений?, Предоставляете ли вы обучение для пользователей?, Есть ли у вас пробный период для услуг?, Могу ли я получить скидку на услуги?, Какие способы оплаты вы принимаете?. ВОПРОС - {question}. ЕСЛИ ВОПРОСА НЕТ В ЗАДАННОМ СПИСКЕ ТО ОТВЕТЬ ВОПРОСОМ ДЛЯ УТОЧНЕНИЯ"

                }
            ]
        }
        ]
    }

    # Выполнение POST-запроса для инициации задачи
    response = requests.post(url_endpoint, json=input_data, headers=headers)
    if response.status_code == 200:
        task_info = response.json()
        task_id = task_info.get("request_id")  # Предполагается, что API возвращает task_id
        print(response.json())
        if not task_id:
            print("Не удалось получить task_id")
            exit()

        # URL для проверки статуса задачи
        status_url = f"https://api.gen-api.ru/api/v1/request/get/{task_id}"

        print("Задача отправлена, task_id:", task_id)

        # Long-polling: проверка статуса задачи
        while True:
            status_response = requests.get(status_url, headers=headers)
            if status_response.status_code == 200:
                status_data = status_response.json()
                status = status_data.get("status")
                if status == "success":
                    return status_data.get("result")
                    break
                elif status == "failed":
                    return status_data.get("result")
                    break
                else:
                    print("Задача в процессе выполнения, ожидаем...")
            else:
                print(f"Ошибка при проверке статуса: {status_response.status_code}, {status_response.text}")

            # Ожидание перед повторной проверкой
            time.sleep(5)
    else:
        return "Ошибка на стороне севрера"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Обрабатывает команды /start и /help.
    """
    bot.reply_to(message, (
        "Привет! Я ваш ИИ-консультант. Задайте мне вопрос, и я постараюсь помочь.\n"
        "Примеры вопросов:\n"
        "- Какие услуги предоставляет компания?\n"
        "- Где находится офис компании?"
    ))

@bot.message_handler(func=lambda message: True)
def handle_query(message):
    """
    Обрабатывает текстовые сообщения от пользователя.
    """
    user_query = message.text  # Получаем сообщение пользователя
    result = search_engine.search(user_query)  # Выполняем поиск

    if result['answer'] == "Извините, я не знаю ответа на этот вопрос.":
        result = search_engine.search(req(user_query))
        bot.reply_to(message, f"Вопрос: {result['question']}\nОтвет: {result['answer']}")

    ##search_engine работает криво, необходимо дообучение для точной отработки
    elif result['answer'] != "Извините, я не знаю ответа на этот вопрос.":
        bot.reply_to(message, f"Вопрос: {result['question']}\nОтвет: {result['answer']}")
    else:
        bot.reply_to(message, "Извините, я не знаю ответа на этот вопрос. Попробуйте задать другой вопрос.")


# Запуск бота
if __name__ == "__main__":
    print("Бот запущен и готов к работе...")
    bot.infinity_polling()
