### AQSANA.KZ  

**AQSANA.KZ** — интеллектуальный конвертор валют, разработанный как финальный проекта на курсе *Python Backend*.  

---
#### Почему AQSANA?
> Название **AQSANA** образовано от двух казахских слов:  
> **"Ақша"** — деньги и **"Сана"** — разум, подсчёт.  
> Это философия проекта:  
> **Считай с умом. Обменивай с разумом.**
---

#### Функциональность
1. Получение актуальных курсов валют из официального API [Нацбанк РК](https://nationalbank.kz)
2. Конвертация валют  
3. История конвертаций  
4. Избраннымые валютные пары
5. Добавление, редактирование и удаление валют  
5. Прогноз курса валют (KZT → USD):
   - Модель линейной регрессии (`scikit-learn`)
   - Прогноз от ИИ (OpenAI GPT-3.5)

---


#### Технологии
|--------------------------------------------------------|
| Python, Django    | Backend                            |
| SQLite            | База данных для разработки         |
| requests, lxml    | Загрузка и парсинг XML с НБК       |
| scikit-learn      | ML линейного прогноза              |
| numpy             | Вспомогательные расчёты            |
| OpenAI API        | ИИ-прогноз валютных курсов         |
| python-dotenv     | Хранение API-ключей и переменных   |
| Docker            | Контейнеризация проекта            |

---

#### Версия
[CHANGELOG.md](./CHANGELOG.md) истории изменении