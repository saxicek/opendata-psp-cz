# coding=utf-8
from django.db import models

class Osoba(models.Model):
    """
    Tabulka osoby
    ========  =======  ====================================================
    Sloupec   Typ      Použití a vazby
    ========  =======  ====================================================
    id_osoba  int      Identifikátor osoby
    pred      char(X)  Titul před jménem
    jmeno     char(X)  Jméno
    prijmeni  char(X)  Příjmení, v některých případech obsahuje i dodatek
                       typu "st.", "ml."
    za        char(X)  Titul za jménem
    narozeni  date     Datum narození, pokud neznámo, pak 1.1.1900.
    pohlavi   char(X)  Pohlaví, "M" jako muž, ostatní hodnoty žena
    zmena     date     Datum poslední změny
    umrti     date     Datum úmrtí
    ========  =======  ====================================================

    """
    POHLAVI_CHOICES = (
        ('M', 'Muž'),
        ('Ž', 'Žena'),               
    )

    titul_pred = models.CharField(max_length=100, blank=True)
    jmeno = models.CharField(max_length=100)
    prijmeni = models.CharField(max_length=100)
    titul_za = models.CharField(max_length=100, blank=True)
    narozeni = models.DateField(null=True)
    pohlavi = models.CharField(max_length=1, choices = POHLAVI_CHOICES)
    zmena = models.DateField(null=True)
    umrti = models.DateField(null=True)

class TypOrganu(models.Model):
    """
    Tabulka typ_organu
    ================  =======  ============================================
    Sloupec           Typ      Použití a vazby
    ================  =======  ============================================
    id_typ_org        int      Identifikátor typu orgánu
    typ_id_typ_org    int      Identifikátor nadřazeného typu orgánu
                               (typ_organu:id_typ_org), pokud je null či
                               nevyplněno, pak nemá nadřazený typ
    nazev_typ_org_cz  char(X)  Název typu orgánu v češtině
    nazev_typ_org_en  char(X)  Název typu orgánu v angličtině
    typ_org_obecny    int      Obecný typ orgánu, pokud je vyplněný,
                               odpovídá záznamu v typ_organu:id_typ_org.
                               Pomocí tohoto sloupce lze najít např.
                               všechny výbory v různých typech
                               zastupitelských sborů.
    priorita          int      Priorita při výpisu
    ================  =======  ============================================

    """
    nazev_typ_org_cz = models.CharField(max_length=100)
    nazev_typ_org_en = models.CharField(max_length=100, blank=True)
    priorita = models.IntegerField(null=True)

    nadrazeny_typ = models.ForeignKey('TypOrganu', null=True,
                                      related_name='detailni_typy')
    obecny_typ = models.ForeignKey('TypOrganu', null=True,
                                   related_name='specificke_typy')

class TypFunkce(models.Model):
    """
    Tabulka typ_funkce
    =================  =======  ===========================================
    Sloupec            Typ      Použití a vazby
    =================  =======  ===========================================
    id_typ_funkce      int      Identifikátor typu funkce
    id_typ_org         int      Identifikátor typu orgánu, viz
                                typ_organu:id_typ_org
    typ_funkce_cz      char(X)  Název typu funkce v češtině
    typ_funkce_en      char(X)  Název typu funkce v angličtině
    priorita           int      Priorita při výpisu
    typ_funkce_obecny  int      Obecný typ funkce, 1 - předseda,
                                2 - místopředseda
    =================  =======  ===========================================

    """
    OBECNY_TYP_CHOICES = (
        (1, 'předseda'),
        (2, 'místopředseda'),               
    )

    typ_funkce_cz = models.CharField(max_length=100)
    typ_funkce_en = models.CharField(max_length=100, blank=True)
    priorita = models.IntegerField(null=True)
    obecny_typ = models.IntegerField(null=True,
                                     choices = OBECNY_TYP_CHOICES)

    typ_organu = models.ForeignKey(TypOrganu)

