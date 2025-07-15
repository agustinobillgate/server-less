#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ba_cancreslinebl import ba_cancreslinebl
from models import Bk_reser, Bk_veran, B_storno, Bediener, Res_history

def ba_plan_res_cancel4bl(b1_resnr:int, b1_reslinnr:int, t_resnr:int, t_reslinnr:int, cancel_str:string, user_init:string):

    prepare_cache ([Bk_reser, Bk_veran, B_storno, Bediener, Res_history])

    curr_resnr = 0
    datum = None
    raum = ""
    von_zeit = ""
    bis_zeit = ""
    resstatus = 0
    bk_reser = bk_veran = b_storno = bediener = res_history = None

    resline = mainres = None

    Resline = create_buffer("Resline",Bk_reser)
    Mainres = create_buffer("Mainres",Bk_veran)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_resnr, datum, raum, von_zeit, bis_zeit, resstatus, bk_reser, bk_veran, b_storno, bediener, res_history
        nonlocal b1_resnr, b1_reslinnr, t_resnr, t_reslinnr, cancel_str, user_init
        nonlocal resline, mainres


        nonlocal resline, mainres

        return {"b1_resnr": b1_resnr, "b1_reslinnr": b1_reslinnr, "curr_resnr": curr_resnr, "datum": datum, "raum": raum, "von_zeit": von_zeit, "bis_zeit": bis_zeit, "resstatus": resstatus}


    resline = get_cache (Bk_reser, {"veran_nr": [(eq, t_resnr)],"veran_resnr": [(eq, t_reslinnr)]})

    if resline:
        datum = resline.datum
        raum = resline.raum
        von_zeit = resline.von_zeit
        bis_zeit = resline.bis_zeit
        resstatus = resline.resstatus

        mainres = get_cache (Bk_veran, {"veran_nr": [(eq, resline.veran_nr)]})

        b_storno = get_cache (B_storno, {"bankettnr": [(eq, resline.veran_nr)],"breslinnr": [(eq, resline.veran_resnr)]})

        if not b_storno:
            b_storno = B_storno()
            db_session.add(b_storno)

            b_storno.bankettnr = resline.veran_nr
            b_storno.breslinnr = resline.veran_resnr
            b_storno.gastnr = mainres.gastnr
            b_storno.betrieb_gast = mainres.gastnrver
            b_storno.datum = resline.datum
        b_storno.grund[17] = cancel_str.upper() + " D*" + to_string(get_current_date(), "99/99/99") + " " + to_string(get_current_time_in_seconds(), "hh:mm:ss") + " " + resline.raum
        b_storno.usercode = user_init
        curr_resnr = 0

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Cancel Banquet No: " + to_string(resline.veran_nr) + " Venue: " + resline.raum + " Reason: " + cancel_str
        res_history.action = "Banquet"


        pass
        pass
        get_output(ba_cancreslinebl(resline.veran_nr, resline.veran_resnr))

        mainres = get_cache (Bk_veran, {"veran_nr": [(eq, b1_resnr)]})

        if not mainres:
            b1_resnr = 0
            b1_reslinnr = 0

    return generate_output()