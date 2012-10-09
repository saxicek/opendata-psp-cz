from djangorestframework.resources import ModelResource
from djangorestframework.reverse import reverse
from api.models import Osoba
from api.models import TypOrganu
from api.models import TypFunkce
from api.models import Organ
from api.models import Funkce

class OsobaResource(ModelResource):
    model = Osoba
    fields = ('id', 'titul_pred', 'jmeno', 'prijmeni', 'titul_za', 'narozeni',
              'pohlavi', 'zmena', 'umrti', 'url')
    ordering = ('prijmeni', 'jmeno')

    def url(self, instance):
        return reverse('osoba',
                        kwargs={'id': instance.id},
                        request=self.request)

class TypOrganuResource(ModelResource):
    model = TypOrganu
    fields = ('id', 'nazev_typ_org_cz', 'nazev_typ_org_en', 'priorita', 'url',
              'nadrazeny_typ_url', 'obecny_typ_url')
    ordering = ('id',)

    def url(self, instance):
        return reverse('typ_organu',
                        kwargs={'id': instance.id},
                        request=self.request)

    def nadrazeny_typ_url(self, instance):
        if instance.nadrazeny_typ_id:
            return reverse('typ_organu',
                            kwargs={'id': instance.nadrazeny_typ_id},
                            request=self.request)

    def obecny_typ_url(self, instance):
        if instance.obecny_typ_id:
            return reverse('typ_organu',
                            kwargs={'id': instance.obecny_typ_id},
                            request=self.request)

class TypFunkceResource(ModelResource):
    model = TypFunkce
    fields = ('id', 'typ_funkce_cz', 'typ_funkce_en', 'priorita', 'obecny_typ',
              'url', 'typ_organu_url')
    ordering = ('id',)

    def url(self, instance):
        return reverse('typ_funkce',
                        kwargs={'id': instance.id},
                        request=self.request)

    def typ_organu_url(self, instance):
        return reverse('typ_organu',
                        kwargs={'id': instance.typ_organu_id},
                        request=self.request)

class OrganResource(ModelResource):
    model = Organ
    fields = ('id', 'organ_id', 'typ_organu_id', 'zkratka', 'nazev_organu_cz',
              'nazev_organu_en', 'od_organ', 'do_organ', 'priorita',
              'cl_organ_base', 'url', 'typ_organu_url', 'organ_url',
              'typ_organu_url')
    ordering = ('id',)

    def url(self, instance):
        return reverse('organ',
                        kwargs={'id': instance.id},
                        request=self.request)

    def organ_url(self, instance):
        return reverse('organ',
                        kwargs={'id': instance.organ_id},
                        request=self.request)

    def typ_organu_url(self, instance):
        return reverse('typ_organu',
                        kwargs={'id': instance.typ_organu_id},
                        request=self.request)

class FunkceResource(ModelResource):
    model = Funkce
    fields = ('id', 'organ_id', 'typ_funkce', 'nazev_funkce_cz', 'priorita',
              'organ', 'url', 'organ_url', 'typ_funkce_url')
    ordering = ('id',)

    def url(self, instance):
        return reverse('organ',
                        kwargs={'id': instance.id},
                        request=self.request)

    def organ_url(self, instance):
        return reverse('organ',
                        kwargs={'id': instance.organ_id},
                        request=self.request)

    def typ_funkce_url(self, instance):
        return reverse('typ_funkce',
                        kwargs={'id': instance.typ_funkce_id},
                        request=self.request)
