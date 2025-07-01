#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Guest

def slc_aktcust_searchwebbl(search1:string, user_init:string, sorttype:int):

    prepare_cache ([Guest])

    gast_list = []
    guest = None

    gast = None

    gast_list, Gast = create_model("Gast", {"gastnr":int, "name":string, "vorname1":string, "anrede1":string, "anredefirma":string, "adresse":string, "plz":string, "wohnort":string, "phonetik3":string, "karteityp":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gast_list, guest
        nonlocal search1, user_init, sorttype


        nonlocal gast
        nonlocal gast_list

        return {"gast": gast_list}

    if search1 == "":

        for guest in db_session.query(Guest).filter(
                 (Guest.name >= (search1).lower()) & (Guest.gastnr > 0) & (Guest.phonetik3 == (user_init).lower()) & (Guest.karteityp == sorttype)).order_by(Guest.name).all():
            gast = Gast()
            gast_list.append(gast)

            gast.gastnr = guest.gastnr
            gast.name = guest.name
            gast.vorname1 = guest.vorname1
            gast.anrede1 = guest.anrede1
            gast.anredefirma = guest.anredefirma
            gast.adresse = (guest.adresse1 + "," + guest.adresse2 + "," + guest.adresse3)
            gast.plz = guest.plz
            gast.wohnort = guest.wohnort
            gast.phonetik3 = guest.phonetik3
            gast.karteityp = guest.karteityp


    else:

        for guest in db_session.query(Guest).filter(
                 (matches(Guest.name,("*" + search1 + "*"))) & (Guest.gastnr > 0) & (Guest.phonetik3 == (user_init).lower()) & (Guest.karteityp == sorttype)).order_by(Guest.name).all():
            gast = Gast()
            gast_list.append(gast)

            gast.gastnr = guest.gastnr
            gast.name = guest.name
            gast.vorname1 = guest.vorname1
            gast.anrede1 = guest.anrede1
            gast.anredefirma = guest.anredefirma
            gast.adresse = (guest.adresse1 + "," + guest.adresse2 + "," + guest.adresse3)
            gast.plz = guest.plz
            gast.wohnort = guest.wohnort
            gast.phonetik3 = guest.phonetik3
            gast.karteityp = guest.karteityp

    return generate_output()