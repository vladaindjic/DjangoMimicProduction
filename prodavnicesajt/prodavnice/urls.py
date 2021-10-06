from django.urls import path

from . import views, artikli_view, prodavnica_view, kasa_view

urlpatterns = [
    path('', views.index, name='index'),
    path('kategorije/', views.lista_kategorija, name='lista_kategorija'),
    path('artikli/', artikli_view.lista_artikala, name='lista_artikala'),
    path('brisanje/artikla/<int:id>', artikli_view.brisanje_artikla, name='brisanje_artikla'),
    path('unos/artikla/', artikli_view.unos_artikla, name='unos_artikla'),
    path('unos/artikla/<int:id>', artikli_view.unos_artikla, name='unos_artikla_p'),
    path('prodavnice/', prodavnica_view.lista_prodavnica, name='lista_prodavnica'),
    path('brisanje/prodavnice/<int:id>', prodavnica_view.brisanje_prodavnice, name='brisanje_prodavnice'),
    path('unos/prodavnice/', prodavnica_view.unos_prodavnice, name='unos_prodavnice'),
    path('unos/prodavnice/<int:id>', prodavnica_view.unos_prodavnice, name='unos_prodavnice_p'),
    path('kase', kasa_view.lista_kasa, name='lista_kasa'),
    path('unos/kase', kasa_view.unos_kase, name='unos_kase'),
    path('unos/kase/<int:id>', kasa_view.unos_kase, name='unos_kase_p'),
    path('kase/login', kasa_view.kase_login, name='kase_login'),
    path('kase/logout', kasa_view.kase_logout, name='kase_logout'),
]
