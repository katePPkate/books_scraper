# Books Scraper

Проект для автоматического сбора данных о книгах с сайта [Books to Scrape](http://books.toscrape.com/).

## Цель

Разработать систему парсинга для сбора полной информации о книгах со всех страниц каталога, включая автоматизацию сбора данных и сохранение результатов.

## Инструкции по запуску

**1. Установите зависимости:**
`pip install -r requirements.txt`

**2. Используйте в коде:**
`from scraper import scrape_books`

*Сбор всех книг с сохранением в файл:*
`books_data = scrape_books(save_to_file=True)`

*Сбор данных без сохранения:*
`books_data = scrape_books(save_to_file=False)`

**3. Для автоматического запуска:**
`from scraper import run_scheduler`
`run_scheduler()  # Ежедневный запуск в 19:00`

**4. Запуск тестов:**
`pytest tests/test_scraper.py`

## Используемые библиотеки

- **requests** - для HTTP-запросов к веб-страницам
- **beautifulsoup4** - для парсинга HTML-контента  
- **schedule** - для автоматизации задач по расписанию
- **time** - для работы с временными интервалами