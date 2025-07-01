#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Ratecode, Guest_pr, Guest, Prtable, Bediener, Res_history

def ratecode_adm_delete_prcode_1bl(icase:int, pvilanguage:int, prcode:string, user_init:string):

    prepare_cache ([Bediener, Res_history])

    msg_str = ""
    error_flag = False
    lvcarea:string = "ratecode-admin"
    queasy = ratecode = guest_pr = guest = prtable = bediener = res_history = None

    bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, lvcarea, queasy, ratecode, guest_pr, guest, prtable, bediener, res_history
        nonlocal icase, pvilanguage, prcode, user_init
        nonlocal bqueasy


        nonlocal bqueasy

        return {"msg_str": msg_str, "error_flag": error_flag}


    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, prcode)]})

    if icase == 1:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)]})

        if ratecode:
            msg_str = translateExtended ("Contract Rates exists, deleting not possible", lvcarea, "")
            error_flag = True

            return generate_output()
        msg_str = "&Q" + translateExtended ("Do you really want to REMOVE the Rate Code", lvcarea, "") + chr_unicode(10) + to_string(prcode) + " - " + queasy.char2 + " ?"

        return generate_output()

    elif icase == 2:

        guest_pr = get_cache (Guest_pr, {"code": [(eq, queasy.char1)]})

        if guest_pr:

            guest = get_cache (Guest, {"gastnr": [(eq, guest_pr.gastnr)]})

            if guest and guest.karteityp == 9:
                pass
                db_session.delete(guest)
            db_session.delete(guest_pr)

        if queasy.char1 != "":

            for prtable in db_session.query(Prtable).filter(
                     (Prtable.prcode == queasy.char1)).order_by(Prtable._recid).all():
                db_session.delete(prtable)


        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy.key == 289) & (Bqueasy.char1 == queasy.char1)).first()

        if bqueasy:
            pass
            db_session.delete(bqueasy)
        pass
        db_session.delete(queasy)

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Delete RateCode, Code: " + prcode


            res_history.action = "RateCode"
            pass
            pass

    return generate_output()