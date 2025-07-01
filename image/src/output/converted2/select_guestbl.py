#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Guest

def select_guestbl(sorttype:int, curr_name:string):

    prepare_cache ([Guest])

    t_guest_list = []
    to_name:string = ""
    guest = None

    t_guest = None

    t_guest_list, T_guest = create_model("T_guest", {"gastnr":int, "name":string, "anredefirma":string, "wohnort":string, "adresse1":string, "vorname1":string, "anrede1":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_guest_list, to_name, guest
        nonlocal sorttype, curr_name


        nonlocal t_guest
        nonlocal t_guest_list

        return {"t-guest": t_guest_list}

    if asc(substring(curr_name, 0, 1)) <= 255:
        to_name = substring(curr_name, 0, 1) + "zzzz"

    if substring(curr_name, 0, 1) == ("*").lower() :

        for guest in db_session.query(Guest).filter(
                 (matches(Guest.name,curr_name)) & (Guest.karteityp == sorttype) & (Guest.gastnr > 0)).order_by(Guest.name).all():
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
                 (Guest.name >= (curr_name).lower()) & (Guest.name <= (to_name).lower()) & (Guest.karteityp == sorttype) & (Guest.gastnr > 0)).order_by(Guest.name).all():
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
                 (Guest.name >= (curr_name).lower()) & (Guest.karteityp == sorttype) & (Guest.gastnr > 0)).order_by(Guest.name).all():
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