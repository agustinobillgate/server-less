#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_veran, Bk_func

def ba_plan_btn_note_webbl(t_resnr:int, t_resline:int):

    prepare_cache ([Bk_veran, Bk_func])

    t_veran_nr = 0
    avail_mainres = False
    resv_datum = None
    bk_veran = bk_func = None

    mainres = None

    Mainres = create_buffer("Mainres",Bk_veran)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_veran_nr, avail_mainres, resv_datum, bk_veran, bk_func
        nonlocal t_resnr, t_resline
        nonlocal mainres


        nonlocal mainres

        return {"t_veran_nr": t_veran_nr, "avail_mainres": avail_mainres, "resv_datum": resv_datum}


    mainres = get_cache (Bk_veran, {"veran_nr": [(eq, t_resnr)]})

    if mainres:
        avail_mainres = True
        t_veran_nr = mainres.veran_nr

    bk_func = get_cache (Bk_func, {"veran_nr": [(eq, t_resnr)],"veran_seite": [(eq, t_resline)]})

    if bk_func:
        resv_datum = bk_func.datum

    return generate_output()