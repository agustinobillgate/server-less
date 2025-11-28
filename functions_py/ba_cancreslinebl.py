#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran, Bk_reser, Bk_func
from sqlalchemy.orm import flag_modified

def ba_cancreslinebl(resnr:int, resline:int):

    prepare_cache ([Bk_veran, Bk_reser, Bk_func])

    bk_veran = bk_reser = bk_func = None

    mres = rline = fsl = None

    Mres = create_buffer("Mres",Bk_veran)
    Rline = create_buffer("Rline",Bk_reser)
    Fsl = create_buffer("Fsl",Bk_func)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_veran, bk_reser, bk_func
        nonlocal resnr, resline
        nonlocal mres, rline, fsl


        nonlocal mres, rline, fsl

        return {}


    # rline = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)],"veran_resnr": [(eq, resline)]})
    rline = db_session.query(Rline).filter(
             (Rline.veran_nr == resnr) &
             (Rline.veran_seite == resline)).with_for_update().first()

    if rline:
        pass
        rline.resstatus = 9
        pass

    # bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, resline)]})
    bk_func = db_session.query(Fsl).filter(
             (Fsl.veran_nr == resnr) &
             (Fsl.veran_seite == resline)).with_for_update().first()

    if bk_func:
        bk_func.resstatus = 9
        bk_func.r_resstatus[0] = 9
        bk_func.c_resstatus[0] = "C"
        pass
    flag_modified(bk_func, "r_resstatus")
    flag_modified(bk_func, "c_resstatus")
    rline = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)],"resstatus": [(le, 2)]})

    if not rline:

        # mres = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})
        mres = db_session.query(Mres).filter(
                 (Mres.veran_nr == resnr)).with_for_update().first()

        if mres:
            pass
            mres.activeflag = 1
            pass

    return generate_output()