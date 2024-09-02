from functions.additional_functions import *
import decimal
from functions.bookcall2bl import bookcall2bl
from functions.bookcall3bl import bookcall3bl
from models import Calls

def calls_list_bookcallbl(pvilanguage:int, s_recid:int, bill_recid:int, room_no:str, user_init:str):
    success = False
    rechnr = 0
    calls = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success, rechnr, calls


        return {"success": success, "rechnr": rechnr}


    calls = db_session.query(Calls).filter(
            (Calls._recid == s_recid)).first()

    if room_no != "":
        success, rechnr = get_output(bookcall2bl(pvilanguage, room_no, calls.datum, calls.zeit, calls.satz_id, calls.dauer, calls.rufnummer, calls.gastbetrag, user_init))
    else:
        success, rechnr = get_output(bookcall3bl(pvilanguage, bill_recid, calls.datum, calls.zeit, calls.satz_id, calls.dauer, calls.rufnummer, calls.gastbetrag, user_init))

    if success:

        calls = db_session.query(Calls).filter(
                (Calls._recid == s_recid)).first()
        calls.buchflag = 1
        calls.rechnr = rechnr
        calls.zinr = room_no

        calls = db_session.query(Calls).first()

    return generate_output()