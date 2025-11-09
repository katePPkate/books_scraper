import sys
import os
import pytest

# Добавляем путь к корневой директории проекта для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from HW_03_python_ds_2025 import get_book_data, scrape_books

class TestGetBookData:
    """Тесты для функции get_book_data"""
    
    def test_returns_dict_with_required_keys(self):
        """Проверяет, что функция возвращает словарь с нужными ключами"""
        # Используем реальную книгу для тестирования
        test_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        result = get_book_data(test_url)
        
        assert result is not None
        assert isinstance(result, dict)
        
        required_keys = [
            'title', 'price', 'rating', 'availability', 'description',
            'upc', 'product_type', 'price_excl_tax', 'price_incl_tax', 
            'tax', 'number_of_reviews'
        ]
        
        for key in required_keys:
            assert key in result, f"Ключ {key} отсутствует в результате"
    
    def test_title_is_not_empty(self):
        """Проверяет, что название книги не пустое"""
        test_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        result = get_book_data(test_url)
        
        assert result is not None
        assert 'title' in result
        assert isinstance(result['title'], str)
        assert len(result['title']) > 0
        assert result['title'] == "A Light in the Attic"
    
    def test_price_format(self):
        """Проверяет формат цены"""
        test_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        result = get_book_data(test_url)
        
        assert result is not None
        assert 'price' in result
        assert '£' in result['price']  # Проверяем наличие символа валюты

class TestScrapeBooks:
    """Тесты для функции scrape_books"""
    
    def test_returns_list_of_books(self):
        """Проверяет, что функция возвращает список книг"""
        # Ограничим парсинг первой страницей для скорости тестирования
        books = scrape_books(save_to_file=False)
        
        assert isinstance(books, list)
        assert len(books) > 0  # На первой странице должно быть несколько книг
    
    def test_books_have_required_structure(self):
        """Проверяет структуру данных в возвращаемых книгах"""
        books = scrape_books(save_to_file=False)
        
        if len(books) > 0:
            first_book = books[0]
            assert isinstance(first_book, dict)
            assert 'title' in first_book
            assert 'price' in first_book
            assert 'rating' in first_book
    
    def test_book_count_per_page(self):
        """Проверяет, что на странице правильное количество книг"""
        books = scrape_books(save_to_file=False)
        
        # На сайте обычно 20 книг на странице
        assert len(books) >= 20  # Минимум 20 книг на первой странице

def test_invalid_url_handling():
    """Проверяет обработку невалидного URL"""
    result = get_book_data("http://invalid-url-that-does-not-exist.com")
    assert result is None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
