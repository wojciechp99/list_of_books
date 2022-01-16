from django.urls import path
from .views import main_page, BookCreate, BookUpdate, BookDetail, BookDelete, list_of_books, search_bar, \
    get_name_to_search, import_books

urlpatterns = [
    path('add_book', BookCreate.as_view(), name='add_book'),
    path('update_book/<int:pk>', BookUpdate.as_view(), name='update_book'),
    path('detail_book/<int:pk>', BookDetail.as_view(), name="detail_book"),
    path('delete_book/<int:pk>', BookDelete.as_view(), name="delete_book"),
    path('list_of_all_books', list_of_books, name='list_of_books'),
    path('search', search_bar, name='search_book'),
    path('get_name_to_search', get_name_to_search, name='get_name_to_search'),
    path('import_books', import_books, name='import_books'),
    path('', main_page, name='main')
]
