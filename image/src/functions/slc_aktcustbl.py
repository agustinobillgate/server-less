from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Akt_kont, Guest

def slc_aktcustbl(gname:str, user_init:str, sorttype:int):
    gast_list = []
    akt_kont = guest = None

    gast = None

    gast_list, Gast = create_model("Gast", {"gastnr":int, "name":str, "vorname1":str, "anrede1":str, "anredefirma":str, "adresse":str, "plz":str, "wohnort":str, "phonetik3":str, "karteityp":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gast_list, akt_kont, guest


        nonlocal gast
        nonlocal gast_list
        return {"gast": gast_list}

    if sorttype == 0:

        guest_obj_list = []
        for guest, akt_kont in db_session.query(Guest, Akt_kont).join(Akt_kont,(Akt_kont.gastnr == Guest.gastnr)).filter(
                (func.lower(Guest.name) >= (gname).lower()) &  (Guest.gastnr > 0) &  (Guest.karteityp == sorttype)).all():
            if guest._recid in guest_obj_list:
                continue
            else:
                guest_obj_list.append(guest._recid)


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
                (func.lower(Guest.name) >= (gname).lower()) &  (Guest.gastnr > 0) &  (func.lower(Guest.phonetik3) == (user_init).lower()) &  (Guest.karteityp == sorttype)).all():
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