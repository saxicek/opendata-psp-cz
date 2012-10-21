# coding=utf-8
"""
Test suite for API.
"""

from django.test import TestCase
import json

class ApiTest(TestCase):
    fixtures = ['api_test_data.json']

    def test_osoba(self):
        # get list of all instances
        response = self.client.get('/api/osoba/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        # get one instance
        response = self.client.get('/api/osoba/5990/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'titul_pred', 'jmeno', 'prijmeni', 'titul_za',
                    'narozeni', 'pohlavi', 'zmena', 'umrti', 'url']:
            self.assertIn(att, obj)

        # update instance - disabled
        response = self.client.put(
            '/api/osoba/5990/',
            {"jmeno": "Janina", "titul_za": "CSc.", "titul_pred": "Ing.",
             "pohlavi": "Ž", "prijmeni": "Fischerová",
             "narozeni": "1955-08-20"})
        self.assertEqual(response.status_code, 405)

        # delete instance - disabled
        response = self.client.delete('/api/osoba/5990/')
        self.assertEqual(response.status_code, 405)

        # create instance = disabled
        response = self.client.post(
            '/api/osoba/',
            {"jmeno": "Janina", "titul_za": "CSc.", "titul_pred": "Ing.",
             "pohlavi": "Ž", "prijmeni": "Fischerová",
             "narozeni": "1955-08-20"})
        self.assertEqual(response.status_code, 405)

    def test_typ_organu(self):
        response = self.client.get('/api/typ_organu/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/typ_organu/12/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'nazev_typ_org_cz', 'nazev_typ_org_en', 'priorita',
                    'url', 'nadrazeny_typ_url', 'obecny_typ_url']:
            self.assertIn(att, obj)

    def test_typ_funkce(self):
        response = self.client.get('/api/typ_funkce/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/typ_funkce/71/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'typ_funkce_cz', 'typ_funkce_en', 'priorita',
                    'obecny_typ', 'url', 'typ_organu_url']:
            self.assertIn(att, obj)

    def test_organ(self):
        response = self.client.get('/api/organ/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/organ/170/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'organ_id', 'typ_organu_id', 'zkratka',
                    'nazev_organu_cz', 'nazev_organu_en', 'od_organ',
                    'do_organ', 'priorita', 'cl_organ_base', 'url',
                    'typ_organu_url', 'organ_url', 'typ_organu_url']:
            self.assertIn(att, obj)

    def test_funkce(self):
        response = self.client.get('/api/funkce/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/funkce/1241/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'organ_id', 'typ_funkce', 'nazev_funkce_cz',
                    'priorita', 'organ', 'url', 'organ_url', 'typ_funkce_url']:
            self.assertIn(att, obj)

    def test_zarazeni_organ(self):
        response = self.client.get('/api/zarazeni_organ/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/zarazeni_organ/2911/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'zarazeni_od', 'zarazeni_do', 'mandat_od',
                    'mandat_do', 'osoba_id', 'osoba_url', 'organ_id',
                    'organ_url', 'url']:
            self.assertIn(att, obj)

    def test_zarazeni_funkce(self):
        response = self.client.get('/api/zarazeni_funkce/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/zarazeni_funkce/164/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'zarazeni_od', 'zarazeni_do', 'mandat_od',
                    'mandat_do', 'osoba_id', 'osoba_url', 'funkce_id',
                    'funkce_url', 'url']:
            self.assertIn(att, obj)

    def test_poslanec(self):
        response = self.client.get('/api/poslanec/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/poslanec/1130/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'web', 'ulice', 'obec', 'psc', 'email', 'telefon',
                    'fax', 'psp_telefon', 'facebook', 'foto', 'url',
                    'osoba_url', 'kraj_url', 'kandidatka_url', 'obdobi_url']:
            self.assertIn(att, obj)

    def test_pkgps(self):
        response = self.client.get('/api/pkgps/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/pkgps/103/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'adresa', 'sirka', 'delka', 'url', 'poslanec_url']:
            self.assertIn(att, obj)

    def test_hlasovani(self):
        response = self.client.get('/api/hlasovani/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/hlasovani/52361/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'schuze', 'cislo', 'bod', 'datum', 'pro', 'proti',
                    'zdrzel', 'nehlasoval', 'prihlaseno', 'kvorum',
                    'druh_hlasovani', 'vysledek', 'nazev_dlouhy',
                    'nazev_kratky', 'organ_id', 'url', 'organ_url']:
            self.assertIn(att, obj)

    def test_hlasovani_poslanec(self):
        response = self.client.get('/api/hlasovani_poslanec/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/hlasovani_poslanec/244/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'vysledek', 'poslanec_id', 'hlasovani_id', 'url',
                    'poslanec_url', 'hlasovani_url']:
            self.assertIn(att, obj)

    def test_omluva(self):
        response = self.client.get('/api/omluva/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/omluva/13185/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['od', 'do', 'organ_id', 'poslanec_id', 'url', 'organ_url',
                    'poslanec_url']:
            self.assertIn(att, obj)

    def test_zpochybneni(self):
        response = self.client.get('/api/zpochybneni/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/zpochybneni/5/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['turn', 'mode', 'hlasovani_id', 'h2_id', 'h3_id', 'url',
                    'hlasovani_url', 'h2_url', 'h3_url']:
            self.assertIn(att, obj)

    def test_zpochybneni_poslanec(self):
        response = self.client.get('/api/zpochybneni_poslanec/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/zpochybneni_poslanec/4/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['mode', 'hlasovani_id', 'osoba_id', 'url', 'hlasovani_url',
                    'osoba_url']:
            self.assertIn(att, obj)

    def test_hlasovani_vazby(self):
        response = self.client.get('/api/hlasovani_vazba/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/hlasovani_vazba/2/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['turn', 'typ', 'hlasovani_id', 'url', 'hlasovani_url']:
            self.assertIn(att, obj)
