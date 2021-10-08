from django.apps.registry import apps
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .models import Kategorija

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def index(request):
    title = apps.get_app_config('prodavnice').verbose_name
    return render(request, 'index.html', {"title": title})


# Under the assumption that category list is rarely changed,
# caching is applicable.
# Note that if you add new category, the view will be updated when
# the cache expires. If you're impatient, then clear the redis cache. :)
# implement caching on this view
# see for tutorial https://realpython.com/caching-in-django-with-redis/
@cache_page(CACHE_TTL)
def lista_kategorija(request):
    kategorije = Kategorija.objects.all()
    title = apps.get_app_config('prodavnice').verbose_name
    return render(request, "lista_kategorija.html", {"title": title, "kategorije": kategorije})
