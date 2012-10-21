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

class Overview(View):
    """
    Toto je přehled všech modelů, které API poskytuje.

    1. Osoba [osoba]
    2. Typ orgánu [typ_organu]
    3. Typ funkce [typ_funkce]
    4. Orgán [organ]
    5. Zařazení do orgánu [zarazeni_organ]
    6. Zařazení do funkce [zarazeni_funkce]
    7. Poslanec [poslanec]
    8. GPS souřadnice kanceláří poslanců [pkgps]
    9. Hlasování [hlasovani]
    10. Hlasování poslance [hlasovani_poslanec]
    11. Omluva poslance [omluva]
    12. Zpochybnění hlasování [zpochybneni]
    13. Zpochybnění hlasování poslancem [zpochybneni_poslanec]
    14. Vazba hlasování na stenozáznam [hlasovani_vazba]

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
