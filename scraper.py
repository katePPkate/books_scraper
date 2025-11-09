import time
import requests
import schedule
from bs4 import BeautifulSoup
def get_book_data(book_url: str) -> dict:
    """
    Парсит данные о книге со страницы каталога сайта Books to Scrape.
    
    Функция получает HTML-страницу книги, извлекает основную информацию (название, цену, рейтинг, наличие, описание) 
    и дополнительные характеристики из таблицы Product Information.
    
    Args:
        url (str): URL-адрес страницы книги для парсинга
     
    Returns:
        Optional[Dict]: Словарь с данными о книге в следующем формате:
            {
                'title': str,           # Название книги
                'price': str,           # Цена
                'rating': str,          # Рейтинг (количество звезд)
                'availability': str,    # Информация о наличии
                'description': str,     # Описание книги
                'upc': str,             # UPC код
                'product_type': str,    # Тип продукта
                'price_excl_tax': str,  # Цена без налога
                'price_incl_tax': str,  # Цена с налогом
                'tax': str,             # Размер налога
                'number_available': str # Количество доступных книг
            }
        Возвращает None в случае ошибки при загрузке страницы.
    """
     
    try:
        response = requests.get(book_url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1').text.strip()
        price = soup.find('p', class_='price_color').text.strip()
        
        rating_element = soup.find('p', class_='star-rating')
        rating_classes = rating_element.get('class', [])
        rating = [cls for cls in rating_classes if cls != 'star-rating'][0]
        
        availability = soup.find('p', class_='instock availability').text.strip() 
        
        product_description = soup.find('div', id='product_description')
        if product_description:
            description = product_description.find_next_sibling('p').text.strip()
        else:
            description = "No description available"
        
        product_info = {}
        info_table = soup.find('table', class_='table table-striped')
        if info_table:
            rows = info_table.find_all('tr')
            for row in rows:
                header = row.find('th').text.strip()
                value = row.find('td').text.strip()
                product_info[header] = value
        book_data = {
            'title': title,
            'price': price,
            'rating': rating,
            'availability': availability,
            'description': description,
            'upc': product_info.get('UPC', ''),
            'product_type': product_info.get('Product Type', ''),
            'price_excl_tax': product_info.get('Price (excl. tax)', ''),
            'price_incl_tax': product_info.get('Price (incl. tax)', ''),
            'tax': product_info.get('Tax', ''),
            'number_of_reviews': product_info.get('Number of reviews', '')
        }
        return book_data
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return None
    except Exception as e:
        print(f"Ошибка при парсинге данных: {e}")
        return None
def scrape_books(save_to_file: bool = False) -> list:
    """
    Собирает данные обо всех книгах со всех страниц каталога Books to Scrape.
    
    Args:
        save_to_file (bool): Флаг для сохранения результатов в файл.
     
    Returns:
        list: Список словарей с данными о всех книгах
    """
    
    base_url = "http://books.toscrape.com/"
    all_books_data = []
    page_number = 1
    
    while True:
        page_url = f"{base_url}catalogue/page-{page_number}.html"
        
        print(f"Парсинг страницы {page_number}: {page_url}")
        
        response = requests.get(page_url)
            
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')

        book_cards = soup.find_all('article', class_='product_pod')
        
        for i, card in enumerate(book_cards, 1):
            book_link_tag = card.find('h3').find('a')
            book_link = book_link_tag['href']
            book_url = f"{base_url}catalogue/{book_link}"
            book_data = get_book_data(book_url)
            all_books_data.append(book_data)
        
        # Проверяем наличие следующей страницы
        next_button = soup.find('li', class_='next')
        if not next_button:
            break
            
        page_number += 1
        
    if save_to_file and all_books_data:
        save_books_to_file(all_books_data)
    
    return all_books_data


def save_books_to_file(books_data: list) -> None:
    """Сохраняет данные о книгах в файл"""
    try:
        with open('books_data.txt', 'w', encoding='utf-8') as file:
            file.write(f"ОТЧЕТ О ПАРСИНГЕ\n")
            file.write(f"Всего книг: {len(books_data)}\n")
            file.write("=" * 80 + "\n\n")
            
            for i, book in enumerate(books_data, 1):
                file.write(f"КНИГА №{i}\n")
                file.write(f"Название: {book.get('title', 'N/A')}\n")
                file.write(f"Цена: {book.get('price', 'N/A')}\n")
                file.write(f"Рейтинг: {book.get('rating', 'N/A')}\n")
                file.write(f"Наличие: {book.get('availability', 'N/A')}\n")
                file.write(f"UPC: {book.get('upc', 'N/A')}\n")
                file.write(f"Тип: {book.get('product_type', 'N/A')}\n")
                file.write(f"Цена без налога: {book.get('price_excl_tax', 'N/A')}\n")
                file.write(f"Цена с налогом: {book.get('price_incl_tax', 'N/A')}\n")
                file.write(f"Налог: {book.get('tax', 'N/A')}\n")
                file.write(f"Количество отзывов: {book.get('number_of_reviews', 'N/A')}\n")
                file.write(f"Описание: {book.get('description', 'N/A')[:200]}...\n")
                file.write("-" * 80 + "\n\n")
        
        print(f"Данные сохранены в 'books_data.txt'")
        
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")