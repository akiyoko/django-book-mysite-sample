from django.db import models


class Publisher(models.Model):
    """出版社モデル"""

    class Meta(object):
        db_table = 'publisher'

    name = models.CharField(verbose_name='出版社名', max_length=255)

    def __str__(self):
        return self.name


class Author(models.Model):
    """著者モデル"""

    class Meta(object):
        db_table = 'author'

    name = models.CharField(verbose_name='著者名', max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """本モデル"""

    class Meta(object):
        db_table = 'book'

    title = models.CharField(verbose_name='タイトル', max_length=255)
    image = models.ImageField(verbose_name='画像', null=True, blank=True)
    publisher = models.ForeignKey(Publisher, verbose_name='出版社', on_delete=models.PROTECT)
    authors = models.ManyToManyField(Author, verbose_name='著者')
    price = models.PositiveIntegerField(verbose_name='価格', null=True, blank=True, default=0)
    description = models.TextField(verbose_name='概要', null=True, blank=True)
    publish_date = models.DateField(verbose_name='出版日', null=True, blank=True)

    def __str__(self):
        return self.title
