from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Calls

def mn_del_old_callsbl():
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

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 302)).first()
        anz1 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 265)).first()
        anz2 = htparam.finteger

        if anz1 > anz2:
            anz = anz1
        else:
            anz = anz2

        calls = db_session.query(Calls).filter(
                ((Calls.datum + anz) < ci_date) &  (Calls.buchflag == 0) &  (Calls.zeit >= 0) &  (Calls.key <= 1)).first()
        while None != calls:

            if (substring(calls.rufnummer, 0, 1) != "0" and (calls.datum + anz2) < ci_date) or (calls.datum + anz1) < ci_date:
                i = i + 1

                calls = db_session.query(Calls).first()
                db_session.delete(calls)

            calls = db_session.query(Calls).filter(
                    ((Calls.datum + anz) < ci_date) &  (Calls.buchflag == 0) &  (Calls.zeit >= 0) &  (Calls.key <= 1)).first()

        calls = db_session.query(Calls).filter(
                ((Calls.datum + anz) < ci_date) &  (Calls.buchflag == 1) &  (Calls.zeit >= 0) &  (Calls.key <= 1)).first()
        while None != calls:

            if (substring(calls.rufnummer, 0, 1) != "0" and (calls.datum + anz2) < ci_date) or (calls.datum + anz1) < ci_date:
                i = i + 1

                calls = db_session.query(Calls).first()
                db_session.delete(calls)

            calls = db_session.query(Calls).filter(
                    ((Calls.datum + anz) < ci_date) &  (Calls.buchflag == 1) &  (Calls.zeit >= 0) &  (Calls.key <= 1)).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    del_old_calls()

    return generate_output()