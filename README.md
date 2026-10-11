# product-roadmap-ai
Описание: AI-платформа управления продуктовым роадмапом. Приоритизация фич (RICE, WSJF, Kano), прогноз сроков через Monte Carlo, симуляция релизов, дашборд для стейкхолдеров, интеграция с Jira/Linear.  Стек: Python 3.11, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Celery, Redis, scikit-learn, Streamlit, Docker, GitHub Actions.

# product-roadmap-ai

AI-платформа управления продуктовым роадмапом.

## Возможности
- Приоритизация RICE, WSJF, Kano
- Комбинированный скоринг
- Monte Carlo симуляция сроков релиза
- Интеграция с Jira и Linear
- Streamlit-дашборд

## Быстрый старт

cp .env.example .env
docker-compose up --build

API: http://localhost:8000/docs
Dashboard: http://localhost:8501

## Пример

curl -X POST http://localhost:8000/api/features \
  -H "Content-Type: application/json" \
  -d '{"title":"AI search","reach":5000,"impact":2.0,
       "confidence":0.8,"effort":5.0}'

curl http://localhost:8000/api/prioritize/rice

## Лицензия
MIT
