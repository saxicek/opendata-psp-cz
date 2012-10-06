from django.conf.urls.defaults import patterns, url
from djangorestframework.views import ListOrCreateModelView, InstanceModelView
from api.resources import OsobaResource
from api.resources import TypOrganuResource
from api.resources import TypFunkceResource

urlpatterns = patterns('',
    url(r'^$', ListOrCreateModelView.as_view(resource=OsobaResource), name='osoby-root'),
    url(r'^osoba/$', ListOrCreateModelView.as_view(resource=OsobaResource), name='osoby'),
    url(r'^osoba/(?P<id>[^/]+)/$', InstanceModelView.as_view(resource=OsobaResource), name='osoba'),
    url(r'^typ_organu/$', ListOrCreateModelView.as_view(resource=TypOrganuResource), name='typy_organu'),
    url(r'^typ_organu/(?P<id>[^/]+)/$', InstanceModelView.as_view(resource=TypOrganuResource), name='typ_organu'),
    url(r'^typ_funkce/$', ListOrCreateModelView.as_view(resource=TypFunkceResource), name='typy_funkci'),
    url(r'^typ_funkce/(?P<id>[^/]+)/$', InstanceModelView.as_view(resource=TypFunkceResource), name='typ_funkce'),
)