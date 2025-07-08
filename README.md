# 🍽️ Restaurant Project – REST API for Online Food Orders

**TL;DR:** Django + DRF = API, Celery + Redis = фонові листи, Docker = однією командою піднялось усе.

> “Ти замовляєш – ми готуємо – Celery шепче Redis’у – лист падає в інбокс. Шеф довольний.” 😎

---

## 📌 Основні можливості

| Функція                    | Опис                                                                                  |
| -------------------------- |---------------------------------------------------------------------------------------|
| **JWT‑аутентифікація**     | Реєстрація, логін, refresh‑токени (`djangorestframework‑simplejwt`)                   |
| **Меню**                   | CRUD страв (адмінка та Read‑only API `/api/menu/`)                                    |
| **Замовлення**             | Користувач створює замовлення з кількох страв, час доставки ≥ 30 хв                   |
| **Email‑нотифікації**      | Celery відправляє лист у точний момент доставки                                       |
| **OpenAPI 3 + Swagger**    | Жива документація на `/api/docs/`, схема на `/api/schema/`                            |
| **Docker‑композ**          | `web` (Django) + `db` (Postgres) + `redis` + `worker` (Celery) + `beat` (Celery Beat) |
| **80 %+ покриття тестами** | `tests` / `test_api` / `coverage`                                                     |
| **CI pipeline**            | GitHub Actions → `isort`, `flake8`, `mypy`, тести, coverage badge                     |

---

## 🛠️ Стек

* **Python 3.12**
* **Django 5**
* **Django REST Framework**
* **PostgreSQL** – основна БД
* **Redis** – брокер задач Celery
* **drf‑spectacular** – автоген OpenAPI 3
* **pytest** – тести
* **Docker + docker‑compose** – прод і розробка
* **GitHub Actions** – CI (lint → type‑check → tests)

---

## ⚙️ Швидкий старт (локально, без Docker)

```bash
git clone https://github.com/Yurashpak887/restaurant_project.git
cd restaurant_project

# 1. Віртуальне середовище
python -m venv .venv
source .venv/bin/activate

# 2. Залежності
pip install -r requirements.txt

# 3. Міграції + суперюзер
python manage.py migrate
python manage.py createsuperuser

# 4. Redis (у новій вкладці)
redis-server

# 5. Celery worker (у ще одній)
celery -A restaurant_project worker -l info

# 6. Запускаємо Django
python manage.py runserver
```

Відкрий `http://127.0.0.1:8000/api/docs/` — там Swagger UI 🦄

---

## 🐳 Швидкий старт із Docker

```bash
docker-compose up --build
```

* Django: `http://localhost:8000/`
* Swagger UI: `http://localhost:8000/api/docs/`
* Адмінка: `http://localhost:8000/admin/`

---

## 🔐 Перемінні середовища

Створи `.env` (або налаштуй у CI/сервері):

```dotenv
DJANGO_SECRET_KEY=super‑secret
POSTGRES_DB=restaurant
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=mail@example.com
EMAIL_HOST_PASSWORD=pass
```

---

## 🛣️ API ендпоінти (коротко)

| Метод | URL                   | Опис                         |
| ----- | --------------------- | ---------------------------- |
| POST  | `/api/token/`         | Отримати JWT pair            |
| POST  | `/api/token/refresh/` | Оновити access‑токен         |
| GET   | `/api/menu/`          | Список страв (public)        |
| GET   | `/api/menu/{id}/`     | Одна страва                  |
| GET   | `/api/orders/`        | Список замовлень користувача |
| POST  | `/api/orders/`        | Створити замовлення          |
| …     | …                     | Див. Swagger UI / ReDoc      |

---

## 🔄 Тести та якість коду

```bash
# Лінтери
isort . && flake8 . && mypy .

# Запуск тестів
pytest

# Покриття
coverage run -m pytest
coverage html  # створить htmlcov/index.html
```

---

## 🚀 CI / CD

`.github/workflows/lint.yml` запускає:

1. **isort** – перевірка/сортування імпортів
2. **flake8** – стиль PEP8 + суворі правила
3. **mypy** – статична перевірка типів
4. **pytest + coverage** – тести (фейл < 80 %)

---

## 🧩 Архітектура Celery

```text
[Django API] -- publish --> [Redis] <-- consume -- [Celery Worker]
                                   ↑
                      schedule --  |  -- periodic tasks
                             [Celery Beat]
```

* Коли користувач створює замовлення, Django ставить задачу `send_order_email` у Redis з `eta=<delivery_time>`.
* Celery Worker спить до потрібного часу, а потім відправляє email.

---

## 📚 Корисні команди Makefile *(для лінивих)*

```make
make up        # docker-compose up
make lint      # isort + flake8 + mypy
make test      # pytest + coverage
make worker    # celery -A restaurant_project worker -l info
make beat      # celery -A restaurant_project beat -l info
```

---





> **Developed with by [@Yurashpak887](https://github.com/Yurashpak887)**
