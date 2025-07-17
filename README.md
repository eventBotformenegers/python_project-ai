# OpenAI + ManyChat + Render Ассистент

## Быстрый старт

### 1. Локальный запуск

```sh
export OPENAI_API_KEY=sk-...ваш_ключ...
uvicorn main:app --reload
```

### 2. Деплой на Render

1. Залейте проект на GitHub.
2. На [render.com](https://render.com/) создайте новый Web Service:
   - Укажите репозиторий.
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`
   - В Environment добавьте переменную `OPENAI_API_KEY` с вашим ключом.
   - Порт: `10000` (или стандартный Render PORT)
3. Render сам соберёт и запустит сервис.

### 3. Интеграция с ManyChat

1. В ManyChat создайте Custom Integration → Webhook.
2. В качестве URL укажите:
   ```
   https://ВАШ_ДОМЕН.onrender.com/manychat-webhook
   ```
3. Передавайте в теле запроса JSON вида:
   ```json
   {
     "user_id": "123",
     "message": "Привет!"
   }
   ```
4. В ответ получите JSON с ответом ассистента.

---

## Хранение истории чатов
Все сообщения и ответы сохраняются в SQLite (`chat_history.db`).

---

## Смена модели OpenAI
По умолчанию используется `gpt-4o` (GPT-4.1 mini). Можно изменить в main.py.

---

## Вопросы? 
Пишите! 