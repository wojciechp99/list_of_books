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
