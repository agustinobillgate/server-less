from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Ratecode, Guest_pr, Guest, Prtable, Bediener, Res_history

def ratecode_adm_delete_prcode_1bl(icase:int, pvilanguage:int, prcode:str, user_init:str):
    msg_str = ""
    error_flag = False
    lvcarea:str = "ratecode_admin"
    queasy = ratecode = guest_pr = guest = prtable = bediener = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, lvcarea, queasy, ratecode, guest_pr, guest, prtable, bediener, res_history


        return {"msg_str": msg_str, "error_flag": error_flag}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (func.lower(Queasy.char1) == (prcode).lower())).first()

    if icase == 1:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower())).first()

        if ratecode:
            msg_str = translateExtended ("Contract Rates exists, deleting not possible", lvcarea, "")
            error_flag = True

            return generate_output()
        msg_str = "&Q" + translateExtended ("Do you really want to REMOVE the Rate Code", lvcarea, "") + chr(10) + to_string(prcode) + " - " + queasy.char2 + " ?"

        return generate_output()

    elif icase == 2:

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.code == queasy.char1)).first()

        if guest_pr:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == guest_pr.gastnr)).first()

            if guest and guest.karteityp == 9:

                guest = db_session.query(Guest).first()
                db_session.delete(guest)
            db_session.delete(guest_pr)

        if queasy.char1 != "":

            for prtable in db_session.query(Prtable).filter(
                    (Prtable.prcode == queasy.char1)).all():
                db_session.delete(prtable)


        queasy = db_session.query(Queasy).first()
        db_session.delete(queasy)

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Delete RateCode, Code: " + prcode


            res_history.action = "RateCode"

            res_history = db_session.query(Res_history).first()


    return generate_output()