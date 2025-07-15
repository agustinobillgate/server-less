#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran, Bk_reser, Bk_func

def check_oth_rl_sts(resnr:int, resline:int, r_status:int):

    prepare_cache ([Bk_veran, Bk_reser, Bk_func])

    bk_veran = bk_reser = bk_func = None

    mres = rline = fsl = None

    Mres = create_buffer("Mres",Bk_veran)
    Rline = create_buffer("Rline",Bk_reser)
    Fsl = create_buffer("Fsl",Bk_func)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_veran, bk_reser, bk_func
        nonlocal resnr, resline, r_status
        nonlocal mres, rline, fsl


        nonlocal mres, rline, fsl

        return {}


    fsl = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, resline)]})

    if fsl:

        if fsl.resstatus != r_status:

            if r_status == 1:
                pass
                fsl.resstatus = 1
                fsl.c_resstatus[0] = "F"
                fsl.r_resstatus[0] = 1
                pass

            elif r_status == 2:
                pass
                fsl.resstatus = 2
                fsl.c_resstatus[0] = "T"
                fsl.r_resstatus[0] = 2
                pass

    rline = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, resline)]})

    if rline:

        if rline.resstatus != r_status:
            pass
            rline.resstatus = r_status
            pass

    rline = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)],"resstatus": [(ne, r_status)]})

    if not rline:

        mres = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})

        if mres:
            pass
            mres.resstatus = r_status
            pass

    return generate_output()