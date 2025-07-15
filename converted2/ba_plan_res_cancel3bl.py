#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ba_cancreslinebl import ba_cancreslinebl
from models import Bk_veran, B_storno, Bediener, Res_history

def ba_plan_res_cancel3bl(b1_resnr:int, b1_reslinnr:int, t_veran_nr:int, t_veran_resnr:int, t_datum:date, t_raum:string, cancel_str:string, user_init:string):

    prepare_cache ([Bk_veran, B_storno, Bediener, Res_history])

    curr_resnr = 0
    bk_veran = b_storno = bediener = res_history = None

    mainres = None

    Mainres = create_buffer("Mainres",Bk_veran)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_resnr, bk_veran, b_storno, bediener, res_history
        nonlocal b1_resnr, b1_reslinnr, t_veran_nr, t_veran_resnr, t_datum, t_raum, cancel_str, user_init
        nonlocal mainres


        nonlocal mainres

        return {"b1_resnr": b1_resnr, "b1_reslinnr": b1_reslinnr, "curr_resnr": curr_resnr}


    mainres = get_cache (Bk_veran, {"veran_nr": [(eq, t_veran_nr)]})

    b_storno = get_cache (B_storno, {"bankettnr": [(eq, t_veran_nr)],"breslinnr": [(eq, t_veran_resnr)]})

    if not b_storno:
        b_storno = B_storno()
        db_session.add(b_storno)

        b_storno.bankettnr = t_veran_nr
        b_storno.breslinnr = t_veran_resnr
        b_storno.gastnr = mainres.gastnr
        b_storno.betrieb_gast = mainres.gastnrver
        b_storno.datum = t_datum
    b_storno.grund[17] = cancel_str.upper() + " D*" + to_string(get_current_date(), "99/99/99") + " " + to_string(get_current_time_in_seconds(), "hh:mm:ss") + " " + t_raum
    b_storno.usercode = user_init
    curr_resnr = 0

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Cancel Banquet No: " + to_string(t_veran_nr) + " Venue: " + t_raum + " Reason: " + cancel_str
    res_history.action = "Banquet"


    pass
    pass
    get_output(ba_cancreslinebl(t_veran_nr, t_veran_resnr))

    mainres = get_cache (Bk_veran, {"veran_nr": [(eq, b1_resnr)]})

    if not mainres:
        b1_resnr = 0
        b1_reslinnr = 0

    return generate_output()