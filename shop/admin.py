from django.contrib import admin
from django import forms

from .models import Author, Book, Publisher


class BookAdminForm(forms.ModelForm):
    def clean_title(self):
        value = self.cleaned_data['title']
        if 'Django' not in value:
            raise forms.ValidationError("タイトルには「Django」という文字を含めてください")
        return value


@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'price')
    ordering = ('-price',)
    form = BookAdminForm


admin.site.register(Publisher)
admin.site.register(Author)
