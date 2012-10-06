# coding=utf-8
from api.models import Osoba
from api.models import TypOrganu
from api.models import TypFunkce
from django.db import models
from heapq import heappush, heappop
import datetime

def _d(date_str):
    """Returns datetime.date from string YY-MM-DD"""
    if not date_str:
        return None
    values = date_str.split('-')
    year = 1900 + int(values[0]) if int(values[0]) > 12 else 2000 + int(values[0])
    return datetime.date(year, int(values[1]), int(values[2]))

def _i(int_str):
    """Returns int from string"""
    if not int_str or not int_str.strip():
        return None
    return int(int_str)

class GenericReader(object):
    encoding = 'cp1250'
    filename = None

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def read(self):
        """Reads the file and submit its values to the database."""
        if not self.filename:
            print 'No filename specified for ' + self.__name__ + '! Skipping.'
            return
        models = []
        with open(self.data_dir + self.filename) as f:
            for line in f.xreadlines():
                model = self.getModel(line.split('|'))
                heappush(models, model)
        #self.model.objects.bulk_create(models)
        while models:
            heappop(models).save()
        print 'File ' + self.filename + ' successfully loaded.'

    def getModel(self, values):
        """Creates instance of self.model and sets its attributes
        per self.fields definition.
        """
        m = self.model()

        for f in self.fields.keys():
            model_field = m._meta.get_field(f)
            if isinstance(model_field, models.AutoField):
                value = _i(values[self.fields[f]])
            if isinstance(model_field, models.IntegerField):
                value = _i(values[self.fields[f]])
            elif isinstance(model_field, models.CharField):
                value = unicode(values[self.fields[f]].strip(), encoding=self.encoding)
            elif isinstance(model_field, models.DateField):
                value = _d(values[self.fields[f]])
            elif isinstance(model_field, models.ForeignKey):
                value = _i(values[self.fields[f]])
                # Some source data contain value 0 which is obviously invalid
                value = value if value <> 0 else None
                f = model_field.column
            else:
                value = values[self.fields[f]]

            setattr(m, f, value)

        return m

    def save_fields(self):
        """Gets list of fields that should be saved."""
        return [field_name for field_name in self.fields.keys() if field_name <> 'id']

class OsobaReader(GenericReader):

    filename = 'osoby.unl'
    model = Osoba

    # 211|doc. MUDr.|Emmerová|Milada|CSc.|44-11-04|Ž|98-12-07||
    fields = {
        'id': 0,
        'titul_pred': 1,
        'prijmeni': 2,
        'jmeno': 3,
        'titul_za': 4,
        'narozeni': 5,
        'pohlavi': 6,
        'zmena': 7,
        'umrti': 8,
    }
    

class TypOrganuReader(GenericReader):

    filename = 'typ_organu.unl'
    model = TypOrganu

    # 24|12|Národní shromáždění republiky Československé|National Assembly|0|24|
    fields = {
        'id': 0,
        'nadrazeny_typ': 1,
        'nazev_typ_org_cz': 2,
        'nazev_typ_org_en': 3,
        'obecny_typ': 4,
        'priorita': 5,
    }

class TypFunkceReader(GenericReader):

    filename = 'typ_funkce.unl'
    model = TypFunkce

    # 8|3|Předseda|Chairperson|1|1|
    fields = {
        'id': 0,
        'typ_organu': 1,
        'typ_funkce_cz': 2,
        'typ_funkce_en': 3,
        'priorita': 4,
        'obecny_typ': 5,
    }

def import_all(data_dir):
    load_entities = [
                     OsobaReader,
                     TypOrganuReader,
                     TypFunkceReader,
                    ]
    # perform reader validation
    for entity in load_entities:
        if not getattr(entity, 'filename', None):
            raise Exception(entity.__class__.__name__ + ".filename not found")
        if not getattr(entity, 'model', None):
            raise Exception(entity.__class__.__name__ + ".model not found")
        if not getattr(entity, 'fields', None):
            raise Exception(entity.__class__.__name__ + ".fields not found")
    # load all entites
    for Entity in load_entities:
        reader = Entity(data_dir)
        reader.read()
