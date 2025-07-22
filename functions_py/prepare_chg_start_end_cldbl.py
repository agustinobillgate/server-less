#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 22/7/2025
# gitlab: 
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser, Htparam, Bk_raum

def prepare_chg_start_end_cldbl(resnr:int, reslinnr:int, curr_date:date):

    prepare_cache ([Htparam, Bk_raum])

    chg_date = None
    ci_date = None
    update_ok = False
    begin_i2 = 0
    ending_i2 = 0
    begin_time = ""
    begin_i = 0
    ending_time = ""
    ending_i = 0
    msg = 0
    t_rsv_table_data = []
    t_bk_reser_data = []
    i:int = 0
    s:int = 0
    bk_reser = htparam = bk_raum = None

    t_rsv_table = t_bk_reser = rsv_table = None

    t_rsv_table_data, T_rsv_table = create_model_like(Bk_reser, {"rec_id":int, "t_vorbereit":int})
    t_bk_reser_data, T_bk_reser = create_model_like(Bk_reser, {"rec_id":int})

    Rsv_table = create_buffer("Rsv_table",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal chg_date, ci_date, update_ok, begin_i2, ending_i2, begin_time, begin_i, ending_time, ending_i, msg, t_rsv_table_data, t_bk_reser_data, i, s, bk_reser, htparam, bk_raum
        nonlocal resnr, reslinnr, curr_date
        nonlocal rsv_table


        nonlocal t_rsv_table, t_bk_reser, rsv_table
        nonlocal t_rsv_table_data, t_bk_reser_data

        return {"chg_date": chg_date, "ci_date": ci_date, "update_ok": update_ok, "begin_i2": begin_i2, "ending_i2": ending_i2, "begin_time": begin_time, "begin_i": begin_i, "ending_time": ending_time, "ending_i": ending_i, "msg": msg, "t-rsv-table": t_rsv_table_data, "t-bk-reser": t_bk_reser_data}

    chg_date = curr_date

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    update_ok = False

    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)],"veran_resnr": [(eq, reslinnr)]})

    if bk_reser:

        bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_reser.raum)]})

        # Rd 22/7/2025
        # Add if is not None
        if bk_raum is not None:
            if bk_reser.datum == chg_date and bk_reser.bis_datum == chg_date:
                i = (((bk_raum.vorbereit + 0.1) * 2) + 1) / 60
                begin_i2 = bk_reser.von_i - i
                begin_time = bk_reser.von_zeit
                begin_i = bk_reser.von_i
                ending_time = bk_reser.bis_zeit
                ending_i = bk_reser.bis_i
                s = (((bk_raum.vorbereit + 0.1) * 2) + 1) / 60
                ending_i2 = bk_reser.bis_i + s
                msg = 1

            elif bk_reser.datum == chg_date and bk_reser.bis_datum > chg_date:
                begin_time = bk_reser.von_zeit
                i = (((bk_raum.vorbereit + 0.1) * 2) + 1) / 60
                begin_i = bk_reser.von_i
                begin_i2 = bk_reser.von_i - i
                ending_time = "24:00"
                ending_i = 48
                msg = 2

            elif bk_reser.datum < chg_date and bk_reser.bis_datum == chg_date:
                begin_time = "00:00"
                begin_i = 1
                ending_time = bk_reser.bis_zeit
                s = (((bk_raum.vorbereit + 0.1) * 2) + 1) / 60
                ending_i2 = bk_reser.bis_i + s
                ending_i = bk_reser.bis_i
                msg = 3

            elif bk_reser.datum < chg_date and bk_reser.bis_datum > chg_date:
                begin_time = "00:00"
                begin_i = 1
                ending_time = "24:00"
                ending_i = 48
    else:
        msg = 4

    if bk_reser:
        t_bk_reser = T_bk_reser()
        t_bk_reser_data.append(t_bk_reser)

        buffer_copy(bk_reser, t_bk_reser)
        t_bk_reser.rec_id = bk_reser._recid

    return generate_output()