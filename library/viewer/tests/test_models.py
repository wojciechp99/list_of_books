from django.test import TestCase
from viewer.models import Book


class BookModelTests(TestCase):

    def setUp(self):
        self.projects1 = Book.objects.create(
            title="Project 1",
            author="Test",
            publication_date=2022,
            ISBN_number="123432",
            pages=123,
            preview_link="https://www.google.com/",
            language='pl',
        )

    def test_str(self):
        self.assertEqual(str(self.projects1), "Project 1")
