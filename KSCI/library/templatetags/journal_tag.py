from django import template

from library.models import Category, Genre, Journal

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_genre():
    return Genre.objects.all()


@register.inclusion_tag('library/tags/last_journal.html')
def get_last_journal(count=3):
    journals = Journal.objects.order_by("-name")[:count]
    return {"last_journal": journals}
