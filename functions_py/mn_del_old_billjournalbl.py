#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/10/2025
# time delta
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timedelta
from models import Htparam, Hoteldpt, Billjournal

def mn_del_old_billjournalbl():

    prepare_cache ([Htparam, Hoteldpt])

    i = 0
    ci_date:date = None
    htparam = hoteldpt = billjournal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, hoteldpt, billjournal

        return {"i": i}

    def del_old_billjournal():

        nonlocal ci_date, htparam, hoteldpt, billjournal

        i:int = 0
        anz:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 161)]})
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():

            # billjournal = get_cache (Billjournal, {"bill_datum": [(lt, (ci_date - anz))],"departement": [(eq, hoteldpt.num)],"zeit": [(ge, 0)],"subtime": [(ge, 0)]})
            billjournal = db_session.query(Billjournal).filter(
                     (Billjournal.bill_datum < (ci_date - timedelta(days=anz))) & (Billjournal.departement == hoteldpt.num) & (Billjournal.zeit >= 0) & (Billjournal.subtime >= 0)).first()
            
            while None != billjournal:
                i = i + 1
                pass
                db_session.delete(billjournal)

                curr_recid = billjournal._recid
                billjournal = db_session.query(Billjournal).filter(
                         (Billjournal.bill_datum < (ci_date - timedelta(days=anz))) & (Billjournal.departement == hoteldpt.num) & (Billjournal.zeit >= 0) & (Billjournal.subtime >= 0) & (Billjournal._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    del_old_billjournal()

    return generate_output()