# План разработки LLM-core (MVP)

**Цель дня**: Получить рабочую базовую версию LLM-core, которая принимает минимальные параметры (`topic`, `specialty`, `level`, `num_questions`) и возвращает валидный структурированный JSON-тест по нефтегазовой тематике.

## Общая информация

- **Время**: ~8–10 часов (реалистично для одного человека)
- **Технологии**: Python, Pydantic, LangChain (или Instructor), LLM (OpenAI / Anthropic / Groq)
- **Результат**: Рабочий скрипт + CLI для генерации тестов

---

## Пошаговый план на 1 день

### Подготовка (30–45 минут)

1. Создать проект:
   ```bash
   mkdir llm-core && cd llm-core
   python -m venv venv
   source venv/bin/activate  # или venv\Scripts\activate на Windows
   pip install pydantic langchain langchain-openai python-dotenv typer
   ```

2. Создать структуру папок:
   ```
   llm-core/
   ├── core/
   │   ├── __init__.py
   │   ├── models.py          # Pydantic модели
   │   ├── prompts.py         # Все промпты
   │   └── generator.py       # Основная логика
   ├── tests/
   │   └── test_basic.py
   ├── main.py                # CLI
   ├── .env
   └── README.md
   ```

3. Настроить `.env` с `OPENAI_API_KEY` (или аналогичным)

---

### Этап 1: Модели данных (20–30 минут)

- В `core/models.py` создать:
  - `GenerationInput`
  - `Question`
  - `GeneratedTest`

Сделать схемы максимально простыми, но достаточными для нефтегазовой отрасли.

---

### Этап 2: Промпты (40–50 минут)

- В `core/prompts.py`:
  - `SYSTEM_PROMPT` — роль senior petroleum engineer + HSE + JSON only
  - `USER_PROMPT_TEMPLATE` — с плейсхолдерами для topic, specialty и т.д.
  - `JUDGE_PROMPT_TEMPLATE` — простая рубрика оценки

---

### Этап 3: Основная функция генерации (1.5–2 часа)

- В `core/generator.py` реализовать `generate_test(input_data: GenerationInput) -> GeneratedTest`
- Последовательность внутри функции:
  1. Preprocessing (расширение параметров)
  2. Сборка промпта
  3. Вызов LLM с `with_structured_output(GeneratedTest)`
  4. Базовая обработка ошибок

**Совет**: Сначала сделай версию **без Judge**, чтобы быстро увидеть результат.

---

### Этап 4: Validation + Judge + Refinement (1–1.5 часа)

- Добавить функцию `evaluate_test_quality(test: GeneratedTest)`
- Реализовать простой Refinement Loop (1–2 попытки)
- Если judge_score низкий — добавить critique в следующий промпт

---

### Этап 5: CLI и Тестирование (1–1.5 часа)

- В `main.py` сделать удобный CLI с помощью `typer`:
  ```bash
  python main.py generate --topic "Контроль скважины" --specialty "Инженер по бурению" --level Senior --num 6
  ```

- Протестировать на 3–4 разных сценариях:
  - Well Control (Senior)
  - Процессная безопасность (Middle)
  - Бурение (Junior)

---

### Этап 6: Финализация и Документация (40–60 минут)

1. Добавить базовый logging
2. Написать README.md с:
   - Описанием проекта
   - Примерами запуска
   - Ограничениями текущей версии
3. Сохранять сгенерированные тесты в JSON-файлы
4. Финальное тестирование всего flow

---

## Итоговый результат за 1 день

- Рабочая базовая версия LLM-core
- Генерация JSON-теста по 4 параметрам
- Поддержка MCQ и Scenario вопросов
- Базовый Judge + refinement
- CLI для быстрого тестирования

---

## Что отложить на следующие дни

- Полноценный RAG
- FastAPI endpoint
- Semantic cache
- Multi-agent workflow
- Админ-панель / UI
- Метрики и мониторинг
- Fine-tuning
