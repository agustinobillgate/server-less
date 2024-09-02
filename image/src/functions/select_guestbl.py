from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest

def select_guestbl(sorttype:int, curr_name:str):
    t_guest_list = []
    to_name:str = ""
    guest = None

    t_guest = None

    t_guest_list, T_guest = create_model("T_guest", {"gastnr":int, "name":str, "anredefirma":str, "wohnort":str, "adresse1":str, "vorname1":str, "anrede1":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_guest_list, to_name, guest


        nonlocal t_guest
        nonlocal t_guest_list
        return {"t-guest": t_guest_list}

    if ord(substring(curr_name, 0, 1)) <= 255:
        to_name = substring(curr_name, 0, 1) + "zzzz"

    if substring(curr_name, 0, 1) == "*":

        for guest in db_session.query(Guest).filter(
                (Guest.name.op("~")(curr_name)) &  (Guest.karteityp == sorttype) &  (Guest.gastnr > 0)).all():
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            t_guest.gastnr = guest.gastnr
            t_guest.name = guest.name
            t_guest.anredefirma = guest.anredefirma
            t_guest.wohnort = guest.wohnort
            t_guest.adresse1 = guest.adresse1
            t_guest.vorname1 = guest.vorname1
            t_guest.anrede1 = guest.anrede1


    elif to_name != "":

        for guest in db_session.query(Guest).filter(
                (func.lower(Guest.name) >= (curr_name).lower()) &  (func.lower(Guest.name) <= (to_name).lower()) &  (Guest.karteityp == sorttype) &  (Guest.gastnr > 0)).all():
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            t_guest.gastnr = guest.gastnr
            t_guest.name = guest.name
            t_guest.anredefirma = guest.anredefirma
            t_guest.wohnort = guest.wohnort
            t_guest.adresse1 = guest.adresse1
            t_guest.vorname1 = guest.vorname1
            t_guest.anrede1 = guest.anrede1

    else:

        for guest in db_session.query(Guest).filter(
                (func.lower(Guest.name) >= (curr_name).lower()) &  (Guest.karteityp == sorttype) &  (Guest.gastnr > 0)).all():
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            t_guest.gastnr = guest.gastnr
            t_guest.name = guest.name
            t_guest.anredefirma = guest.anredefirma
            t_guest.wohnort = guest.wohnort
            t_guest.adresse1 = guest.adresse1
            t_guest.vorname1 = guest.vorname1
            t_guest.anrede1 = guest.anrede1


    return generate_output()