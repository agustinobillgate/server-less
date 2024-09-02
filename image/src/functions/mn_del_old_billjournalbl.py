from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Hoteldpt, Billjournal

def mn_del_old_billjournalbl():
    i = 0
    ci_date:date = None
    htparam = hoteldpt = billjournal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, hoteldpt, billjournal


        return {"i": i}

    def del_old_billjournal():

        nonlocal i, ci_date, htparam, hoteldpt, billjournal

        i:int = 0
        anz:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 161)).first()
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        for hoteldpt in db_session.query(Hoteldpt).all():

            billjournal = db_session.query(Billjournal).filter(
                    (Billjournal.bill_datum < (ci_date - anz)) &  (Billjournal.departement == hoteldpt.num) &  (Billjournal.zeit >= 0) &  (Billjournal.subtime >= 0)).first()
            while None != billjournal:
                i = i + 1

                billjournal = db_session.query(Billjournal).first()
                db_session.delete(billjournal)


                billjournal = db_session.query(Billjournal).filter(
                        (Billjournal.bill_datum < (ci_date - anz)) &  (Billjournal.departement == hoteldpt.num) &  (Billjournal.zeit >= 0) &  (Billjournal.subtime >= 0)).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    del_old_billjournal()

    return generate_output()