# coding=utf-8
from djangorestframework.mixins import ReadModelMixin
from djangorestframework.views import ModelView
from djangorestframework.reverse import reverse
from djangorestframework.views import View

class InstanceModelReadOnlyView(ReadModelMixin, ModelView):
    """
    A view which provides default operations for read against a model instance.
    """
    _suffix = 'Instance'

class Sandbox(View):
    """
    This is the sandbox for all models.
    """

    def get(self, request):
        return [{'name': 'osoba', 'url': reverse('osoby', request=request)},
                {'name': 'typ_organu', 'url': reverse('typy_organu', request=request)},
                {'name': 'typ_funkce', 'url': reverse('typy_funkci', request=request)},
                {'name': 'organ', 'url': reverse('organy', request=request)},
                {'name': 'zarazeni_organ', 'url': reverse('zarazeni_organu', request=request)},
                {'name': 'zarazeni_funkce', 'url': reverse('zarazeni_funkci', request=request)},
                {'name': 'poslanec', 'url': reverse('poslanci', request=request)},
                {'name': 'pkgps', 'url': reverse('pkgps-list', request=request)},
                {'name': 'hlasovani', 'url': reverse('hlasovani-list', request=request)},
                {'name': 'hlasovani_poslanec', 'url': reverse('hlasovani_poslanec-list', request=request)},
                {'name': 'omluva', 'url': reverse('omluvy', request=request)},
                {'name': 'zpochybneni', 'url': reverse('zpochybneni-list', request=request)},
                {'name': 'zpochybneni_poslanec', 'url': reverse('zpochybneni_poslanec-list', request=request)},
                {'name': 'hlasovani_vazba', 'url': reverse('hlasovani_vazby', request=request)}
        ]
