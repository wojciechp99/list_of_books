from django.db.models import Model, IntegerField, CharField, URLField


class Book(Model):
    title = CharField(max_length=128)
    author = CharField(max_length=128, null=True)
    publication_date = IntegerField(blank=True, null=True)
    ISBN_number = CharField(max_length=128, blank=True, null=True)
    pages = IntegerField(blank=True, null=True)
    preview_link = URLField(blank=True, null=True)
    language = CharField(max_length=28, null=True)

    def __str__(self):
        return self.title
