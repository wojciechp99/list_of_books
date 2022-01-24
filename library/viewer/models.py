from django.db.models import Model, IntegerField, CharField, URLField


class Book(Model):
    title = CharField(max_length=128)
    author = CharField(max_length=128)
    publication_date = IntegerField(blank=True)
    ISBN_number = CharField(max_length=128, blank=True)
    pages = IntegerField(blank=True)
    preview_link = URLField(blank=True)
    language = CharField(max_length=28)

    def __str__(self):
        return self.title
