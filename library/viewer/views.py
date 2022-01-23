from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from .models import Book
import requests


def main_page(request):
    return render(request, template_name='main_page.html')


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    template_name = 'forms.html'
    success_url = reverse_lazy('list_of_books')


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
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
    # sorting =

    return render(request, template_name='book_list.html', context={'books': books})


def search_bar(request):
    if request.method == "POST":
        searched = request.POST['searched']
        books = Book.objects.filter(title__contains=searched)
        if not books:
            books = Book.objects.filter(author__contains=searched)
    else:
        books = Book.objects.all()
    return render(request, template_name='search.html', context={'books': books})


def get_name_to_search(request):
    return render(request, template_name='get_name_to_search.html')


def import_books(request):
    NAME_TO_SEARCH = request.GET.get('book_id')
    get_api = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={NAME_TO_SEARCH}')

    if get_api.status_code != 200:
        return render(request, template_name='status_code.html', context={'status_code': get_api.status_code})
    # Hobbit Niezwykla podroz Oficjalny przewodnik po filmie
    try:
        books_to_add = get_api.json()['items']
        for book in books_to_add:
            try:
                Book.objects.create(title=book['volumeInfo']['title'],
                                    author=book['volumeInfo']['authors'][0],
                                    publication_date=book['volumeInfo']['publishedDate'],
                                    ISBN_number=book['volumeInfo']['industryIdentifiers'][0]['identifier'],
                                    pages=book['volumeInfo']['pageCount'],
                                    preview_link=book['volumeInfo']['previewLink'],
                                    language=book['volumeInfo']['language'])
            except:
                print("nie")
                continue
    except:
        return render(request, template_name='status_code.html', context={'status_code': get_api.status_code})

    return render(request, template_name='book_list.html', context={'books': Book.objects.all()})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookSerialized
from rest_framework import filters, generics


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List': '/book-list/',
        'Search': '/book_search/',
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

