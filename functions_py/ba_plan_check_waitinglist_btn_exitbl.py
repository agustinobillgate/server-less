#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser, Bk_func

def ba_plan_check_waitinglist_btn_exitbl(rec_id:int):

    prepare_cache ([Bk_reser, Bk_func])

    bk_reser = bk_func = None

    resline = bf = None

    Resline = create_buffer("Resline",Bk_reser)
    Bf = create_buffer("Bf",Bk_func)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_reser, bk_func
        nonlocal rec_id
        nonlocal resline, bf


        nonlocal resline, bf

        return {}


    # resline = get_cache (Bk_reser, {"_recid": [(eq, rec_id)]})
    resline = db_session.query(Resline).filter(
             (Resline._recid == rec_id)).with_for_update().first()
    resline.resstatus = 2

    # bf = get_cache (Bk_func, {"veran_nr": [(eq, resline.veran_nr)],"veran_seite": [(eq, resline.veran_seite)]})
    bf = db_session.query(Bf).filter(
             (Bf.veran_nr == resline.veran_nr) &
             (Bf.veran_seite == resline.veran_seite)).with_for_update().first()

    if bf.veran_seite > 8:
        bf.c_resstatus[0] = "T"
        bf.r_resstatus[0] = 2
        bf.resstatus = 2


    else:
        bf.c_resstatus[bf.veran_seite - 1] = "T"
        bf.r_resstatus[bf.veran_seite - 1] = 2
        bf.resstatus = 2


    pass

    return generate_output()