class Organ(models.Model):
    """
    Tabulka organy
    ===============  =======  =============================================
    Sloupec          Typ      Použití a vazby
    ===============  =======  =============================================
    id_organ         int      Identifikátor orgánu
    organ_id_organ   int      Identifikátor nadřazeného orgánu, viz
                              organy:id_organ
    id_typ_organu    int      Typ orgánu, viz typ_organu:id_typ_organu
    zkratka          char(X)  Zkratka orgánu, bez diakritiky, v některých
                              případech se zkratka při zobrazení nahrazuje
                              jiným názvem
    nazev_organu_cz  int      Název orgánu v češtině
    nazev_organu_en  int      Název orgánu v angličtině
    od_organ         date     Ustavení orgánu
    do_organ         date     Ukončení orgánu
    priorita         int      Priorita výpisu orgánů
    cl_organ_base    int      Pokud je nastaveno na 1, pak při výpisu členů
                              se nezobrazují záznamy v tabulkce zarazeni
                              kde cl_funkce == 0. Toto chování odpovídá
                              tomu, že v některých orgánech nejsou členové
                              a teprve z nich se volí funkcionáři, ale
                              přímo se volí do určité funkce.
    ===============  =======  =============================================

    """
    zkratka = models.CharField(max_length=100)
    nazev_organu_cz = models.CharField(max_length=1000)
    nazev_organu_en = models.CharField(max_length=1000)
    od_organ = models.DateField(null=True)
    do_organ = models.DateField(null=True)
    priorita = models.IntegerField(null=True)
    cl_organ_base = models.IntegerField(null=True)

    organ = models.ForeignKey('Organ', null=True,
                              related_name='podorgany')
    typ_organu = models.ForeignKey(TypOrganu)

class Funkce(models.Model):
    """
    Tabulka funkce
    ===============  =======  =============================================
    Sloupec          Typ      Použití a vazby
    ===============  =======  =============================================
    id_funkce        int      Identifikátor funkce, používá se
                              v zarazeni:id_fo
    id_organ         int      Identifikátor orgánu, viz organy:id_organ
    id_typ_funkce    int      Typ funkce, viz typ_funkce:id_typ_funkce
    nazev_funkce_cz  char(X)  Název funkce, pouze pro interní použití
    priorita         int      Priorita výpisu
    ===============  =======  =============================================

    """
    nazev_funkce_cz = models.CharField(max_length=100)
    priorita = models.IntegerField(null=True)

    organ = models.ForeignKey(Organ)
    typ_funkce = models.ForeignKey(TypFunkce)

class ZarazeniOrgan(models.Model):
    """
    Tabulka zarazeni
    =========  ======================  ====================================
    Sloupec    Typ                     Použití a vazby
    =========  ======================  ====================================
    id_osoba   int                     Identifikátor osoby, viz
                                       osoba:id_osoba
    id_of      int                     Identifikátor orgánu či funkce:
                                       pokud je zároveň nastaveno
                                       zarazeni:cl_funkce == 0, pak id_o
                                       odpovídá organy:id_organ, pokud
                                       cl_funkce == 1, pak odpovídá
                                       funkce:id_funkce.
    cl_funkce  int                     Status členství nebo funce: pokud je
                                       rovno 0, pak jde o členství,
                                       pokud 1, pak jde o funkci.
    od_o       datetime(year to hour)  Zařazení od
    do_o       datetime(year to hour)  Zařazení do
    od_f       date                    Mandát od. Nemusí být vyplněno a
                                       pokud je vyplněno, pak určuje datum
                                       vzniku mandátu a zarazeni:od_o
                                       obsahuje datum volby.
    do_f       date                    Mandát do. Nemusí být vyplněno a
                                       pokud je vyplněno, určuje datum
                                       konce mandátu a zarazeni:do_o
                                       obsahuje datum ukončení zařazení.
    =========  ======================  ====================================

    Zdrojová tabulka není v 3NF a proto jsem ji rozdělil na 2:
    - ZarazeniOrgan
    - ZarazeniFunkce

    Model ZarazeniOrgan reprezentuje záznamy, které mají cl_funkce == 0.

    """
    zarazeni_od = models.DateTimeField()
    zarazeni_do = models.DateTimeField(null=True)
    mandat_od = models.DateField(null=True)
    mandat_do = models.DateField(null=True)

    osoba = models.ForeignKey(Osoba)
    organ = models.ForeignKey(Organ)

