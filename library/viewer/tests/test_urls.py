from django.test import TestCase
from django.urls import reverse, resolve
from viewer.views import main_page, BookCreate, BookUpdate, BookDetail, BookDelete, \
    list_of_books, search_bar, get_name_to_search, import_books, api_overview, \
    book_list, BookListView, book_detail, book_create, book_update, book_delete


class UrlsTests(TestCase):

    def test_main_page(self):
        url = reverse('main')
        self.assertEqual(resolve(url).func, main_page)

    def test_add_book(self):
        url = reverse('add_book')
        self.assertEqual(resolve(url).func.view_class, BookCreate)

    def test_update_book(self):
        url = reverse('update_book', args=[1])
        self.assertEqual(resolve(url).func.view_class, BookUpdate)

    def test_detail_book(self):
        url = reverse('detail_book', args=[1])
        self.assertEqual(resolve(url).func.view_class, BookDetail)

    def test_delete_book(self):
        url = reverse('delete_book', args=[1])
        self.assertEqual(resolve(url).func.view_class, BookDelete)

    def test_list_of_all_books(self):
        url = reverse('list_of_books')
        self.assertEqual(resolve(url).func, list_of_books)

    def test_search(self):
        url = reverse('search_book')
        self.assertEqual(resolve(url).func, search_bar)

    def test_get_name_to_search(self):
        url = reverse('get_name_to_search')
        self.assertEqual(resolve(url).func, get_name_to_search)

    def test_import_books(self):
        url = reverse('import_books')
        self.assertEqual(resolve(url).func, import_books)

    #  API Tests
    def test_api_overview(self):
        url = reverse('api')
        self.assertEqual(resolve(url).func, api_overview)

    def test_book_search(self):
        url = reverse('book-search')
        self.assertEqual(resolve(url).func.view_class, BookListView)

    def test_book_list(self):
        url = reverse('book-overview')
        self.assertEqual(resolve(url).func, book_list)

    def test_book_create(self):
        url = reverse('book-create')
        self.assertEqual(resolve(url).func, book_create)

    def test_book_detail(self):
        url = reverse('book-detail', args=['1'])
        self.assertEqual(resolve(url).func, book_detail)

    def test_book_update(self):
        url = reverse('book-update', args=['1'])
        self.assertEqual(resolve(url).func, book_update)

    def test_book_delete(self):
        url = reverse('book-delete', args=['1'])
        self.assertEqual(resolve(url).func, book_delete)
