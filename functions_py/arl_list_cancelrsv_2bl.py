#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 25-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from functions.del_reslinebl import del_reslinebl
from models import Reservation, Res_line, Reslin_queasy

def arl_list_cancelrsv_2bl(pvilanguage:int, arl_list_resnr:int, arl_list_reslinnr:int, cancel_str:string, user_init:string):

    prepare_cache ([Reservation, Res_line, Reslin_queasy])

    done = False
    del_mainres = False
    msg_str = ""
    lvcarea:string = "arl-list"
    reservation = res_line = reslin_queasy = None

    mainres = r_line = None

    Mainres = create_buffer("Mainres",Reservation)
    R_line = create_buffer("R_line",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, del_mainres, msg_str, lvcarea, reservation, res_line, reslin_queasy
        nonlocal pvilanguage, arl_list_resnr, arl_list_reslinnr, cancel_str, user_init
        nonlocal mainres, r_line


        nonlocal mainres, r_line

        return {"done": done, "del_mainres": del_mainres, "msg_str": msg_str}


    # mainres = get_cache (Reservation, {"resnr": [(eq, arl_list_resnr)]})
    mainres = db_session.query(Reservation).filter(Reservation.resnr == arl_list_resnr).with_for_update().first()
    pass

    if cancel_str != "":
        mainres.vesrdepot2 = cancel_str
    pass
    db_session.refresh(mainres, with_for_update=False)

    # r_line = get_cache (Res_line, {"resnr": [(eq, arl_list_resnr)],"reslinnr": [(eq, arl_list_reslinnr)]})
    r_line = db_session.query(Res_line).filter(
        (Res_line.resnr == arl_list_resnr) & (Res_line.reslinnr == arl_list_reslinnr)).with_for_update().first()

    if r_line:
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = r_line.resnr
        reslin_queasy.reslinnr = r_line.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(r_line.ankunft) + ";" + to_string(r_line.ankunft) + ";" + to_string(r_line.abreise) + ";" + to_string(r_line.abreise) + ";" + to_string(r_line.zimmeranz) + ";" + to_string(r_line.zimmeranz) + ";" + to_string(r_line.erwachs) + ";" + to_string(r_line.erwachs) + ";" + to_string(r_line.kind1) + ";" + to_string(r_line.kind1) + ";" + to_string(r_line.gratis) + ";" + to_string(r_line.gratis) + ";" + to_string(r_line.zikatnr) + ";" + to_string(r_line.zikatnr) + ";" + to_string(r_line.zinr) + ";" + to_string(r_line.zinr) + ";" + to_string(r_line.arrangement) + ";" + to_string(r_line.arrangement) + ";" + to_string(r_line.zipreis) + ";" + to_string(r_line.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(r_line.name) + ";" + to_string("CANCEL RSV") + ";" + to_string(" ") + ";" + to_string(" ") + ";"

        db_session.refresh(reslin_queasy, with_for_update=True)
        pass
        pass
    del_mainres, msg_str = get_output(del_reslinebl(pvilanguage, "cancel", arl_list_resnr, arl_list_reslinnr, user_init, cancel_str))
    done = True

    return generate_output()