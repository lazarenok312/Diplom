from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .forms import UserRegistrationForm

from library.models import Journal, Category, Genre, ScientificEditors, Issues, Items
from .forms import JournalForm, IssuesForm, ItemsForm


class JournalFilter:
    """"Фильтрация журналов"""
    """"По категории"""

    def get_category(self):
        return Category.objects.all()

    """"По жанру"""

    def get_genre(self):
        return Genre.objects.all()

    """"По годам"""

    def get_years(self):
        return Journal.objects.filter(draft=False).values('publication_date').distinct()


class Genres:
    def get_name(self):
        return Genre.objects.all()


class JournalView(JournalFilter, Genres, ListView):
    """"Список журналов"""
    model = Journal
    queryset = Journal.objects.filter(draft=False)
    paginate_by = 6


class JournalDetailView(DetailView):
    """Описание журналов"""
    model = Journal
    slug_field = "name"


# class JournalCategoryView(ListView):
#     model = Journal
#     template_name = 'library/journal_list.html'
#     context_object_name = 'journal'
#
#     def get_queryset(self):
#         return Journal.objects.filter(category__slug=self.kwargs['category_slug'], draft=False)


def create_journal(request):
    """Создание журнала"""
    error = ''
    if request.method == 'POST':
        form = JournalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            error = 'Неправильно заполнена форма добавления журнала'

    form = JournalForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'library/create_journal.html', data)


class JournalUpdateView(DetailView, UpdateView):
    """изменение журналов"""
    model = Journal
    template_name = 'library/tags/journal_update.html'
    slug_field = "name"
    fields = ['name',
              'category',
              'genres',
              'description',
              'image',
              'files',
              'publication_date',
              'country',
              'editors',
              'draft',
              ]


class JournalDeleteView(DeleteView):
    """удаление журналов"""
    model = Journal
    success_url = '/'
    template_name = 'library/tags/journal_delete.html'


class IssuesDetailView(DetailView):
    """Описание выпусков"""
    model = Issues
    template_name = 'library/issues_detail.html'
    slug_field = "name"


def create_issues(request):
    """Создание выпуска"""
    error = ''
    if request.method == 'POST':
        form = IssuesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            error = 'Неправильно заполнена форма добавления выпуска'

    form = IssuesForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'library/create_issues.html', data)


class IssuesUpdateView(DetailView, UpdateView):
    """изменение выпуска"""
    model = Issues
    template_name = 'library/tags/issues_update.html'
    slug_field = "name"
    fields = ['name',
              'journal',
              'description',
              'files',
              'publication_date',
              ]


class IssuesDeleteView(DeleteView):
    """удаление выпусков"""
    model = Issues
    success_url = '/'
    template_name = 'library/tags/issues_delete.html'


class ItemsDetailView(DetailView):
    """Описание статей"""
    model = Items
    template_name = 'library/items_detail.html'
    slug_field = "name"


def create_items(request):
    """Создание статьи"""
    error = ''
    if request.method == 'POST':
        form = ItemsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            error = 'Неправильно заполнена форма добавления статьи'

    form = ItemsForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'library/create_items.html', data)


class ItemsUpdateView(DetailView, UpdateView):
    """изменение статьи"""
    model = Items
    template_name = 'library/tags/items_update.html'
    slug_field = "name"
    fields = ['name',
              'issues',
              'description',
              'files',
              'image',
              'publication_date',
              'country',
              'editors',
              ]


class ItemsDeleteView(DeleteView):
    """удаление статей"""
    model = Items
    success_url = '/'
    template_name = 'library/tags/items_delete.html'


class EditorView(DetailView):
    """Описание редакторов"""
    model = ScientificEditors
    template_name = 'library/Editor.html'
    slug_field = "name"


class Search(JournalFilter, ListView):
    """Поиск"""
    paginate_by = 6

    def get_queryset(self):
        return Journal.objects.filter(name__iregex=self.request.GET.get("q"))


def register(request):
    """Регистрация юзера"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'library/create_user.html', {'user_form': user_form})


class FilterJournalView(JournalFilter, ListView):
    """Фильтр"""
    paginate_by = 6

    def get_queryset(self):
        queryset = Journal.objects.filter(
            Q(publication_date__in=self.request.GET.getlist("publication_date")) |
            Q(category__in=self.request.GET.getlist("category")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset


def showthis(request):
    item = Items.objects.all()

    context = {'item': item, 'item_count': len(item)}

    return render(request, 'library/journal_detail.html', context)

