# import os
#
from django.db import models
from django.urls import reverse

COUNTRY_CHOICES = (
    ("Россия", "Россия"),
    ("Кыргызстан", "Кыргызстан"),
    ("Казахстан", "Казахстан"),
    ("Узбекистан", "Узбекистан"),
)


class Category(models.Model):
    "Категории"
    id = models.AutoField(primary_key=True)
    name = models.CharField("Категория", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['id']


class Genre(models.Model):
    "Разделы"
    id = models.AutoField(primary_key=True)
    name = models.CharField("Раздел", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ['id']


class ScientificEditors(models.Model):
    """Редакционная коллегия"""
    id = models.AutoField(primary_key=True)
    name = models.CharField("Имя", blank=True, max_length=50)
    surname = models.CharField("Фамилия", blank=True, max_length=50)
    patronymic = models.CharField("Отчество", blank=True, max_length=50)
    phone_number = models.CharField("Номер телефона", blank=True, max_length=20)
    image = models.ImageField("Изображение", blank=True, upload_to="Editors/")
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic

    def get_absolute_url(self):
        return reverse('editor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Редакционная коллегия"
        verbose_name_plural = "Редакционная коллегия"
        ordering = ['id']


class Journal(models.Model):
    """Журналы"""
    id = models.AutoField(primary_key=True)
    name = models.CharField('Название', max_length=100, unique=True)
    category = models.ManyToManyField(Category, verbose_name='Категория')
    genres = models.ManyToManyField(Genre, verbose_name="Раздел")
    description = models.TextField("Описание")
    image = models.ImageField('Изображение', upload_to='journal/')
    files = models.FileField(upload_to='journal/', blank=False)
    publication_date = models.PositiveSmallIntegerField('Дата выхода', default='2022')
    country = models.CharField('Страна', max_length=30, choices=COUNTRY_CHOICES)
    editors = models.ManyToManyField(ScientificEditors, verbose_name="Редактор", related_name='journal_editors')
    draft = models.BooleanField('Черновик', default=False)

    def filedir(self):
        return str(self.files).replace('journal/', '')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('journal_detail', kwargs={"slug": self.name})

    def get_update_url(self):
        return reverse('journal_update', kwargs={"slug": self.name})

    def get_delete_url(self):
        return reverse('journal_delete', kwargs={"pk": self.id})

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'
        ordering = ['id']


class Issues(models.Model):
    """Выпуски"""
    id = models.AutoField(primary_key=True)
    name = models.CharField('Название', max_length=100)
    journal = models.ForeignKey(Journal, verbose_name='Журнал', on_delete=models.SET_NULL, null=True)
    description = models.TextField("Описание")
    files = models.FileField(upload_to='Issues/', blank=False)
    publication_date = models.PositiveSmallIntegerField('Год выпуска', default='2022')

    def __str__(self):
        return self.name

    def filedir(self):
        return str(self.files).replace('Issues/', '')

    def get_absolute_url(self):
        return reverse('issues_detail', kwargs={'slug': self.name})

    def get_update_url(self):
        return reverse('issues_update', kwargs={"slug": self.name})

    def get_delete_url(self):
        return reverse('issues_delete', kwargs={"pk": self.id})

    @property
    def items(self):
        return self.items.set_all().count()

    class Meta:
        verbose_name = 'Выпуск'
        verbose_name_plural = 'Выпуски'
        ordering = ['id']


class Items(models.Model):
    """Статьи"""
    id = models.AutoField(primary_key=True)
    name = models.CharField("Имя", blank=True, max_length=50)
    issues = models.ForeignKey(Issues, verbose_name='Выпуск', on_delete=models.SET_NULL, null=True)
    files = models.FileField(upload_to='Items/', blank=False)
    description = models.TextField("Описание")
    image = models.ImageField('Изображение', upload_to='items/')
    publication_date = models.PositiveSmallIntegerField('Год написания статьи', default='2022')
    country = models.CharField('Страна', max_length=30, choices=COUNTRY_CHOICES)
    editors = models.ManyToManyField(ScientificEditors, verbose_name="Редактор")

    def __str__(self):
        return self.name

    def filedir(self):
        return str(self.files).replace('Items/', '')

    def get_absolute_url(self):
        return reverse('items_detail', kwargs={"slug": self.name})

    def get_update_url(self):
        return reverse('items_update', kwargs={"slug": self.name})

    def get_delete_url(self):
        return reverse('items_delete', kwargs={"pk": self.id})

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['id']
