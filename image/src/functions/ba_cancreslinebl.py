from functions.additional_functions import *
import decimal
from models import Bk_veran, Bk_reser, Bk_func

def ba_cancreslinebl(resnr:int, resline:int):
    bk_veran = bk_reser = bk_func = None

    mres = rline = fsl = None

    Mres = Bk_veran
    Rline = Bk_reser
    Fsl = Bk_func

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_veran, bk_reser, bk_func
        nonlocal mres, rline, fsl


        nonlocal mres, rline, fsl
        return {}


    rline = db_session.query(Rline).filter(
            (Rline.veran_nr == resnr) &  (Rline.veran_resnr == resline)).first()

    if rline:

        rline = db_session.query(Rline).first()
        rline.resstatus = 9

        rline = db_session.query(Rline).first()

    bk_func = db_session.query(Bk_func).filter(
            (Bk_func.veran_nr == resnr) &  (Bk_func.veran_seite == resline)).first()

    if bk_func:
        bk_func.resstatus = 9
        bk_func.r_resstatus[0] = 9
        bk_func.c_resstatus[0] = "C"

        bk_func = db_session.query(Bk_func).first()

    rline = db_session.query(Rline).filter(
            (Rline.veran_nr == resnr) &  (Rline.resstatus <= 2)).first()

    if not rline:

        mres = db_session.query(Mres).filter(
                (Mres.veran_nr == resnr)).first()

        if mres:

            mres = db_session.query(Mres).first()
            mres.activeflag = 1

            mres = db_session.query(Mres).first()

    return generate_output()