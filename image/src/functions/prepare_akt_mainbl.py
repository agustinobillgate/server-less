from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Akt_cust

def prepare_akt_mainbl(user_init:str, lname:str):
    q1_list_list = []
    guest = akt_cust = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"name":str, "anredefirma":str, "anrede1":str, "firmen_nr":int, "adresse1":str, "plz":str, "wohnort":str, "telefon":str, "fax":str, "rabatt":decimal, "endperiode":date, "namekontakt":str, "gastnr":int, "userinit":str, "datum":date, "c_init":str, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, guest, akt_cust


        nonlocal q1_list
        nonlocal q1_list_list
        return {"q1-list": q1_list_list}

    akt_cust_obj_list = []
    for akt_cust, guest in db_session.query(Akt_cust, Guest).join(Guest,(Guest.gastnr == Akt_cust.gastnr) &  (Guest.phonetik3 == Akt_cust.userinit) &  (func.lower(Guest.name) >= (lname).lower()) &  (Guest.gastnr > 0)).filter(
            (func.lower(Akt_cust.userinit) == (user_init).lower())).all():
        if akt_cust._recid in akt_cust_obj_list:
            continue
        else:
            akt_cust_obj_list.append(akt_cust._recid)


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
        q1_list.rabatt = guest.rabatt
        q1_list.endperiode = guest.endperiode
        q1_list.namekontakt = guest.namekontakt
        q1_list.gastnr = akt_cust.gastnr
        q1_list.userinit = akt_cust.userinit
        q1_list.datum = akt_cust.datum
        q1_list.c_init = akt_cust.c_init
        q1_list.rec_id = akt_cust._recid

    return generate_output()