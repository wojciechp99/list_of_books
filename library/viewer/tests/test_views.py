import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from viewer.models import Book


class ViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.main_url = reverse('main')
        self.book_create = reverse('add_book')
        self.update_book = reverse('update_book', args=[1])
        self.detail_book = reverse('detail_book', args=[1])
        self.delete_book = reverse('delete_book', args=[1])

        self.list_of_books = reverse('list_of_books')
        self.search = reverse('search_book')
        self.get_name_to_search = reverse('get_name_to_search')
        self.import_books = reverse('import_books')

        self.book_1 = Book.objects.create(
            title="Project 1",
            author="Test",
            publication_date=2022,
            ISBN_number="123432",
            pages=123,
            preview_link="https://www.google.com/",
            language='pl',
        )

    def test_main_page_view(self):
        response = self.client.get(self.main_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_page.html')

    def test_book_create_view(self):
        response = self.client.get(self.book_create)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forms.html')

    def test_book_update_view(self):
        response = self.client.get(self.update_book)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forms.html')

    def test_book_detail_view(self):
        response = self.client.get(self.detail_book)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail_book.html')

    def test_book_delete_view(self):
        response = self.client.get(self.delete_book)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_book.html')

    def test_list_of_books_view(self):
        response = self.client.get(self.list_of_books)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')

    def test_search_view(self):
        response = self.client.get(self.search)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_get_name_to_search_view(self):
        response = self.client.get(self.get_name_to_search)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'get_name_to_search.html')

    def test_import_books_view(self):
        response = self.client.get(self.import_books)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')


class ApiViewsTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.data = {
            "id": 1,
            "title": "Hobbit",
            "author": "John Ronald Reuel Tolkien",
            "publication_date": 1985,
            "ISBN_number": "IND:3900000",
            "pages": 234,
            "preview_link": "https://www.google.com/",
            "language": "pl"
        }

        self.api_overview = reverse('api')
        self.book_search = reverse('book-search')
        self.book_list = reverse('book-overview')
        self.book_create = reverse('book-create')

    def test_api_overview(self):
        response = self.client.get(self.api_overview, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_book_search(self):
        response = self.client.get(self.api_overview, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_list(self):
        response = self.client.get(self.book_list, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_create(self):
        response = self.client.post(self.book_create, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.count(), 1)
