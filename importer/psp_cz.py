# coding=utf-8
from django.db import models
from django.db import transaction
from pytz import timezone
from decimal import Decimal
import datetime
import time
import re
import logging

from api.models import Osoba
from api.models import Poslanec
from api.models import TypOrganu
from api.models import TypFunkce
from api.models import Organ
from api.models import Funkce
from api.models import ZarazeniOrgan
from api.models import ZarazeniFunkce
from api.models import Pkgps
from api.models import Hlasovani
from api.models import HlasovaniPoslanec
from api.models import Omluva
from api.models import Zpochybneni
from api.models import ZpochybneniPoslanec
from api.models import HlasovaniVazby

DATETIME_RE = re.compile(r'(\d{2})-(\d{2})-(\d{2}) (\d{2}):(\d{2})')
FULL_DATETIME_RE = re.compile(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})')
SHORT_DATETIME_RE = re.compile(r'(\d{4})-(\d{2})-(\d{2}) (\d{2})')
DATE_RE = re.compile(r'(\d{2})\.(\d{2})\.(\d{4})')
SHORT_DATE_RE = re.compile(r'(\d{2})-(\d{2})-(\d{2})')

tz = timezone('Europe/Prague')

def _d(date_str):
    """Returns datetime.date from string YY-MM-DD or DD.MM.YYYY"""
    if not date_str:
        return None
    # FORMAT FIX: dates are sometimes in format DD.MM.YYYY ...
    m = DATE_RE.match(date_str)
    if m:
        return datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    # FORMAT FIX: ... and sometimes in format YY-MM-DD
    m = SHORT_DATE_RE.match(date_str)
    if m:
        year = int(m.group(1)) + 1900 if int(m.group(1)) > 12 else int(m.group(1)) + 2000
        return datetime.date(year, int(m.group(2)), int(m.group(3)))

    logging.error('String |' + date_str + '| does not match any supported date format!')
    return None

def _dt(datetime_str):
    """Returns datetime.datetime from string YY-MM-DD HH"""
    if not datetime_str:
        return None
    m = SHORT_DATETIME_RE.match(datetime_str)
    if m:
        dt = datetime.datetime(
            int(m.group(1)), int(m.group(2)), int(m.group(3)),
            int(m.group(4)))

    m = DATETIME_RE.match(datetime_str)
    if m:
        year = int(m.group(1)) + 1900 if int(m.group(1)) > 12 else int(m.group(1)) + 2000
        dt = datetime.datetime(
            year, int(m.group(2)), int(m.group(3)),
            int(m.group(4)), int(m.group(5)))

    m = FULL_DATETIME_RE.match(datetime_str)
    if m:
        dt = datetime.datetime(
            int(m.group(1)), int(m.group(2)), int(m.group(3)),
            int(m.group(4)), int(m.group(5)))

    if dt:
        return tz.localize(dt)
    else:
        logging.error('String |' + datetime_str + '| does not match any supported date format!')
        return None

def _i(int_str):
    """Returns int from string"""
    if not int_str or not int_str.strip():
        return None

    return int(int_str)

def _dec(decimal_str):
    """Returns Decimal from string"""
    if not decimal_str:
        return None

    return Decimal(decimal_str)

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

