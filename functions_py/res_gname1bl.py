#using conversion tools version: 1.0.0.117

# =========================================================================
# Rulita, 09-12-2025
# - Fixing error cannot assign or edit guest name
# - Issue casetype send via ui casetype 4 but progress casetype 4 not found
# - else condition fo casetype 1 & 4
# =========================================================================

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Guest

def res_gname1bl(case_type:int, famname:string, name1:string, gname:string):

    prepare_cache ([Guest])

    guest1_data = []
    guest = None

    guest1 = None

    guest1_data, Guest1 = create_model("Guest1", {"gastnr":int, "name":string, "vorname1":string, "anrede1":string, "nation1":string, "wohnort":string, "land":string, "adresse1":string, "telefon":string, "ausweis_nr1":string})

    db_session = local_storage.db_session

    famname = famname.strip()
    name1 = name1.strip()
    gname = gname.strip()

    def generate_output():
        nonlocal guest1_data, guest
        nonlocal case_type, famname, name1, gname


        nonlocal guest1
        nonlocal guest1_data

        return {"guest1": guest1_data}

    # Rulita, 09-12-2025
    # - Fixing error cannot assign or edit guest name
    # - Issue casetype send via ui casetype 4 but progress casetype 4 not found
    # if case_type == 1:

    #     for guest in db_session.query(Guest).filter(
    #              (matches((Guest.name + Guest.vorname1),famname)) & (Guest.vorname1 >= (name1).lower()) & (Guest.karteityp == 0) & (Guest.gastnr > 0)).order_by(Guest.name).all():
    #         guest1 = Guest1()
    #         guest1_data.append(guest1)

    #         guest1.gastnr = guest.gastnr
    #         guest1.name = guest.name
    #         guest1.vorname1 = guest.vorname1
    #         guest1.anrede1 = guest.anrede1
    #         guest1.nation1 = guest.nation1
    #         guest1.wohnort = guest.wohnort
    #         guest1.land = guest.land
    #         guest1.adresse1 = guest.adresse1
    #         guest1.telefon = guest.telefon
    #         guest1.ausweis_nr1 = guest.ausweis_nr1


    # elif case_type == 2:
    if case_type == 2:

        for guest in db_session.query(Guest).filter(
                 (Guest.name == (gname).lower()) & (Guest.vorname1 >= (name1).lower()) & (Guest.karteityp == 0) & (Guest.gastnr > 0)).order_by(Guest.name).all():
            guest1 = Guest1()
            guest1_data.append(guest1)

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
                 (Guest.name == (gname).lower()) & (Guest.vorname1 == (name1).lower()) & (Guest.karteityp == 0) & (Guest.gastnr > 0)).order_by(Guest.name).all():
            guest1 = Guest1()
            guest1_data.append(guest1)

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

    # Rulita, 09-12-2025
    # - else condition fo casetype 1 & 4
    else:
        for guest in db_session.query(Guest).filter(
                 (func.like((Guest.name + Guest.vorname1).collate("C"),f"%{famname}%")) & (Guest.vorname1 >= (name1).lower()) & (Guest.karteityp == 0) & (Guest.gastnr > 0)).order_by(Guest.name).all():
            guest1 = Guest1()
            guest1_data.append(guest1)

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