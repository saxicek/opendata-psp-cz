# coding=utf-8
from api.models import Osoba
from api.models import TypOrganu
from api.models import TypFunkce
from api.models import Organ
from api.models import Funkce
from api.models import ZarazeniOrgan
from api.models import ZarazeniFunkce
from django.db import models
from django.db import transaction
from pytz import timezone
import datetime
import time
import re

DATETIME_RE = re.compile(r'(\d{4})-(\d{2})-(\d{2}) (\d{2})')

def _d(date_str):
    """Returns datetime.date from string YY-MM-DD"""
    if not date_str:
        return None
    values = date_str.split('-')
    year = 1900 + int(values[0]) if int(values[0]) > 12 else 2000 + int(values[0])

    return datetime.date(year, int(values[1]), int(values[2]))

def _dt(datetime_str):
    """Returns datetime.datetime from string YY-MM-DD HH"""
    if not datetime_str:
        return None
    m = DATETIME_RE.match(datetime_str)

    return datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                             int(m.group(4)), tzinfo=timezone('Europe/Prague'))

def _i(int_str):
    """Returns int from string"""
    if not int_str or not int_str.strip():
        return None

    return int(int_str)

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

class GenericReader(object):
    encoding = 'cp1250'
    filename = None
    model = None

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.record_count = 0

        if self.model:
            self._init_getters(self.model)

    def _init_getters(self, model):
        self.getter = {}
        self.db_field = {}
        for f in self.fields.keys():
            model_field = model._meta.get_field(f)
            self.db_field[f] = f
            if isinstance(model_field, models.AutoField):
                self.getter[f] = _i
            elif isinstance(model_field, models.IntegerField):
                self.getter[f] = _i
            elif isinstance(model_field, models.CharField):
                self.getter[f] = lambda x: unicode(x.strip(), encoding=self.encoding)
            elif type(model_field) == models.DateTimeField:
                self.getter[f] = _dt
            elif isinstance(model_field, models.DateField):
                self.getter[f] = _d
            elif isinstance(model_field, models.ForeignKey):
                self.getter[f] = lambda x: _i(x) if _i(x) <> 0 else None
                self.db_field[f] = model_field.column
            else:
                self.getter[f] = lambda x: x

    @transaction.commit_on_success
    def read(self):
        """Reads the file and submit its values to the database."""
        with Timer() as t:
            with open(self.data_dir + self.filename) as f:
                previous_line = ''
                for line in f:
                    # FORMAT FIX: some rows are split with \r\\\n - join them with next line
                    line = previous_line + line
                    if line[-3:] == "\r\\\n":
                        previous_line = line[:-3] + ' '
                    else:
                        previous_line = ''
                        # map the line to model
                        model = self.fillModel(line.split('|'))
                        model.save()
                        self.record_count += 1

        print 'File ' + self.filename + ' successfully loaded (%d records in %.03f sec).' % (self.record_count, t.interval)

    def fillModel(self, values):
        """Creates instance of self.model and sets its attributes
        per self.fields definition.
        """
        m = self.model()

        for f in self.fields.keys():
            value = self.getter[f](values[self.fields[f]])
            setattr(m, self.db_field[f], value)

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

class OrganReader(GenericReader):

    filename = 'organy.unl'
    model = Organ

    # 165|0|11|PSP1|Poslanecká sněmovna|Chamber of Deputies|92-06-06|96-06-06|1000|0|
    fields = {
        'id': 0,
        'organ': 1,
        'typ_organu': 2,
        'zkratka': 3,
        'nazev_organu_cz': 4,
        'nazev_organu_en': 5,
        'od_organ': 6,
        'do_organ': 7,
        'priorita': 8,
        'cl_organ_base': 9,
    }

class FunkceReader(GenericReader):

    filename = 'funkce.unl'
    model = Funkce

    # 755|168|18|Předseda|1|
    fields = {
        'id': 0,
        'organ': 1,
        'typ_funkce': 2,
        'nazev_funkce_cz': 3,
        'priorita': 4,
    }

class ZarazeniReader(GenericReader):

    filename = 'zarazeni.unl'

    # 2965|644|1|1993-09-15 00||93-09-17|14-03-25|
    fields = {
        'osoba': 0,
        'zarazeni_od': 3,
        'zarazeni_do': 4,
        'mandat_od': 5,
        'mandat_do': 6,
    }

    def fillModel(self, values):
        """Creates instance of self.model and sets its attributes
        per self.fields definition.
        This is overloaded implementation of generic function
        because we are loading data into 2 tables.
        """
        model = None
        if values[2] == '0':
            model = ZarazeniOrgan
            self.fields['organ'] = 1
            if 'funkce' in self.fields:
                del self.fields['funkce']
        else:
            model = ZarazeniFunkce
            self.fields['funkce'] = 1
            if 'organ' in self.fields:
                del self.fields['organ']

        self._init_getters(model)
        values_dict = {}

        for f in self.fields.keys():
            value = self.getter[f](values[self.fields[f]])
            values_dict[self.db_field[f]] = value

        # check whether the model instance exists in the DB
        instances = model.objects.filter(**values_dict)
        if instances:
            if len(instances) == 1:
                m = instances[0]
            else:
                raise Exception('Query for ' + model.__class__.__name__ + ' with criteria ' + values_dict +
                                ' returned more than 1 row!')
        else:
            m = model(**values_dict)

        return m

def import_all(data_dir):
    data_dir = data_dir if data_dir[-1:] == '/' else data_dir + '/'
    load_entities = [
                     OsobaReader,
                     TypOrganuReader,
                     TypFunkceReader,
                     OrganReader,
                     FunkceReader,
                     ZarazeniReader,
                    ]
    # perform reader validation
    for entity in load_entities:
        if not getattr(entity, 'filename', None):
            raise Exception(entity.__class__.__name__ + ".filename not found")
        if not getattr(entity, 'fields', None):
            raise Exception(entity.__class__.__name__ + ".fields not found")
    # load all entites
    for Entity in load_entities:
        reader = Entity(data_dir)
        reader.read()
