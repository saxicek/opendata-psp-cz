from django.conf.urls import patterns, url

from api.resources import OsobaResource
from api.resources import TypOrganuResource
from api.resources import TypFunkceResource
from api.resources import OrganResource
from api.resources import FunkceResource
from api.resources import ZarazeniOrganResource
from api.resources import ZarazeniFunkceResource
from api.resources import PoslanecResource
from api.resources import PkgpsResource
from api.resources import HlasovaniResource
from api.resources import HlasovaniPoslanecResource
from api.resources import OmluvaResource
from api.resources import ZpochybneniResource
from api.resources import ZpochybneniPoslanecResource
from api.resources import HlasovaniVazbyResource
from api.views import ListModelView, InstanceModelReadOnlyView

urlpatterns = patterns('',
    url(r'^$', ListModelView.as_view(resource=OsobaResource), name='osoby-root'),
    url(r'^osoba/$', ListModelView.as_view(resource=OsobaResource), name='osoby'),
    url(r'^osoba/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=OsobaResource), name='osoba'),
    url(r'^typ_organu/$', ListModelView.as_view(resource=TypOrganuResource), name='typy_organu'),
    url(r'^typ_organu/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=TypOrganuResource), name='typ_organu'),
    url(r'^typ_funkce/$', ListModelView.as_view(resource=TypFunkceResource), name='typy_funkci'),
    url(r'^typ_funkce/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=TypFunkceResource), name='typ_funkce'),
    url(r'^organ/$', ListModelView.as_view(resource=OrganResource), name='organy'),
    url(r'^organ/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=OrganResource), name='organ'),
    url(r'^funkce/$', ListModelView.as_view(resource=FunkceResource), name='funkce-list'),
    url(r'^funkce/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=FunkceResource), name='funkce'),
    url(r'^zarazeni_organ/$', ListModelView.as_view(resource=ZarazeniOrganResource), name='zarazeni_organu'),
    url(r'^zarazeni_organ/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=ZarazeniOrganResource), name='zarazeni_organ'),
    url(r'^zarazeni_funkce/$', ListModelView.as_view(resource=ZarazeniFunkceResource), name='zarazeni_funkci'),
    url(r'^zarazeni_funkce/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=ZarazeniFunkceResource), name='zarazeni_funkce'),
    url(r'^poslanec/$', ListModelView.as_view(resource=PoslanecResource), name='poslanci'),
    url(r'^poslanec/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=PoslanecResource), name='poslanec'),
    url(r'^pkgps/$', ListModelView.as_view(resource=PkgpsResource), name='pkgps-list'),
    url(r'^pkgps/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=PkgpsResource), name='pkgps'),
    url(r'^hlasovani/$', ListModelView.as_view(resource=HlasovaniResource), name='hlasovani-list'),
    url(r'^hlasovani/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=HlasovaniResource), name='hlasovani'),
    url(r'^hlasovani_poslanec/$', ListModelView.as_view(resource=HlasovaniPoslanecResource), name='hlasovani_poslanec-list'),
    url(r'^hlasovani_poslanec/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=HlasovaniPoslanecResource), name='hlasovani_poslanec'),
    url(r'^omluva/$', ListModelView.as_view(resource=OmluvaResource), name='omluvy'),
    url(r'^omluva/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=OmluvaResource), name='omluva'),
    url(r'^zpochybneni/$', ListModelView.as_view(resource=ZpochybneniResource), name='zpochybneni-list'),
    url(r'^zpochybneni/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=ZpochybneniResource), name='zpochybneni'),
    url(r'^zpochybneni_poslanec/$', ListModelView.as_view(resource=ZpochybneniPoslanecResource), name='zpochybneni_poslanec-list'),
    url(r'^zpochybneni_poslanec/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=ZpochybneniPoslanecResource), name='zpochybneni_poslanec'),
    url(r'^hlasovani_vazby/$', ListModelView.as_view(resource=HlasovaniVazbyResource), name='hlasovani_vazby-list'),
    url(r'^hlasovani_vazby/(?P<id>[^/]+)/$', InstanceModelReadOnlyView.as_view(resource=HlasovaniVazbyResource), name='hlasovani_vazby'),
)
