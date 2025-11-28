#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from functions.bookcall2bl import bookcall2bl
from functions.bookcall3bl import bookcall3bl
from models import Calls

def calls_list_bookcallbl(pvilanguage:int, s_recid:int, bill_recid:int, room_no:string, user_init:string):

    prepare_cache ([Calls])

    success = False
    rechnr = 0
    calls = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success, rechnr, calls
        nonlocal pvilanguage, s_recid, bill_recid, room_no, user_init

        return {"success": success, "rechnr": rechnr}


    # calls = get_cache (Calls, {"_recid": [(eq, s_recid)]})
    calls = db_session.query(Calls).filter(Calls._recid == s_recid).with_for_update().first()

    if not calls:

        return generate_output()

    if room_no != "":
        success, rechnr = get_output(bookcall2bl(pvilanguage, room_no, calls.datum, calls.zeit, calls.satz_id, calls.dauer, calls.rufnummer, calls.gastbetrag, user_init))
    else:
        success, rechnr = get_output(bookcall3bl(pvilanguage, bill_recid, calls.datum, calls.zeit, calls.satz_id, calls.dauer, calls.rufnummer, calls.gastbetrag, user_init))

    if success:

        calls = get_cache (Calls, {"_recid": [(eq, s_recid)]})
        calls.buchflag = 1
        calls.rechnr = rechnr
        calls.zinr = room_no


        pass

    return generate_output()