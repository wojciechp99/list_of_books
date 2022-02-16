from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from .models import Book
from .forms import BookForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookSerialized
from rest_framework import filters, generics

import requests


def main_page(request):
    return render(request, template_name='main_page.html')


class BookCreate(CreateView):
    form_class = BookForm
    template_name = 'forms.html'
    success_url = reverse_lazy('list_of_books')


class BookUpdate(UpdateView):
    form_class = BookForm
    model = Book
    template_name = 'forms.html'
    success_url = reverse_lazy('list_of_books')


class BookDetail(DetailView):
    model = Book
    template_name = 'detail_book.html'
    context_object_name = 'book'


class BookDelete(DeleteView):
    model = Book
    template_name = 'delete_book.html'
    success_url = reverse_lazy('main')


def list_of_books(request):
    books = Book.objects.all()

    return render(request, template_name='book_list.html',
                  context={'books': books})


def search_bar(request):
    if request.method not in ["GET", "POST"]:
        return render(request, template_name="status_code.html", status=405)

    if request.method == "GET":
        return render(request, template_name='search.html',
                      context={'books': Book.objects.all()})

    searched = request.POST['searched']
    books = Book.objects.filter(title__contains=searched)
    if not books:
        books = Book.objects.filter(author__contains=searched)
    if not books:
        books = Book.objects.filter(language=searched)
    if not books:
        books = Book.objects.filter(publication_date__gte=searched[0:4],
                                    publication_date__lt=searched[-4:])
    return render(request, template_name='search.html',
                  context={'books': books})


def get_name_to_search(request):
    return render(request, template_name='get_name_to_search.html')


def import_books(request):
    name_to_search = request.GET.get('book_id')
    response = requests.get(
        f'https://www.googleapis.com/books/v1/volumes?q={name_to_search}'
    )

    if response.status_code != 200:
        return render(request, template_name='status_code.html',
                      context={'status_code': response.status_code})

    books_to_add = response.json()['items']
    for book in books_to_add:
        if Book.objects.filter(title=book['volumeInfo']['title']):
            continue

        volume_info = book['volumeInfo']
        publication_date = parse_year(volume_info['publishedDate'])

        authors = volume_info.get("authors", [])
        Book.objects.create(
            title=volume_info['title'],
            author=",".join(authors),
            publication_date=publication_date,
            ISBN_number=volume_info['industryIdentifiers'][0]['identifier'],
            pages=volume_info.get('pageCount'),
            preview_link=volume_info['previewLink'],
            language=volume_info['language']
        )

    return render(request, template_name='book_list.html',
                  context={'books': Book.objects.all()})


def parse_year(date_to_split):
    year = date_to_split.split('-')[0]
    return int(year)


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List': 'http://127.0.0.1:8000/book-list/',
        'Search': 'http://127.0.0.1:8000/book_search/',
        'Detail View': '/book-detail/<int:pk>/',
        'Create': '/book-create/<int:pk>/',
        'Update': '/book-update/<int:pk>/',
        'Delete': '/book-delete/<int:pk>/',
    }
    return Response(api_urls)


@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerialized(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def book_detail(request, pk):
    books = Book.objects.get(id=pk)
    serializer = BookSerialized(books, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def book_update(request, pk):
    book = Book.objects.get(id=pk)
    serializer = BookSerialized(instance=book, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def book_create(request):
    serializer = BookSerialized(data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def book_delete(request, pk):
    book = Book.objects.get(id=pk)
    book.delete()
    return Response("Item deleted successfully")


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerialized
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'ISBN_number', 'language']
