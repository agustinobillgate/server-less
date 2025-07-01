#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reservation, Res_line, Guest

na_list_list, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "bezeich":string, "anz":int})

def update_reservationbl(na_list_list:[Na_list], ci_date:date):

    prepare_cache ([Reservation, Res_line, Guest])

    i = 0
    reservation = res_line = guest = None

    na_list = breserv = None

    Breserv = create_buffer("Breserv",Reservation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, reservation, res_line, guest
        nonlocal ci_date
        nonlocal breserv


        nonlocal na_list, breserv

        return {"na-list": na_list_list, "i": i}

    for res_line in db_session.query(Res_line).filter(
             (Res_line.ankunft == ci_date) & (Res_line.active_flag == 0)).order_by(Res_line._recid).all():

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        if not reservation:

            na_list = query(na_list_list, filters=(lambda na_list: na_list.reihenfolge == 4), first=True)

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
            breserv = Reservation()
            db_session.add(breserv)

            breserv.resnr = res_line.resnr
            breserv.gastnr = guest.gastnr
            breserv.gastnrherk = guest.gastnr
            breserv.name = guest.name
            breserv.herkunft = guest.name + ", " + guest.vorname1 + guest.anredefirma
            i = i + 1
            na_list.anz = na_list.anz + 1


            pass

    return generate_output()