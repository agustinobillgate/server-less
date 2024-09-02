from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from functions.htpdate import htpdate
from functions.gcheck_inbl import gcheck_inbl
from models import Reservation

def prepare_gcheck_inbl(input_resnr:int):
    i_slist2 = 0
    ci_date = None
    t_reservation_list = []
    gcheck_in_list = []
    reservation = None

    t_reservation = gcheck_in = None

    t_reservation_list, T_reservation = create_model_like(Reservation)
    gcheck_in_list, Gcheck_in = create_model("Gcheck_in", {"resnr":int, "zinr":str, "name":str, "abreise":date, "anztage":int, "zimmeranz":int, "kurzbez":str, "erwachs":int, "gratis":int, "resstatus":int, "arrangement":str, "zipreis":decimal, "wabkurz":str, "l_zuordnung":int, "ankzeit":int, "gastnr":int, "reslinnr":int, "gastnrmember":int, "grpflag":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i_slist2, ci_date, t_reservation_list, gcheck_in_list, reservation


        nonlocal t_reservation, gcheck_in
        nonlocal t_reservation_list, gcheck_in_list
        return {"i_slist2": i_slist2, "ci_date": ci_date, "t-reservation": t_reservation_list, "gcheck-in": gcheck_in_list}

    i_slist2 = get_output(htpint(297))
    ci_date = get_output(htpdate(87))

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == input_resnr)).first()
    t_reservation = T_reservation()
    t_reservation_list.append(t_reservation)

    buffer_copy(reservation, t_reservation)
    gcheck_in_list = get_output(gcheck_inbl(input_resnr, ci_date))

    return generate_output()