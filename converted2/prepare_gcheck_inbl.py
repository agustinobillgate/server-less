#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.htpdate import htpdate
from functions.gcheck_inbl import gcheck_inbl
from models import Reservation

def prepare_gcheck_inbl(input_resnr:int):
    i_slist2 = 0
    ci_date = None
    t_reservation_data = []
    gcheck_in_data = []
    reservation = None

    t_reservation = gcheck_in = None

    t_reservation_data, T_reservation = create_model_like(Reservation)
    gcheck_in_data, Gcheck_in = create_model("Gcheck_in", {"resnr":int, "zinr":string, "name":string, "abreise":date, "anztage":int, "zimmeranz":int, "kurzbez":string, "erwachs":int, "gratis":int, "resstatus":int, "arrangement":string, "zipreis":Decimal, "wabkurz":string, "l_zuordnung":int, "ankzeit":int, "gastnr":int, "reslinnr":int, "gastnrmember":int, "grpflag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i_slist2, ci_date, t_reservation_data, gcheck_in_data, reservation
        nonlocal input_resnr


        nonlocal t_reservation, gcheck_in
        nonlocal t_reservation_data, gcheck_in_data

        return {"i_slist2": i_slist2, "ci_date": ci_date, "t-reservation": t_reservation_data, "gcheck-in": gcheck_in_data}

    i_slist2 = get_output(htpint(297))
    ci_date = get_output(htpdate(87))

    reservation = get_cache (Reservation, {"resnr": [(eq, input_resnr)]})
    t_reservation = T_reservation()
    t_reservation_data.append(t_reservation)

    buffer_copy(reservation, t_reservation)
    gcheck_in_data = get_output(gcheck_inbl(input_resnr, ci_date))

    return generate_output()