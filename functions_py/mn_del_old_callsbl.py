#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Calls

def mn_del_old_callsbl():

    prepare_cache ([Htparam])

    i = 0
    ci_date:date = None
    htparam = calls = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, calls

        return {"i": i}

    def del_old_calls():

        nonlocal i, ci_date, htparam, calls

        anz:int = 0
        anz1:int = 0
        anz2:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 302)]})
        anz1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 265)]})
        anz2 = htparam.finteger

        if anz1 > anz2:
            anz = anz1
        else:
            anz = anz2

        calls = db_session.query(Calls).filter(
                 ((Calls.datum + timedelta(days=anz)) < ci_date) & (Calls.buchflag == 0) & (Calls.zeit >= 0) & (Calls.key <= 1)).first()
        while None != calls:

            if (substring(calls.rufnummer, 0, 1) != ("0")  and (calls.datum + timedelta(days=anz2)) < ci_date) or (calls.datum + timedelta(days=anz1)) < ci_date:
                i = i + 1
                pass
                db_session.delete(calls)

            curr_recid = calls._recid
            calls = db_session.query(Calls).filter(
                     ((Calls.datum + timedelta(days=anz)) < ci_date) & (Calls.buchflag == 0) & (Calls.zeit >= 0) & (Calls.key <= 1) & (Calls._recid > curr_recid)).first()

        calls = db_session.query(Calls).filter(
                 ((Calls.datum + timedelta(days=anz)) < ci_date) & (Calls.buchflag == 1) & (Calls.zeit >= 0) & (Calls.key <= 1)).first()
        while None != calls:

            if (substring(calls.rufnummer, 0, 1) != ("0")  and (calls.datum + timedelta(days=anz2)) < ci_date) or (calls.datum + timedelta(days=anz1)) < ci_date:
                i = i + 1
                pass
                db_session.delete(calls)

            curr_recid = calls._recid
            calls = db_session.query(Calls).filter(
                     ((Calls.datum + timedelta(days=anz)) < ci_date) & (Calls.buchflag == 1) & (Calls.zeit >= 0) & (Calls.key <= 1) & (Calls._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    del_old_calls()

    return generate_output()