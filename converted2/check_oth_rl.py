from functions.additional_functions import *
import decimal
from models import Bk_veran, Bk_reser, Bk_func

def check_oth_rl(resnr:int, resline:int):
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


    fsl = db_session.query(Fsl).filter(
             (Fsl.veran_nr == resnr) & (Fsl.veran_seite == resline)).first()

    if fsl:
        fsl.resstatus = 5
        fsl.c_resstatus[0] = "I"
        fsl.r_resstatus[0] = 5

    rline = db_session.query(Rline).filter(
             (Rline.veran_nr == resnr) & (Rline.veran_resnr == resline)).first()

    if rline:
        rline.resstatus = 5
    FIND rline WHERE rline.veran_nr = resnr and rline.resstatus != 5

    if not rline:

        mres = db_session.query(Mres).filter(
                 (Mres.veran_nr == resnr)).first()

        if mres:
            mres.activeflag = 1

    return generate_output()