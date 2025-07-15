#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.connect_groupbl import connect_groupbl
from functions.read_reservationbl import read_reservationbl
from functions.read_res_linebl import read_res_linebl
from functions.read_guestbl import read_guestbl
from models import Res_line, Reservation, Guest

def prepare_connect_groupbl(resno:int, reslinno:int):
    res_list_data = []
    mainres_list_data = []
    guest_list_data = []
    t_reservation_data = []
    t_guest_data = []
    res_line = reservation = guest = None

    res_list = mainres_list = guest_list = t_reservation = t_res_line = t_guest = None

    res_list_data, Res_list = create_model_like(Res_line, {"kurzbez":string, "groupname":string, "join_flag":bool, "mbill_flag":bool, "prev_join":bool, "prev_mbill":bool})
    mainres_list_data, Mainres_list = create_model("Mainres_list", {"gastnr":int, "resnr":int, "actflag":int, "zimanz":int, "ankunft":date, "abreise":date, "segm":int, "deposit":Decimal, "until":date, "paid":Decimal, "id1":string, "id2":string, "id2_date":date, "groupname":string, "grpflag":bool, "bemerk":string, "arrival":bool, "resident":bool, "arr_today":bool})
    guest_list_data, Guest_list = create_model("Guest_list", {"gastnr":int, "name":string, "anredefirma":string, "wohnort":string, "karteityp":int})
    t_reservation_data, T_reservation = create_model_like(Reservation)
    t_res_line_data, T_res_line = create_model_like(Res_line)
    t_guest_data, T_guest = create_model_like(Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_list_data, mainres_list_data, guest_list_data, t_reservation_data, t_guest_data, res_line, reservation, guest
        nonlocal resno, reslinno


        nonlocal res_list, mainres_list, guest_list, t_reservation, t_res_line, t_guest
        nonlocal res_list_data, mainres_list_data, guest_list_data, t_reservation_data, t_res_line_data, t_guest_data

        return {"res-list": res_list_data, "mainres-list": mainres_list_data, "guest-list": guest_list_data, "t-reservation": t_reservation_data, "t-guest": t_guest_data}


    if resno != 0:
        res_list_data, mainres_list_data, guest_list_data = get_output(connect_groupbl(1, resno, reslinno, None, None, None, None))
        t_reservation_data = get_output(read_reservationbl(1, resno, None, ""))

        t_reservation = query(t_reservation_data, first=True)

        if t_reservation:
            t_res_line_data = get_output(read_res_linebl(1, resno, reslinno, 0, 0, "", None, None, 0, 0, ""))

            t_res_line = query(t_res_line_data, first=True)

            if t_res_line:
                t_guest_data = get_output(read_guestbl(1, t_reservation.gastnr, "", ""))

    return generate_output()