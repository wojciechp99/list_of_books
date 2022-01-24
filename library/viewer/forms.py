from datetime import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, URLField, IntegerField
from .models import Book


def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError("First letter must be upper")


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

    title = CharField(max_length=128, validators=[capitalized_validator])
    author = CharField(max_length=128, validators=[capitalized_validator])
    publication_date = IntegerField(min_value=0, max_value=datetime.now().year)
    ISBN_number = CharField(max_length=128)
    pages = IntegerField(min_value=1)
    preview_link = URLField()
    language = CharField(max_length=28)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
