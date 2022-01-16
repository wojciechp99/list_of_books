from django.db.models import Model, IntegerField, CharField, DateField,URLField


class Book(Model):
    title = CharField(max_length=128)
    author = CharField(max_length=128)
    # publication_date = DateField()
    publication_date = CharField(max_length=15)
    ISBN_number = CharField(max_length=128)
    pages = IntegerField()
    preview_link = URLField()
    language = CharField(max_length=28)

    def __str__(self):
        return self.title

# tytuł, autor, data publikacji, numer ISBN, liczba stron, link do okładki i język publikacji