class GenericReader(object):
    """
    'Abstract' class which implements import logic. Every subclass must set
    following class attributes:

    `filename` name of the file we are exporting from

    `model` is Django model class we will use for ORM mapping. If model is
            determined dynamically from data row, function `dynamic_model` must
            be overloaded.

    `fields` is dictionary of model fields and their position in the file. This
            represents actual mapping. Dictionary keys are model attribute
            names, values are position in the file row (where '|' character is
            the separator).

    `has_id` is switch for tables which to not have single primary key (ID).
            If set to False, query against database is run to check if
            the record with same values already exists in the database.
            If found, no insert/update operation is performed. If not found,
            new record is created. If set to True (default), database model has
            single primary key and insert/update operation is handled
            automatically by Django.
    """
    encoding = 'cp1250'
    filename = None
    model = None
    fields = {}
    has_id = True

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.record_count = 0

        if not self.has_dynamic_model():
            self._init_getters(self.model)

    def dynamic_model(self, values):
        """
        Returns Django model class based on input values. Used in cases when
        input file is loaded into multiple database tables.
        """
        return None

    def process_values(self, values):
        """
        Method suitable for overloading. It can transform values parsed from
        row to match custom needs - for example join 2 original columns into
        one.
        NOTE: values contains newline character as the last value. Do not forget
              it when setting position for artificial fields.
        """
        return values

    def _init_getters(self, model_class):
        self.getter = {}
        self.db_field = {}
        for f in self.fields.keys():
            model_field = model_class._meta.get_field(f)
            self.db_field[f] = f
            if isinstance(model_field, models.AutoField):
                self.getter[f] = _i
            elif isinstance(model_field, models.IntegerField):
                self.getter[f] = _i
            elif isinstance(model_field, models.DecimalField):
                self.getter[f] = _dec
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
                        # transform input values if needed
                        values = self.process_values(line.split('|'))
                        # map the line to model
                        model = self.fill_model(values)
                        if model:
                            model.save()
                        # count record even if it has not been saved - it is in
                        # the database already
                        self.record_count += 1

        if not self.has_dynamic_model():
            logging.info(
                'File ' + self.filename +\
                ' successfully loaded (%d records in %.03f sec; %d records in DB).'\
                % (self.record_count, t.interval, self.model.objects.count())
            )
        else:
            logging.info(
                'File ' + self.filename +\
                ' successfully loaded (%d records in %.03f sec).'\
                % (self.record_count, t.interval)
            )

    def fill_model(self, values):
        """Creates instance of self.model and sets its attributes
        per self.fields definition.
        """
        if self.has_dynamic_model():
            model_cls = self._get_dynamic_model(values)
        else:
            model_cls = self.model

        if self.has_id:
            m = model_cls()
            for f in self.fields.keys():
                value = self.getter[f](values[self.fields[f]])
                setattr(m, self.db_field[f], value)
        else:
            m = self._no_id_get_model(values, model_cls)
        return m

    def _get_dynamic_model(self, values):
        cls = self.dynamic_model(values)
        self._init_getters(cls)

        return cls

    def save_fields(self):
        """Gets list of fields that should be saved."""
        return [field_name for field_name in self.fields.keys() if field_name <> 'id']

    def _no_id_get_model(self, values, model_class):
        """
        This function should be used for files with no ID for records. It is
        queried using all attributes, if no matching record is found, new
        instance is created. If query returns exactly one item, function
        returns None - item is already in database, there is no need to save it
        again.
        """
        values_dict = {}

        for f in self.fields.keys():
            value = self.getter[f](values[self.fields[f]])
            values_dict[self.db_field[f]] = value

        # check whether the model instance exists in the DB
        instances = model_class.objects.filter(**values_dict)
        if instances:
            if len(instances) == 1:
                # Instance is in database already, there is no need to store it
                m = None
            else:
                raise Exception('Query for ' + model_class.__class__.__name__ +
                                ' with criteria ' + str(values_dict) +
                                ' returned more than 1 row!')
        else:
            m = model_class(**values_dict)

        return m

    def has_dynamic_model(self):
        return self.model is None


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
    has_id = False

    # 2965|644|1|1993-09-15 00||93-09-17|14-03-25|
    fields = {
        'osoba': 0,
        'zarazeni_od': 3,
        'zarazeni_do': 4,
        'mandat_od': 5,
        'mandat_do': 6,
    }

    def dynamic_model(self, values):
        """Creates instance of self.model and sets its attributes
        per self.fields definition.
        This is overloaded implementation of generic function
        because we are loading data into 2 tables.
        """
        if values[2] == '0':
            m = ZarazeniOrgan
            self.fields['organ'] = 1
            if 'funkce' in self.fields:
                del self.fields['funkce']
        else:
            m = ZarazeniFunkce
            self.fields['funkce'] = 1
            if 'organ' in self.fields:
                del self.fields['organ']

        return m

