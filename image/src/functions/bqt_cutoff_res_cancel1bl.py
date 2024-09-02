from functions.additional_functions import *
import decimal
from models import Bk_veran, Bk_reser, Guest, Bk_raum

def bqt_cutoff_res_cancel1bl(pvilanguage:int, o_resnr:int, o_reslinnr:int):
    msg_str = ""
    msg_strq = ""
    recid_bk_reser = 0
    lvcarea:str = "bqt_cutoff"
    bk_veran = bk_reser = guest = bk_raum = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_strq, recid_bk_reser, lvcarea, bk_veran, bk_reser, guest, bk_raum


        return {"msg_str": msg_str, "msg_strq": msg_strq, "recid_bk_reser": recid_bk_reser}


    bk_veran = db_session.query(Bk_veran).filter(
            (Bk_veran.veran_nr == o_resnr)).first()

    if (bk_veran.deposit_payment[0] + bk_veran.deposit_payment[1] + bk_veran.deposit_payment[2] + bk_veran.deposit_payment[3] + bk_veran.deposit_payment[4] + bk_veran.deposit_payment[5] + bk_veran.deposit_payment[6] + bk_veran.deposit_payment[7] + bk_veran.deposit_payment[8]) > 0:

        bk_reser = db_session.query(Bk_reser).filter(
                (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.veran_resnr != o_reslinnr) &  (Bk_reser.resstatus == 1)).first()

        if not bk_reser:
            msg_str = translateExtended ("Deposit exists, cancel reservation not possible.", lvcarea, "")

            return generate_output()

    if bk_veran.rechnr > 0:

        bk_reser = db_session.query(Bk_reser).filter(
                (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.veran_resnr != o_reslinnr) &  (Bk_reser.resstatus == 1)).first()

        if not bk_reser:
            msg_str = translateExtended ("Bill exists, cancel reservation not possible.", lvcarea, "")

            return generate_output()

    bk_reser = db_session.query(Bk_reser).filter(
            (Bk_reser.veran_nr == o_resnr) &  (Bk_reser.veran_seite == o_reslinnr)).first()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == bk_veran.gastnr)).first()

    bk_raum = db_session.query(Bk_raum).filter(
            (Bk_raum.raum == bk_reser.raum)).first()
    msg_strq = "&Q" + translateExtended ("Do you really want to delete reservation of", lvcarea, "") + chr(10) + guest.name + " - " + translateExtended ("Room:", lvcarea, "") + " " + bk_raum.bezeich + chr(10) + translateExtended ("Date:", lvcarea, "") + " " + to_string(bk_reser.datum) + " - " + to_string(bk_reser.bis_datum) + "  " + translateExtended ("Time:", lvcarea, "") + " " + to_string(bk_reser.von_zeit, "99:99") + " - " + to_string(bk_reser.bis_zeit, "99:99") + "?"
    recid_bk_reser = bk_reser._recid

    return generate_output()