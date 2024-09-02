from functions.additional_functions import *
import decimal
from functions.ba_cancreslinebl import ba_cancreslinebl
from models import Bk_veran, Bk_reser, Guest, Bk_raum, B_storno

def rsv_cancel_listbl(bqt_resnr:int, bqt_reslinnr:int, user_init:str):
    msg_str = ""
    cancel_str:str = ""
    bk_veran = bk_reser = guest = bk_raum = b_storno = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, cancel_str, bk_veran, bk_reser, guest, bk_raum, b_storno


        return {"msg_str": msg_str}


    bk_veran = db_session.query(Bk_veran).filter(
            (Bk_veran.veran_nr == bqt_resnr)).first()

    if (bk_veran.deposit_payment[0] + bk_veran.deposit_payment[1] + bk_veran.deposit_payment[2] + bk_veran.deposit_payment[3] + bk_veran.deposit_payment[4] + bk_veran.deposit_payment[5] + bk_veran.deposit_payment[6] + bk_veran.deposit_payment[7] + bk_veran.deposit_payment[8]) > 0:

        bk_reser = db_session.query(Bk_reser).filter(
                (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.veran_resnr != bqt_reslinnr) &  (Bk_reser.resstatus == 1)).first()

        if not bk_reser:
            msg_str = "Deposit exists, cancel reservation not possible."

            return generate_output()

    if bk_veran.rechnr > 0:

        bk_reser = db_session.query(Bk_reser).filter(
                (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.veran_resnr != bqt_reslinnr) &  (Bk_reser.resstatus == 1)).first()

        if not bk_reser:
            msg_str = "Bill exists, cancel reservation not possible."

            return generate_output()

    bk_reser = db_session.query(Bk_reser).filter(
            (Bk_reser.veran_nr == bqt_resnr) &  (Bk_reser.veran_seite == bqt_reslinnr)).first()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == bk_veran.gastnr)).first()

    bk_raum = db_session.query(Bk_raum).filter(
            (Bk_raum.raum == bk_reser.raum)).first()

    b_storno = db_session.query(B_storno).filter(
            (B_storno.bankettnr == bk_reser.veran_nr) &  (B_storno.breslinnr == bk_reser.veran_resnr)).first()

    if not b_storno:
        b_storno = B_storno()
    db_session.add(b_storno)

    b_storno.bankettnr = bk_reser.veran_nr
    b_storno.breslinnr = bk_reser.veran_resnr
    b_storno.gastnr = bk_veran.gastnr
    b_storno.betrieb_gast = bk_veran.gastnrver
    b_storno.datum = bk_reser.datum
    b_storno.grund[17] = cancel_str + " D*" +\
            to_string(get_current_date(), "99/99/99") + " " + to_string(get_current_time_in_seconds(), "hh:mm:ss") +\
            " " + bk_reser.raum


    b_storno.usercode = user_init
    get_output(ba_cancreslinebl(bk_reser.veran_nr, bk_reser.veran_resnr))

    return generate_output()