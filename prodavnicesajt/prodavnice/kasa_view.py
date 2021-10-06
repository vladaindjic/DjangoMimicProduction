from django.apps.registry import apps
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import Http404

from .util import convert_to_boolean
from .models import Kasa, Prodavnica


# samo neki ovo mogu da vide
# za vise informacija pogledati https://docs.djangoproject.com/en/3.2/topics/auth/default/#the-permission-required-decorator
# 403 kod greske, ali se dozvoljava eventualno logovanje.
# podrazumevana putanja za logovanje je promenjena parametrom login_url
@login_required(login_url='/kase/login')
@permission_required('prodavnice.moze_da_koristi', raise_exception=True)
def lista_kasa(request):
    title = apps.get_app_config('prodavnice').verbose_name
    kase = Kasa.objects.all()
    return render(request, "lista_kasa.html", {"title": title, "kase": kase})


# samo neki ovome mogu da pristupe
@login_required(login_url='/kase/login')
@permission_required('prodavnice.moze_da_koristi', raise_exception=True)
def unos_kase(request, id=None):
    title = apps.get_app_config('prodavnice').verbose_name
    if request.method == 'GET':
        prodavnice = Prodavnica.objects.all()
        greska_kase = None
        if not prodavnice.exists():
            greska_kase = "Da biste mogli da unosite Kase morate uneti bar jednu prodavnicu."

        if greska_kase:
            return render(request, "unos_kase.html",
                          {"title": title, "greska_kase": greska_kase})
        if id is None:
            return render(request, "unos_kase.html", {"title": title, "prodavnice": prodavnice})
        else:
            k = Kasa.objects.get(id=id)
            return render(request, "unos_kase.html", {"title": title, "stari_id": id, "oznaka": k.oznaka,
                                                      "naziv": k.naziv, "radi": k.radi,
                                                      "prodavnica": k.prodavnica, "prodavnice": prodavnice})
    else:
        greska_oznaka = None
        greska_naziv = None
        greska_radi = None
        greska_prodavnica = None
        oznaka = request.POST['oznaka']
        naziv = request.POST['naziv']
        try:
            radi, radi_converted = convert_to_boolean(request.POST['radi'])
        except:
            radi = False
        prodavnica = request.POST['prodavnica']

        try:
            stari_id = request.POST['stari_id']
        except:
            stari_id = None

        if oznaka is not None and oznaka == "":
            greska_oznaka = "Morate uneti oznaku"
        if naziv is not None and naziv == "":
            greska_naziv = "Morate uneti naziv"
        if radi is not None and radi == "":
            greska_radi = "Morate odrediti da li radi"

        if prodavnica is not None and prodavnica == "":
            greska_prodavnica = "Morate izabrati prodavnicu"

        if greska_prodavnica is None:
            p = Prodavnica.objects.get(id=prodavnica)
            if p is not None:
                prodavnica = p
            else:
                greska_prodavnica = "Izabrana prodavnica ne postoji"

        if greska_oznaka is None:
            try:
                k = Kasa.objects.get(oznaka=oznaka)
                if stari_id is not None:
                    k2 = Kasa.objects.get(id=stari_id)
                    if k2.oznaka != k.oznaka:
                        greska_oznaka = "Kasa sa tom vrednoscu oznake vec postoji"
                else:
                    greska_oznaka = "Kasa sa tom vrednoscu oznake vec postoji"
            except:
                pass

        if greska_oznaka is None and greska_naziv is None and greska_radi is None and greska_prodavnica is None:
            if stari_id is None:
                k = Kasa(oznaka=oznaka, naziv=naziv, radi=radi, prodavnica=prodavnica)
                k.save()
            else:
                k = Kasa.objects.get(id=stari_id)
                k.oznaka = oznaka
                k.naziv = naziv
                k.radi = radi
                k.prodavnica = prodavnica
                k.save()
            return redirect('lista_kasa')
        prodavnice = Prodavnica.objects.all()
        return render(request, "unos_kase.html", {"title": title, "greska_oznaka": greska_oznaka,
                                                  "greska_naziv": greska_naziv, "greska_rado": greska_radi,
                                                  "greska_prodavnica": greska_prodavnica,
                                                  "oznaka": oznaka, "naziv": naziv, "radi": radi,
                                                  "stari_id": stari_id,
                                                  "prodavnica": prodavnica,
                                                  "prodavnice": prodavnice}
                      )


def kase_login(request):
    # ukoliko je korisnik autentifikovan, proslediti ga na listu sa kasama
    if request.user.is_authenticated:
        return redirect('lista_kasa')
    title = apps.get_app_config('prodavnice').verbose_name
    if request.method == 'GET':
        return render(request, "kase_login.html", {"title": title})
    elif request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']
        # pokusavamo autentifikaciju
        user = authenticate(request, username=username, password=password)
        if user:
            # uspesno
            login(request, user)
            # redirekcija na listu sa kasama, gde cemo proveriti permisije
            return redirect('lista_kasa')
        else:
            # neuspesno
            return render(request, "kase_login.html", {"title": title, 'greska_login': True})
    else:
        raise Http404()


# https://www.delftstack.com/howto/django/django-check-logged-in-user/
def kase_logout(request):
    # The user must be authenticated to do this.
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    raise PermissionDenied()
