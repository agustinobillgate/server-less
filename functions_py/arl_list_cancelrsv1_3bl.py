#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 25-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from functions.del_reservebl import del_reservebl
from models import Reservation, Res_line, Reslin_queasy

def arl_list_cancelrsv1_3bl(pvilanguage:int, arl_list_resnr:int, cancel_str:string, user_init:string):

    prepare_cache ([Reservation, Reslin_queasy])

    done = False
    msg_str = ""
    reservation = res_line = reslin_queasy = None

    mainres = r_line = None

    Mainres = create_buffer("Mainres",Reservation)
    R_line = create_buffer("R_line",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, msg_str, reservation, res_line, reslin_queasy
        nonlocal pvilanguage, arl_list_resnr, cancel_str, user_init
        nonlocal mainres, r_line


        nonlocal mainres, r_line

        return {"done": done, "msg_str": msg_str}


    # mainres = get_cache (Reservation, {"resnr": [(eq, arl_list_resnr)]})
    mainres = db_session.query(Reservation).filter(Reservation.resnr == arl_list_resnr).with_for_update().first()
    pass

    if cancel_str != "":
        mainres.vesrdepot2 = cancel_str
    pass
    db_session.refresh(mainres, with_for_update=True)

    r_line = db_session.query(R_line).filter(
                 (R_line.resnr == arl_list_resnr) & (R_line.active_flag == 0) & (R_line.l_zuordnung[inc_value(2)] == 0)).first()
    while None != r_line:
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = r_line.resnr
        reslin_queasy.reslinnr = r_line.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(r_line.ankunft) + ";" + to_string(r_line.ankunft) + ";" + to_string(r_line.abreise) + ";" + to_string(r_line.abreise) + ";" + to_string(r_line.zimmeranz) + ";" + to_string(r_line.zimmeranz) + ";" + to_string(r_line.erwachs) + ";" + to_string(r_line.erwachs) + ";" + to_string(r_line.kind1) + ";" + to_string(r_line.kind1) + ";" + to_string(r_line.gratis) + ";" + to_string(r_line.gratis) + ";" + to_string(r_line.zikatnr) + ";" + to_string(r_line.zikatnr) + ";" + to_string(r_line.zinr) + ";" + to_string(r_line.zinr) + ";" + to_string(r_line.arrangement) + ";" + to_string(r_line.arrangement) + ";" + to_string(r_line.zipreis) + ";" + to_string(r_line.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(r_line.name) + ";" + to_string("CANCEL RSV") + ";" + to_string(" ") + ";" + to_string(" ") + ";"

        curr_recid = r_line._recid
        r_line = db_session.query(R_line).filter(
                     (R_line.resnr == arl_list_resnr) & (R_line.active_flag == 0) & (R_line.l_zuordnung[inc_value(2)] == 0) & (R_line._recid > curr_recid)).first()
    pass
    pass
    msg_str = get_output(del_reservebl(pvilanguage, "cancel", arl_list_resnr, user_init, cancel_str))
    done = True

    return generate_output()