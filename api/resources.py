from djangorestframework.resources import ModelResource
from djangorestframework.reverse import reverse
from api.models import Osoba
from api.models import TypOrganu
from api.models import TypFunkce

class OsobaResource(ModelResource):
    model = Osoba
    fields = ('id', 'titul_pred', 'jmeno', 'prijmeni', 'titul_za', 'narozeni', 'pohlavi', 'zmena', 'umrti', 'url')
    ordering = ('prijmeni', 'jmeno')

    def url(self, instance):
        return reverse('osoba',
                        kwargs={'id': instance.id},
                        request=self.request)

class TypOrganuResource(ModelResource):
    model = TypOrganu
    fields = ('id', 'nazev_typ_org_cz', 'nazev_typ_org_en', 'priorita', 'url', 'nadrazeny_typ_url', 'obecny_typ_url')
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
    fields = ('id', 'typ_funkce_cz', 'typ_funkce_en', 'priorita', 'obecny_typ', 'url', 'typ_organu_url')
    ordering = ('id',)

    def url(self, instance):
        return reverse('typ_funkce',
                        kwargs={'id': instance.id},
                        request=self.request)

    def typ_organu_url(self, instance):
        return reverse('typ_organu',
                        kwargs={'id': instance.typ_organu_id},
                        request=self.request)