class ZarazeniFunkce(models.Model):
    """
    Tabulka zarazeni
    =========  ======================  ====================================
    Sloupec    Typ                     Použití a vazby
    =========  ======================  ====================================
    id_osoba   int                     Identifikátor osoby, viz
                                       osoba:id_osoba
    id_of      int                     Identifikátor orgánu či funkce:
                                       pokud je zároveň nastaveno
                                       zarazeni:cl_funkce == 0, pak id_o
                                       odpovídá organy:id_organ, pokud
                                       cl_funkce == 1, pak odpovídá
                                       funkce:id_funkce.
    cl_funkce  int                     Status členství nebo funce: pokud je
                                       rovno 0, pak jde o členství,
                                       pokud 1, pak jde o funkci.
    od_o       datetime(year to hour)  Zařazení od
    do_o       datetime(year to hour)  Zařazení do
    od_f       date                    Mandát od. Nemusí být vyplněno a
                                       pokud je vyplněno, pak určuje datum
                                       vzniku mandátu a zarazeni:od_o
                                       obsahuje datum volby.
    do_f       date                    Mandát do. Nemusí být vyplněno a
                                       pokud je vyplněno, určuje datum
                                       konce mandátu a zarazeni:do_o
                                       obsahuje datum ukončení zařazení.
    =========  ======================  ====================================

    Zdrojová tabulka není v 3NF a proto jsem ji rozdělil na 2:
    - ZarazeniOrgan
    - ZarazeniFunkce

    Model ZarazeniFunkce reprezentuje záznamy, které mají cl_funkce == 1.

    """
    zarazeni_od = models.DateTimeField()
    zarazeni_do = models.DateTimeField(null=True)
    mandat_od = models.DateField(null=True)
    mandat_do = models.DateField(null=True)

    osoba = models.ForeignKey(Osoba)
    funkce = models.ForeignKey(Funkce)

class Poslanec(models.Model):
    """
    Tabulka poslanec
    =============  =======  ===============================================
    Sloupec        Typ      Použití a vazby
    =============  =======  ===============================================
    id_poslanec    int      Identifikátor poslance
    id_osoba       int      Identifikátor osoby, viz osoba:id_osoba
    id_kraj        int      Volební kraj, viz organy:id_organu
    id_kandidatka  int      Volební strana/hnutí, viz org:id_organu, pouze
                            odkazuje na stranu/hnutí, za kterou byl zvolen
                            a nemusí mít souvislost s členstvím
                            v poslaneckém klubu.
    id_obdobi      int      Volební období, viz organy:id_organu
    web            char(X)  URL vlastních stránek poslance
    ulice          char(X)  Adresa regionální kanceláře, ulice.
    obec           char(X)  Adresa regionální kanceláře, obec.
    psc            char(X)  Adresa regionální kanceláře, PSČ.
    email          char(X)  E-mailová adresa poslance, případně obecná
                            posta@psp.cz.
    telefon        char(X)  Adresa regionální kanceláře, telefon.
    fax            char(X)  Adresa regionální kanceláře, fax.
    psp_telefon    char(X)  Telefonní číslo do kanceláře v budovách PS.
    facebook       char(X)  URL stránky služby Facebook.
    foto           int      Pokud je rovno 1, pak existuje fotografie
                            poslance.
    =============  =======  ===============================================

    """
    web = models.CharField(max_length=1000, blank=True)
    ulice = models.CharField(max_length=100, blank=True)
    obec = models.CharField(max_length=100, blank=True)
    psc = models.CharField(max_length=10, blank=True)
    email = models.CharField(max_length=100, blank=True)
    telefon = models.CharField(max_length=100, blank=True)
    fax = models.CharField(max_length=100, blank=True)
    psp_telefon = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=1000, blank=True)
    foto = models.IntegerField()

    osoba = models.ForeignKey(Osoba)
    kraj = models.ForeignKey(Organ,
                             related_name='poslanci_kraje')
    kandidatka = models.ForeignKey(Organ, null=True,
                                   related_name='poslanci_strany')
    obdobi = models.ForeignKey(Organ,
                               related_name='poslanci_obdobi')

class Pkgps(models.Model):
    """
    ===========  =======  =================================================
    Sloupec      Typ      Použití a vazby
    ===========  =======  =================================================
    id_poslanec  int      Identifikátor poslance, viz poslanec:id_poslanec
    adresa       char(X)  Adresa kanceláře, jednotlivé položky jsou
                          odděleny středníkem
    sirka        char(X)  Severní šířka, WGS 84, formát GG.AABBCCC,
                          GG = stupně, AA - minuty, BB - vteřiny,
                          CCC - tisíciny vteřin
    delka        char(X)  Východní délka, WGS 84, formát GG.AABBCCC,
                          GG = stupně, AA - minuty, BB - vteřiny,
                          CCC - tisíciny vteřin
    ===========  =======  =================================================

    """
    adresa = models.CharField(max_length=1000)
    sirka = models.DecimalField(max_digits=20, decimal_places=17)
    delka = models.DecimalField(max_digits=20, decimal_places=17)

    poslanec = models.ForeignKey(Poslanec)

