from django.core.management.base import BaseCommand

from ...models import Prodavnica, Kategorija, Artikal, Kasa
from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    # args = '<args1 args2>'
    help = 'Komanda za popunjavanje baze sa inicijalnim vrednostima'

    def _ubaci_prodavnice(self):
        Prodavnica.objects.all().delete()

        p1 = Prodavnica(pib="2345", naziv="Market", adresa="Adresa 1", broj_telefona="0213333333")
        p1.save()

        p2 = Prodavnica(pib="1578", naziv="Megamarket", adresa="Adresa 2", broj_telefona="02355444")
        p2.save()

        p3 = Prodavnica(pib="3456", naziv="Krojac", adresa="Adresa 3", broj_telefona="01178321")
        p3.save()

    def _ubaci_kategorije(self):
        Kategorija.objects.all().delete()

        k1 = Kategorija(oznaka="K1", naziv="Slatko")
        k1.save()

        k2 = Kategorija(oznaka="K2", naziv="Slano")
        k2.save()

        k3 = Kategorija(oznaka="K3", naziv="Cokolada")
        k3.save()

        k4 = Kategorija(oznaka="K4", naziv="Keks")
        k4.save()

        k5 = Kategorija(oznaka="K5", naziv="Mlecni proizvodi")
        k5.save()

        k6 = Kategorija(oznaka="K6", naziv="Voda")
        k6.save()

        k7 = Kategorija(oznaka="K7", naziv="Gazirano")
        k7.save()

        k8 = Kategorija(oznaka="K8", naziv="Negazirano")
        k8.save()

        k9 = Kategorija(oznaka="K9", naziv="Obuca")
        k9.save()

        k10 = Kategorija(oznaka="K10", naziv="Odeca")
        k10.save()

        k11 = Kategorija(oznaka="K11", naziv="Jakna")
        k11.save()

        k12 = Kategorija(oznaka="K12", naziv="Pantalone")
        k12.save()

    def _ubaci_artikle(self):
        Artikal.objects.all().delete()

        a1 = Artikal(oznaka="P1", naziv="Mleko", opis="Mleko 1L", cena=30.2, na_akciji=True)
        a1.prodavnica = Prodavnica.objects.get(pib="1578")

        a1.save()
        a1.kategorije.add(Kategorija.objects.get(oznaka="K5"))
        a1.save()

        a2 = Artikal(oznaka="P2", naziv="Najlepse zelje cokolada", opis="200g", cena=70.0, na_akciji=False)
        a2.prodavnica = Prodavnica.objects.get(pib="1578")

        a2.save()
        a2.kategorije.add(Kategorija.objects.get(oznaka="K3"))
        a2.kategorije.add(Kategorija.objects.get(oznaka="K1"))
        a2.save()

        a3 = Artikal(oznaka="P3", naziv="Pantalone", opis="Pamucne pantalone", cena=70.0, na_akciji=False)
        a3.prodavnica = Prodavnica.objects.get(pib="3456")

        a3.save()
        a3.kategorije.add(Kategorija.objects.get(oznaka="K10"))
        a3.kategorije.add(Kategorija.objects.get(oznaka="K12"))
        a3.save()

        a4 = Artikal(oznaka="P4", naziv="Kaput", opis="Pamucni kaput", cena=7000.0, na_akciji=False)
        a4.prodavnica = Prodavnica.objects.get(pib="3456")

        a4.save()
        a4.kategorije.add(Kategorija.objects.get(oznaka="K10"))
        a4.kategorije.add(Kategorija.objects.get(oznaka="K11"))
        a4.save()

    def _ubaci_kase(self):
        Kasa.objects.all().delete()

        k1 = Kasa(oznaka="K1", naziv="Kasa1", radi=True)
        k1.prodavnica = Prodavnica.objects.get(pib="1578")
        k1.save()

        k2 = Kasa(oznaka="K2", naziv="Kasa2", radi=True)
        k2.prodavnica = Prodavnica.objects.get(pib="3456")
        k2.save()

        k3 = Kasa(oznaka="K3", naziv="Kasa3", radi=True)
        k3.prodavnica = Prodavnica.objects.get(pib="1578")
        k3.save()

    def _napravi_korisnike(self):
        # kreiranje custom permisije (mogu se koristiti i podrazumevane)
        # npr. "prodavnice.add/change/delete/view_prodavnica"
        # za vise informacija pogledati https://docs.djangoproject.com/en/3.2/topics/auth/default/#programmatically-creating-permissions
        content_type = ContentType.objects.get_for_model(Prodavnica)
        # get_or_create koristimo za slucaj da postoji
        permission, _ = Permission.objects.get_or_create(
            codename='moze_da_koristi',
            name='Moze da koristi',
            content_type=content_type,
        )
        # kreiranje grupe
        group, _ = Group.objects.get_or_create(name="ulogovani")
        # dedoljivanje permisije grupi
        group.permissions.add(permission)
        # uklonicemo sve korisnike
        User.objects.all().delete()
        # dodacemo jednog superusera
        User.objects.create_superuser("admin", "admin@mailinator.com", "admin")
        # kreiranje obicnog korisnika
        user1 = User.objects.create_user("user1", "user1@mailinator.com", "user1")
        # dodeljivanje korisnika grupi
        user1.groups.add(group)
        # kreiranje jos jednog korisnika koji nije u grupi, te nema permisije
        User.objects.create_user("user2", "user2@mailinator.com", "user2")

    def handle(self, *args, **options):
        self._ubaci_prodavnice()
        self._ubaci_kategorije()
        self._ubaci_artikle()
        self._ubaci_kase()
        self._napravi_korisnike()
