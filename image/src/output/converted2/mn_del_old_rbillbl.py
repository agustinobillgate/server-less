#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Counters, Queasy, H_bill, H_bill_line

def mn_del_old_rbillbl():

    prepare_cache ([Htparam, Counters])

    i = 0
    ci_date:date = None
    htparam = counters = queasy = h_bill = h_bill_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, counters, queasy, h_bill, h_bill_line

        return {"i": i}

    def del_old_rbill():

        nonlocal i, ci_date, htparam, counters, queasy, h_bill, h_bill_line

        anz:int = 0
        bbuff = None
        lbuff = None
        Bbuff =  create_buffer("Bbuff",H_bill)
        Lbuff =  create_buffer("Lbuff",H_bill_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 164)]})
        anz = htparam.finteger

        if anz == 0:
            anz = 7

        h_bill_line = get_cache (H_bill_line, {"bill_datum": [(lt, (ci_date - anz))]})
        while None != h_bill_line:

            lbuff = db_session.query(Lbuff).filter(
                             (Lbuff._recid == h_bill_line._recid)).first()
            db_session.delete(lbuff)
            pass
            i = i + 1

            curr_recid = h_bill_line._recid
            h_bill_line = db_session.query(H_bill_line).filter(
                         (H_bill_line.bill_datum < (ci_date - timedelta(days=anz))) & (H_bill_line._recid > curr_recid)).first()
        i = 0

        h_bill = get_cache (H_bill, {"flag": [(eq, 1)],"departement": [(ge, 1)]})
        while None != h_bill:

            h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, h_bill.departement)]})

            if not h_bill_line:

                bbuff = db_session.query(Bbuff).filter(
                             (Bbuff._recid == h_bill._recid)).first()
                db_session.delete(bbuff)
                pass
                i = i + 1

            curr_recid = h_bill._recid
            h_bill = db_session.query(H_bill).filter(
                         (H_bill.flag == 1) & (H_bill.departement >= 1) & (H_bill._recid > curr_recid)).first()

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 4)).order_by(Queasy._recid).all():
            db_session.delete(queasy)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    del_old_rbill()

    counters = get_cache (Counters, {"counter_no": [(eq, 121)]})

    if counters:
        counters.counter = 0


        pass

    queasy = get_cache (Queasy, {"key": [(eq, 191)]})

    if queasy:
        queasy.number1 = 0
        queasy.number2 = 0


        pass

    return generate_output()