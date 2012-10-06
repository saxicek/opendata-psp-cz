# coding=utf-8
from django.db import models

# Create your models here.
class Osoba(models.Model):
    POHLAVI_CHOICES = (
        ('M', 'Muž'),
        ('Ž', 'Žena'),               
    )

    ## Atributy
    titul_pred = models.CharField(max_length=100, blank=True) # Titul pred jmenem
    jmeno = models.CharField(max_length=100)    # Jméno
    prijmeni = models.CharField(max_length=100) # Příjmení, v některých případech obsahuje i
                                                # dodatek typu "st.", "ml."
    titul_za = models.CharField(max_length=100, blank=True)   # Titul za jménem
    narozeni = models.DateField(null=True)      # Datum narození, pokud neznámo, pak 1.1.1900.
    pohlavi = models.CharField(max_length=1, choices = POHLAVI_CHOICES) # Pohlaví, "M" jako muž,
                                                                        # ostatní hodnoty žena
    zmena = models.DateField(null=True)         # Datum posledni změny
    umrti = models.DateField(null=True)         # Datum úmrtí

class TypOrganu(models.Model):
    ## Atributy
    nazev_typ_org_cz = models.CharField(max_length=100) # Název typu orgánu v češtině
    nazev_typ_org_en = models.CharField(max_length=100, blank=True) # Název typu orgánu v angličtině
    priorita = models.IntegerField(null=True) # Priorita při výpisu

    ## Cizí klíče
    nadrazeny_typ = models.ForeignKey('TypOrganu',                  # Identifikátor nadřazeného typu orgánu
                                      null=True,                    # (typ_organu:id_typ_org), pokud je null či
                                      related_name='detailni_typy') # nevyplněno, pak nemá nadřazený typ
    obecny_typ = models.ForeignKey('TypOrganu',                    # Obecný typ orgánu, pokud je vyplněný, odpovídá
                                   null=True,                      # záznamu v typ_organu:id_typ_org. Pomocí tohoto
                                   related_name='specificke_typy') # sloupce lze najít např. všechny výbory v různých
                                                                   # typech zastupitelských sborů.

class TypFunkce(models.Model):
    OBECNY_TYP_CHOICES = (
        (1, 'předseda'),
        (2, 'místopředseda'),               
    )

    ## Atributy
    typ_funkce_cz = models.CharField(max_length=100)             # Název typu funkce v češtině
    typ_funkce_en = models.CharField(max_length=100, blank=True) # Název typu funkce v angličtině
    priorita = models.IntegerField(null=True)                    # Priorita při výpisu
    obecny_typ = models.IntegerField(null=True, # Obecný typ funkce, 1 - předseda, 2 - místopředseda
                                     choices = OBECNY_TYP_CHOICES)

    ## Cizí klíče
    typ_organu = models.ForeignKey(TypOrganu)   # Identifikátor typu orgánu, viz typ_organu:id_typ_org
