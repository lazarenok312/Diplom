import instance as instance
from django import forms

from django.forms import ModelForm, TextInput, Select, FileInput, DateInput, Textarea, SelectDateWidget, CheckboxInput, \
    SelectMultiple, DateTimeInput

from django.contrib.auth.models import User
from .models import Journal, Items, Issues, Genre, Category


class JournalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"
        self.fields['genres'].empty_label = "Раздел не выбран"

    class Meta:
        model = Journal
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
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название журнала...'
            }),
            'category': SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'genres': SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
            }),
            'image': DateTimeInput(attrs={
                # 'class': 'form-control',
            }),
            'files': FileInput(attrs={
                'class': 'form-control',
            }),
            'publication_date': TextInput(attrs={
                'class': 'form-control',
            }),

            'editors': SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'draft': CheckboxInput(attrs={
                'class': 'form-check-label',
            }),
        }


class IssuesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['journal'].empty_label = "Журнал не выбран"

    class Meta:
        model = Issues
        fields = ['name',
                  'journal',
                  'description',
                  'files',
                  'publication_date',
                  ]

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название выпуска...'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
            }),
            'files': FileInput(attrs={
                'class': 'form-control',
            }),
            'publication_date': TextInput(attrs={
                'class': 'form-control',
            }),
        }


class ItemsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['issues'].empty_label = "Выпуск не выбран"

    class Meta:
        model = Items
        fields = ['name',
                  'issues',
                  'description',
                  'files',
                  'image',
                  'publication_date',
                  'country',
                  'editors',
                  ]

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название статьи...'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
            }),
            'files': FileInput(attrs={
                'class': 'form-control',
            }),
            'publication_date': TextInput(attrs={
                'class': 'form-control',
            }),
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']