class PoslanecReader(GenericReader):

    filename = 'poslanec.unl'
    model = Poslanec

    # 1262|5859|586|155|170|http://www.jirisulc.cz/|Klíšská 2058/33|Ústí nad Labem|40001|sulcj@psp.cz|||2057|http://www.facebook.com/profile.php?id=100000017868039&ref=ts|1|
    fields = {
        'id': 0,
        'osoba': 1,
        'kraj': 2,
        'kandidatka': 3,
        'obdobi': 4,
        'web': 5,
        'ulice': 6,
        'obec': 7,
        'psc': 8,
        'email': 9,
        'telefon': 10,
        'fax': 11,
        'psp_telefon': 12,
        'facebook': 13,
        'foto': 14,
    }

class PkgpsReader(GenericReader):

    filename = 'pkgps.unl'
    model = Pkgps
    has_id = False

    # 1091|Masarykova 12/1355; Blansko; 67801|49.2121903|16.3856678|
    fields = {
        'poslanec': 0,
        'adresa': 1,
        'delka': 2,
        'sirka': 3,
    }

class HlasovaniReader(GenericReader):

    filename = 'hl2010s.unl'
    model = Hlasovani

    # 52621|170|7|10|0|10-10-29|09:08|149|0|7|1|157|79|N|A|Pořad schůze||
    fields = {
        'id': 0,
        'organ': 1,
        'schuze': 2,
        'cislo': 3,
        'bod': 4,
        'pro': 7,
        'proti': 8,
        'zdrzel': 9,
        'nehlasoval': 10,
        'prihlaseno': 11,
        'kvorum': 12,
        'druh_hlasovani': 13,
        'vysledek': 14,
        'nazev_dlouhy': 15,
        'nazev_kratky': 16,
        # custom value
        'datum': 18,
    }

    def process_values(self, values):
        """
        Joins datum and čas fields into one.
        """
        values.append(values[5] + ' ' + values[6])
        return values

class HlasovaniPoslanecReader(GenericReader):

    filename = 'hl2010h.unl'
    model = HlasovaniPoslanec
    has_id = False

    # 1088|52361|A|
    fields = {
        'poslanec': 0,
        'hlasovani': 1,
        'vysledek': 2,
    }

class OmluvaReader(GenericReader):

    filename = 'omluvy.unl'
    model = Omluva
    has_id = False

    # 167|571|02-02-13|09:30|23:59|
    fields = {
        'organ': 0,
        'poslanec': 1,
        # custom value
        'od': 6,
        'do': 7,
    }

    def process_values(self, values):
        """
        Joins fields `den`, `od` and `do`. It follows similar logic like
        original except that both fields are always set. If justification is
        valid for the whole day then the interval is explicitly set from
        midnight to midnight.
        """
        od = values[3] if values[3] != '' else '00:00'
        do = values[4] if values[4] != '' else '23:59'
        values.append(values[2] + ' ' + od)
        values.append(values[2] + ' ' + do)
        return values

class ZpochybneniReader(GenericReader):

    filename = 'hl2010z.unl'
    model = Zpochybneni
    has_id = False

    # 55680|67|0|55681|55682|
    fields = {
        'hlasovani': 0,
        'turn': 1,
        'mode': 2,
        'h2': 3,
        'h3': 4,
    }

class ZpochybneniPoslanecReader(GenericReader):

    filename = 'hl2010x.unl'
    model = ZpochybneniPoslanec
    has_id = False

    # 55680|5971|0|
    fields = {
        'hlasovani': 0,
        'osoba': 1,
        'mode': 2,
    }

class HlasovaniVazbyReader(GenericReader):

    filename = 'hl2010v.unl'
    model = HlasovaniVazby
    has_id = False

    # 52361|6|0|
    fields = {
        'hlasovani': 0,
        'turn': 1,
        'typ': 2,
    }

def import_all(data_dir):
    data_dir = data_dir if data_dir[-1:] == '/' else data_dir + '/'
    load_entities = [
                     OsobaReader,
                     TypOrganuReader,
                     TypFunkceReader,
                     OrganReader,
                     FunkceReader,
                     ZarazeniReader,
                     PoslanecReader,
                     PkgpsReader,
                     HlasovaniReader,
                     HlasovaniPoslanecReader,
                     OmluvaReader,
                     ZpochybneniReader,
                     ZpochybneniPoslanecReader,
                     HlasovaniVazbyReader,
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
