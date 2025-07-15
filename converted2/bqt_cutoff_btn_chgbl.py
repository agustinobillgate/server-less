#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran, Bk_reser

def bqt_cutoff_btn_chgbl(o_resnr:int, o_reslinnr:int, o_resstatus:int):

    prepare_cache ([Bk_veran, Bk_reser])

    recid_bk_reser = 0
    msg_it = False
    bk_veran = bk_reser = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal recid_bk_reser, msg_it, bk_veran, bk_reser
        nonlocal o_resnr, o_reslinnr, o_resstatus

        return {"recid_bk_reser": recid_bk_reser, "msg_it": msg_it}


    if o_resstatus == 1:

        bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, o_resnr)]})

        if (bk_veran.deposit_payment[0] + bk_veran.deposit_payment[1] + bk_veran.deposit_payment[2] + bk_veran.deposit_payment[3] + bk_veran.deposit_payment[4] + bk_veran.deposit_payment[5] + bk_veran.deposit_payment[6] + bk_veran.deposit_payment[7] + bk_veran.deposit_payment[8]) != 0:

            bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"veran_resnr": [(ne, o_reslinnr)],"resstatus": [(eq, 1)]})

            if not bk_reser:
                msg_it = True

    if msg_it:

        return generate_output()

    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, o_resnr)],"veran_seite": [(eq, o_reslinnr)]})

    if bk_reser:
        recid_bk_reser = bk_reser._recid

    return generate_output()