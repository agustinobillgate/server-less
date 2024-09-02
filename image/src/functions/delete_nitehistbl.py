from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Nitehist, Nitestor

def delete_nitehistbl(case_type:int, datum1:date, int1:int):
    success_flag = False
    billdate:date = None
    htparam = nitehist = nitestor = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, billdate, htparam, nitehist, nitestor


        return {"success_flag": success_flag}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    if case_type == 1:

        for nitehist in db_session.query(Nitehist).filter(
                (Nitehist.datum == datum1) &  (Nitehist.reihenfolge == int1)).all():
            db_session.delete(nitehist)

            success_flag = True

        for nitestor in db_session.query(Nitestor).filter(
                (Nitestor.reihenfolge == int1)).all():
            nitehist = Nitehist()
            db_session.add(nitehist)

            nitehist.datum = billdate
            nitehist.reihenfolge = nitestor.reihenfolge
            nitehist.line = nitestor.line
            nitehist.line_nr = nitestor.line_nr

    return generate_output()