from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Reslin_queasy, Res_line, Prtable

def argt_admincheck_delbl(pvilanguage:int, argtnr:int, arrangement:str):
    msg_str = ""
    lvcarea:str = "argt-admin-check-del"
    found:bool = False
    i:int = 0
    reslin_queasy = res_line = prtable = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, found, i, reslin_queasy, res_line, prtable
        nonlocal pvilanguage, argtnr, arrangement


        return {"msg_str": msg_str}


    reslin_queasy = db_session.query(Reslin_queasy).filter(
             (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (Reslin_queasy.number2 == argtnr)).first()

    if reslin_queasy:
        msg_str = msg_str + chr(2) + translateExtended ("Deleting no possible, arrangement defined in price code : ", lvcarea, "") + reslin_queasy.char1

        return generate_output()

    res_line = db_session.query(Res_line).filter(
             (func.lower(Res_line.arrangement) == (arrangement).lower())).first()

    if res_line:
        msg_str = msg_str + chr(2) + translateExtended ("Reservation exists, deleting not possible.", lvcarea, "")

        return generate_output()

    prtable = db_session.query(Prtable).first()
    while None != prtable and not found:
        for i in range(1,99 + 1) :

            if prtable.argtnr[i - 1] == argtnr:
                found = True

        curr_recid = prtable._recid
        prtable = db_session.query(Prtable).filter(Prtable._recid > curr_recid).first()

    if found:
        msg_str = msg_str + chr(2) + translateExtended ("Price Market Table exists, deleting not possible.", lvcarea, "")

        return generate_output()