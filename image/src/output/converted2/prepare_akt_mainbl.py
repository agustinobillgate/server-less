#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Akt_cust

def prepare_akt_mainbl(user_init:string, lname:string):

    prepare_cache ([Guest, Akt_cust])

    q1_list_list = []
    guest = akt_cust = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"name":string, "anredefirma":string, "anrede1":string, "firmen_nr":int, "adresse1":string, "plz":string, "wohnort":string, "telefon":string, "fax":string, "rabatt":Decimal, "endperiode":date, "namekontakt":string, "gastnr":int, "userinit":string, "datum":date, "c_init":string, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, guest, akt_cust
        nonlocal user_init, lname


        nonlocal q1_list
        nonlocal q1_list_list

        return {"q1-list": q1_list_list}

    akt_cust_obj_list = {}
    akt_cust = Akt_cust()
    guest = Guest()
    for akt_cust.gastnr, akt_cust.userinit, akt_cust.datum, akt_cust.c_init, akt_cust._recid, guest.name, guest.anredefirma, guest.anrede1, guest.firmen_nr, guest.adresse1, guest.plz, guest.wohnort, guest.telefon, guest.fax, guest.rabatt, guest.endperiode, guest.namekontakt, guest._recid in db_session.query(Akt_cust.gastnr, Akt_cust.userinit, Akt_cust.datum, Akt_cust.c_init, Akt_cust._recid, Guest.name, Guest.anredefirma, Guest.anrede1, Guest.firmen_nr, Guest.adresse1, Guest.plz, Guest.wohnort, Guest.telefon, Guest.fax, Guest.rabatt, Guest.endperiode, Guest.namekontakt, Guest._recid).join(Guest,(Guest.gastnr == Akt_cust.gastnr) & (Guest.phonetik3 == Akt_cust.userinit) & (Guest.name >= (lname).lower()) & (Guest.gastnr > 0)).filter(
             (Akt_cust.userinit == (user_init).lower())).order_by(Guest.name).all():
        if akt_cust_obj_list.get(akt_cust._recid):
            continue
        else:
            akt_cust_obj_list[akt_cust._recid] = True


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.name = guest.name
        q1_list.anredefirma = guest.anredefirma
        q1_list.anrede1 = guest.anrede1
        q1_list.firmen_nr = guest.firmen_nr
        q1_list.adresse1 = guest.adresse1
        q1_list.plz = guest.plz
        q1_list.wohnort = guest.wohnort
        q1_list.telefon = guest.telefon
        q1_list.fax = guest.fax
        q1_list.rabatt =  to_decimal(guest.rabatt)
        q1_list.endperiode = guest.endperiode
        q1_list.namekontakt = guest.namekontakt
        q1_list.gastnr = akt_cust.gastnr
        q1_list.userinit = akt_cust.userinit
        q1_list.datum = akt_cust.datum
        q1_list.c_init = akt_cust.c_init
        q1_list.rec_id = akt_cust._recid

    return generate_output()