class Hlasovani(models.Model):
    """
    ==============  ================  =====================================
    Sloupec         Typ               Použití a vazby
    ==============  ================  =====================================
    id_hlasovani    int               Identifikátor hlasování
    id_organ        int               Identifikátor orgánu, viz
                                      organy:id_organ
    schuze          int               Číslo schůze
    cislo           int               Číslo hlasování
    bod             int               Bod pořadu schůze; je-li menší než 1,
                                      pak jde o procedurální hlasování nebo
                                      o hlasování k bodům, které v době
                                      hlasování neměly přiděleno číslo.
    datum           date              Datum hlasování
    čas             datetime          Čas hlasování
                    (hour to minute)
    pro             int               Počet hlasujících pro
    proti           int               Počet hlasujících proti
    zdrzel          int               Počet hlasujících zdržel se, tj.
                                      stiskl tlačítko X
    nehlasoval      int               Počet přihlášených, kteří nestiskli
                                      žádné tlačítko
    prihlaseno      int               Počet přihlášených poslanců
    kvorum          int               Kvórum, nejmenší počet hlasů k
                                      přijetí návrhu
    druh_hlasovani  char(X)           Druh hlasování: N - normální,
                                      R - ruční (nejsou známy hlasování
                                      jednotlivých poslanců)
    vysledek        char(X)           Výsledek: A - přijato, R - zamítnuto,
                                      jinak zmatečné hlasování
    nazev_dlouhy    char(X)           Dlouhý název bodu hlasování
    nazev_kratky    char(X)           Krátký název bodu hlasování
    ==============  ================  =====================================

    """
    HLASOVANI_CHOICES = (
        ('N', 'normální'),
        ('R', 'ruční'),
        )

    VYSLEDEK_CHOICES = (
        ('A', 'přijato'),
        ('R', 'zamítnuto'),
        )

    schuze = models.IntegerField()
    cislo = models.IntegerField()
    bod = models.IntegerField()
    datum = models.DateTimeField()
    pro = models.IntegerField()
    proti = models.IntegerField()
    zdrzel = models.IntegerField()
    nehlasoval = models.IntegerField()
    prihlaseno = models.IntegerField()
    kvorum = models.IntegerField()
    druh_hlasovani = models.CharField(max_length=1, choices=HLASOVANI_CHOICES)
    vysledek = models.CharField(max_length=1, choices=VYSLEDEK_CHOICES)
    nazev_dlouhy = models.CharField(max_length=100, blank=True)
    nazev_kratky = models.CharField(max_length=100, blank=True)

    organ = models.ForeignKey(Organ)

class HlasovaniPoslanec(models.Model):
    """
    ============  =======  ================================================
    Sloupec       Typ      Použití a vazby
    ============  =======  ================================================
    id_poslanec   int      Identifikátor poslance, viz poslanec:id_poslanec
    id_hlasovani  int      Identifikátor hlasování,
                           viz hl_hlasovani:id_hlasovani
    vysledek      char(X)  Hlasování jednotlivého poslance. 'A' - ano,
                           'B' - ne, 'C' - zdržel se (stiskl tlačítko X),
                           'F' - nehlasoval (byl přihlášen, ale nestiskl
                           žádné tlačítko), '@' - nepřihlášen,
                           'M' - omluven. Viz úvodní vysvětlení zpracování
                           výsledků hlasování.
    ============  =======  ================================================

    """
    VYSLEDEK_CHOICES = (
        ('A', 'ano'),
        ('B', 'ne'),
        ('C', 'zdržel se'),
        ('F', 'nehlasoval'),
        ('@', 'nepřihlášen'),
        ('M', 'omluven')
    )

    vysledek = models.CharField(max_length=1)

    poslanec = models.ForeignKey(Poslanec)
    hlasovani = models.ForeignKey(Hlasovani)

    class Meta:
        unique_together = (("poslanec", "hlasovani"),
            )
