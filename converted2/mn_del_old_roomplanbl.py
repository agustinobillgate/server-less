#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Resplan, Zimplan

def mn_del_old_roomplanbl():

    prepare_cache ([Htparam])

    i = 0
    ci_date:date = None
    htparam = resplan = zimplan = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, resplan, zimplan

        return {"i": i}

    def del_old_roomplan():

        nonlocal i, ci_date, htparam, resplan, zimplan

        anz:int = 0

        resplan = get_cache (Resplan, {"datum": [(lt, ci_date)]})
        while None != resplan:
            i = i + 1
            pass
            db_session.delete(resplan)
            pass

            curr_recid = resplan._recid
            resplan = db_session.query(Resplan).filter(
                     (Resplan.datum < ci_date) & (Resplan._recid > curr_recid)).first()

        zimplan = get_cache (Zimplan, {"datum": [(lt, ci_date)]})
        while None != zimplan:
            i = i + 1
            pass
            db_session.delete(zimplan)
            pass

            curr_recid = zimplan._recid
            zimplan = db_session.query(Zimplan).filter(
                     (Zimplan.datum < ci_date) & (Zimplan._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    del_old_roomplan()

    return generate_output()