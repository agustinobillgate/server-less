#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_func, Bk_reser, Bk_veran
from sqlalchemy.orm import flag_modified

def bqt_cutoff_update_resstatusbl(r_status:int, c_status:string, o_resnr:int, o_reslinnr:int):

    prepare_cache ([Bk_func, Bk_reser, Bk_veran])

    t_output_list_data = []
    bk_func = bk_reser = bk_veran = None

    t_output_list = None

    t_output_list_data, T_output_list = create_model("T_output_list", {"resnr":int, "reslinnr":int, "resstatus":int, "datum":date, "crdate":date, "cutoff":date, "str":string})

    db_session = local_storage.db_session
    c_status = c_status.strip()

    def generate_output():
        nonlocal t_output_list_data, bk_func, bk_reser, bk_veran
        nonlocal r_status, c_status, o_resnr, o_reslinnr


        nonlocal t_output_list
        nonlocal t_output_list_data

        return {"t-output-list": t_output_list_data}

    def update_resstatus():

        nonlocal t_output_list_data, bk_func, bk_reser, bk_veran
        nonlocal r_status, c_status, o_resnr, o_reslinnr


        nonlocal t_output_list
        nonlocal t_output_list_data

        # bk_func = get_cache (Bk_func, {"veran_nr": [(eq, o_resnr)],"veran_seite": [(eq, o_reslinnr)]})
        bk_func = db_session.query(Bk_func).filter(
                 (Bk_func.veran_nr == o_resnr) &
                 (Bk_func.veran_seite == o_reslinnr)).with_for_update().first()
        
        bk_func.resstatus = r_status
        bk_func.r_resstatus[0] = r_status
        bk_func.c_resstatus[0] = c_status
        flag_modified(bk_func, "r_resstatus")
        flag_modified(bk_func, "c_resstatus")

        pass

        # bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, o_resnr)],"veran_seite": [(eq, o_reslinnr)]})
        bk_reser = db_session.query(Bk_reser).filter(
                 (Bk_reser.veran_nr == o_resnr) &
                 (Bk_reser.veran_seite == o_reslinnr)).with_for_update().first()
        
        bk_reser.resstatus = r_status


        pass

        # bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, o_resnr)]})
        bk_veran = db_session.query(Bk_veran).filter(
                 (Bk_veran.veran_nr == o_resnr)).with_for_update().first()
        bk_veran.resstatus = r_status


        pass
        t_output_list = T_output_list()
        t_output_list_data.append(t_output_list)

        t_output_list.str = to_string(bk_func.bis_datum, "99/99/99") +\
                to_string(bk_func.bestellt__durch, "x(32)") +\
                to_string(bk_func.v_kontaktperson[0], "x(32)") +\
                to_string(bk_func.zweck[0], "x(18)") +\
                to_string(bk_func.raeume[0], "x(12)") +\
                to_string(bk_func.uhrzeit, "x(13)") +\
                to_string(bk_func.personen, ">,>>>") +\
                to_string(bk_veran.deposit, ">>>,>>>,>>9") +\
                to_string(bk_veran.total_paid, ">>>,>>>,>>9") +\
                to_string(bk_func.vgeschrieben, "x(2)") +\
                to_string(bk_func.veran_nr, ">>>,>>>") +\
                to_string(bk_func.veran_seite, ">>>") +\
                to_string(bk_func.c_resstatus[0], "x(1)")
        t_output_list.resnr = bk_func.veran_nr
        t_output_list.reslinnr = bk_func.veran_seite
        t_output_list.resstatus = bk_func.resstatus

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)]})

        if bk_reser:
            t_output_list.cutoff = bk_reser.limitdate

    update_resstatus()

    return generate_output()