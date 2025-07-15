#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Akt_kont

def prepare_sls_detailbl(inp_gastnr:int):

    prepare_cache ([Guest, Akt_kont])

    lname = ""
    namekontakt = ""
    guest1_data = []
    akt_kont1_data = []
    guest = akt_kont = None

    guest1 = akt_kont1 = None

    guest1_data, Guest1 = create_model_like(Guest)
    akt_kont1_data, Akt_kont1 = create_model_like(Akt_kont)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lname, namekontakt, guest1_data, akt_kont1_data, guest, akt_kont
        nonlocal inp_gastnr


        nonlocal guest1, akt_kont1
        nonlocal guest1_data, akt_kont1_data

        return {"lname": lname, "namekontakt": namekontakt, "guest1": guest1_data, "akt-kont1": akt_kont1_data}

    guest1 = Guest1()
    guest1_data.append(guest1)

    akt_kont1 = Akt_kont1()
    akt_kont1_data.append(akt_kont1)


    guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})

    if guest:
        guest1.gastnr = guest.gastnr
        lname = guest.name + ", " + guest.anredefirma
        guest1.adresse1 = guest.adresse1
        guest1.adresse2 = guest.adresse2
        guest1.adresse3 = guest.adresse3
        guest1.wohnort = guest.wohnort
        guest1.plz = guest.plz
        guest1.land = guest.land
        guest1.telefon = guest.telefon
        guest1.fax = guest.fax
        guest1.email_adr = guest.email_adr

    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, inp_gastnr)],"hauptkontakt": [(eq, True)]})

    if akt_kont:
        namekontakt = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede
        akt_kont1.geburtdatum1 = akt_kont.geburtdatum1
        akt_kont1.geburt_ort1 = akt_kont.geburt_ort1
        akt_kont1.telefon = akt_kont.telefon
        akt_kont1.durchwahl = akt_kont.durchwahl
        akt_kont1.abteilung = akt_kont.abteilung
        akt_kont1.funktion = akt_kont.funktion
        akt_kont1.email_adr = akt_kont.email_adr

    return generate_output()