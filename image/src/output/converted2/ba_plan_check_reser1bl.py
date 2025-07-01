#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser

def ba_plan_check_reser1bl(rml_raum:string, rsv_date:date, rsv_i:int):

    prepare_cache ([Bk_reser])

    t_bk_reser_list = []
    bk_reser = None

    t_bk_reser = None

    t_bk_reser_list, T_bk_reser = create_model("T_bk_reser", {"resstatus":int, "veran_nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bk_reser_list, bk_reser
        nonlocal rml_raum, rsv_date, rsv_i


        nonlocal t_bk_reser
        nonlocal t_bk_reser_list

        return {"t-bk-reser": t_bk_reser_list}

    for bk_reser in db_session.query(Bk_reser).filter(
             (Bk_reser.raum == (rml_raum).lower()) & (Bk_reser.datum == rsv_date) & (rsv_i >= Bk_reser.von_i) & (rsv_i <= Bk_reser.bis_i) & (Bk_reser.resstatus <= 2)).order_by(Bk_reser._recid).all():
        t_bk_reser = T_bk_reser()
        t_bk_reser_list.append(t_bk_reser)

        t_bk_reser.resstatus = bk_reser.resstatus
        t_bk_reser.veran_nr = bk_reser.veran_nr

    return generate_output()