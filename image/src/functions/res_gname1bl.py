from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest

def res_gname1bl(case_type:int, famname:str, name1:str, gname:str):
    guest1_list = []
    guest = None

    guest1 = None

    guest1_list, Guest1 = create_model("Guest1", {"gastnr":int, "name":str, "vorname1":str, "anrede1":str, "nation1":str, "wohnort":str, "land":str, "adresse1":str, "telefon":str, "ausweis_nr1":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest1_list, guest


        nonlocal guest1
        nonlocal guest1_list
        return {"guest1": guest1_list}

    if case_type == 1:

        for guest in db_session.query(Guest).filter(
                ((Guest.name + func.lower(Guest.vorname1)) MATCHES famname) &  (func.lower(Guest.vorname1) >= (name1).lower()) &  (Guest.karteityp == 0) &  (Guest.gastnr > 0)).all():
            guest1 = Guest1()
            guest1_list.append(guest1)

            guest1.gastnr = guest.gastnr
            guest1.name = guest.name
            guest1.vorname1 = guest.vorname1
            guest1.anrede1 = guest.anrede1
            guest1.nation1 = guest.nation1
            guest1.wohnort = guest.wohnort
            guest1.land = guest.land
            guest1.adresse1 = guest.adresse1
            guest1.telefon = guest.telefon
            guest1.ausweis_nr1 = guest.ausweis_nr1


    elif case_type == 2:

        for guest in db_session.query(Guest).filter(
                (func.lower(Guest.name) == (gname).lower()) &  (func.lower(Guest.vorname1) >= (name1).lower()) &  (Guest.karteityp == 0) &  (Guest.gastnr > 0)).all():
            guest1 = Guest1()
            guest1_list.append(guest1)

            guest1.gastnr = guest.gastnr
            guest1.name = guest.name
            guest1.vorname1 = guest.vorname1
            guest1.anrede1 = guest.anrede1
            guest1.nation1 = guest.nation1
            guest1.wohnort = guest.wohnort
            guest1.land = guest.land
            guest1.adresse1 = guest.adresse1
            guest1.telefon = guest.telefon
            guest1.ausweis_nr1 = guest.ausweis_nr1


    elif case_type == 3:

        for guest in db_session.query(Guest).filter(
                (func.lower(Guest.name) == (gname).lower()) &  (func.lower(Guest.vorname1) == (name1).lower()) &  (Guest.karteityp == 0) &  (Guest.gastnr > 0)).all():
            guest1 = Guest1()
            guest1_list.append(guest1)

            guest1.gastnr = guest.gastnr
            guest1.name = guest.name
            guest1.vorname1 = guest.vorname1
            guest1.anrede1 = guest.anrede1
            guest1.nation1 = guest.nation1
            guest1.wohnort = guest.wohnort
            guest1.land = guest.land
            guest1.adresse1 = guest.adresse1
            guest1.telefon = guest.telefon
            guest1.ausweis_nr1 = guest.ausweis_nr1


    return generate_output()