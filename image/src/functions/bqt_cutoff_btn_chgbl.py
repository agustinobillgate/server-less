from functions.additional_functions import *
import decimal
from models import Bk_veran, Bk_reser

def bqt_cutoff_btn_chgbl(o_resnr:int, o_reslinnr:int, o_resstatus:int):
    recid_bk_reser = 0
    msg_it = False
    bk_veran = bk_reser = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal recid_bk_reser, msg_it, bk_veran, bk_reser


        return {"recid_bk_reser": recid_bk_reser, "msg_it": msg_it}


    if o_resstatus == 1:

        bk_veran = db_session.query(Bk_veran).filter(
                (Bk_veran.veran_nr == o_resnr)).first()

        if (bk_veran.deposit_payment[0] + bk_veran.deposit_payment[1] + bk_veran.deposit_payment[2] + bk_veran.deposit_payment[3] + bk_veran.deposit_payment[4] + bk_veran.deposit_payment[5] + bk_veran.deposit_payment[6] + bk_veran.deposit_payment[7] + bk_veran.deposit_payment[8]) != 0:

            bk_reser = db_session.query(Bk_reser).filter(
                    (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.veran_resnr != o_reslinnr) &  (Bk_reser.resstatus == 1)).first()

            if not bk_reser:
                msg_it = True

    if msg_it:

        return generate_output()

    bk_reser = db_session.query(Bk_reser).filter(
            (Bk_reser.veran_nr == o_resnr) &  (Bk_reser.veran_seite == o_reslinnr)).first()
    recid_bk_reser = bk_reser._recid

    return generate_output()