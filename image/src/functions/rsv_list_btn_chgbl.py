from functions.additional_functions import *
import decimal
from models import Bk_veran, Bk_reser

def rsv_list_btn_chgbl(output_list_resstatus:int, output_list_resnr:int, output_list_reslinnr:int):
    recid_bk_reser = 0
    avail_bk_reser = False
    bk_veran = bk_reser = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal recid_bk_reser, avail_bk_reser, bk_veran, bk_reser


        return {"recid_bk_reser": recid_bk_reser, "avail_bk_reser": avail_bk_reser}


    if output_list_resstatus == 1:

        bk_veran = db_session.query(Bk_veran).filter(
                (Bk_veran.veran_nr == output_list_resnr)).first()

        if (bk_veran.deposit_payment[0] + bk_veran.deposit_payment[1] + bk_veran.deposit_payment[2] + bk_veran.deposit_payment[3] + bk_veran.deposit_payment[4] + bk_veran.deposit_payment[5] + bk_veran.deposit_payment[6] + bk_veran.deposit_payment[7] + bk_veran.deposit_payment[8]) != 0:

            bk_reser = db_session.query(Bk_reser).filter(
                    (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.veran_resnr != output_list_reslinnr) &  (Bk_reser.resstatus == 1)).first()

            if not bk_reser:
                avail_bk_reser = False

                return generate_output()
            avail_bk_reser = True
            recid_bk_reser = bk_reser._recid
        else:

            bk_reser = db_session.query(Bk_reser).filter(
                    (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.veran_resnr == output_list_reslinnr) &  (Bk_reser.resstatus == 1)).first()

            if bk_reser:
                avail_bk_reser = True
                recid_bk_reser = bk_reser._recid
    else:

        bk_veran = db_session.query(Bk_veran).filter(
                (Bk_veran.veran_nr == output_list_resnr)).first()

        if (bk_veran.deposit_payment[0] + bk_veran.deposit_payment[1] + bk_veran.deposit_payment[2] + bk_veran.deposit_payment[3] + bk_veran.deposit_payment[4] + bk_veran.deposit_payment[5] + bk_veran.deposit_payment[6] + bk_veran.deposit_payment[7] + bk_veran.deposit_payment[8]) != 0:

            bk_reser = db_session.query(Bk_reser).filter(
                    (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.veran_resnr == output_list_reslinnr) &  (Bk_reser.resstatus == output_list_resstatus)).first()

            if bk_reser:
                avail_bk_reser = True
                recid_bk_reser = bk_reser._recid
            else:
                avail_bk_reser = False

                return generate_output()
        else:

            bk_reser = db_session.query(Bk_reser).filter(
                    (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.veran_resnr == output_list_reslinnr) &  (Bk_reser.resstatus == output_list_resstatus)).first()

            if bk_reser:
                avail_bk_reser = True
                recid_bk_reser = bk_reser._recid

    return generate_output()