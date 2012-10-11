"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import json

class ApiTest(TestCase):
    fixtures = ['api_test_data.json']

    def test_osoba(self):
        response = self.client.get('/api/osoba/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/osoba/5990/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'titul_pred', 'jmeno', 'prijmeni', 'titul_za', 'narozeni',
                    'pohlavi', 'zmena', 'umrti', 'url']:
            self.assertIn(att, obj)

    def test_typ_organu(self):
        response = self.client.get('/api/typ_organu/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/typ_organu/12/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'nazev_typ_org_cz', 'nazev_typ_org_en', 'priorita', 'url',
                    'nadrazeny_typ_url', 'obecny_typ_url']:
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
        for att in ['id', 'organ_id', 'typ_organu_id', 'zkratka', 'nazev_organu_cz',
                    'nazev_organu_en', 'od_organ', 'do_organ', 'priorita',
                    'cl_organ_base', 'url', 'typ_organu_url', 'organ_url',
                    'typ_organu_url']:
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
        for att in ['id', 'zarazeni_od', 'zarazeni_do', 'mandat_od', 'mandat_do',
                    'osoba_id', 'osoba_url', 'organ_id', 'organ_url', 'url']:
            self.assertIn(att, obj)

    def test_zarazeni_funkce(self):
        response = self.client.get('/api/zarazeni_funkce/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/zarazeni_funkce/164/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        for att in ['id', 'zarazeni_od', 'zarazeni_do', 'mandat_od', 'mandat_do',
                    'osoba_id', 'osoba_url', 'funkce_id', 'funkce_url', 'url']:
            self.assertIn(att, obj)
