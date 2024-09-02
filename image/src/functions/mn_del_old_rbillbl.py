from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Counters, Queasy, H_bill, H_bill_line

def mn_del_old_rbillbl():
    i = 0
    ci_date:date = None
    htparam = counters = queasy = h_bill = h_bill_line = None

    bbuff = lbuff = None

    Bbuff = H_bill
    Lbuff = H_bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, counters, queasy, h_bill, h_bill_line
        nonlocal bbuff, lbuff


        nonlocal bbuff, lbuff
        return {"i": i}

    def del_old_rbill():

        nonlocal i, ci_date, htparam, counters, queasy, h_bill, h_bill_line
        nonlocal bbuff, lbuff


        nonlocal bbuff, lbuff

        anz:int = 0
        Bbuff = H_bill
        Lbuff = H_bill_line

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 164)).first()
        anz = htparam.finteger

        if anz == 0:
            anz = 7

        h_bill_line = db_session.query(H_bill_line).filter(
                    (H_bill_line.bill_datum < (ci_date - anz))).first()
        while None != h_bill_line:

            lbuff = db_session.query(Lbuff).filter(
                            (Lbuff._recid == h_bill_line._recid)).first()
            db_session.delete(lbuff)

            i = i + 1


            h_bill_line = db_session.query(H_bill_line).filter(
                        (H_bill_line.bill_datum < (ci_date - anz))).first()
        i = 0

        h_bill = db_session.query(H_bill).filter(
                    (H_bill.flag == 1) &  (H_bill.departement >= 1)).first()
        while None != h_bill:

            h_bill_line = db_session.query(H_bill_line).filter(
                        (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement)).first()

            if not h_bill_line:

                bbuff = db_session.query(Bbuff).filter(
                            (Bbuff._recid == h_bill._recid)).first()
                db_session.delete(bbuff)

                i = i + 1

            h_bill = db_session.query(H_bill).filter(
                        (H_bill.flag == 1) &  (H_bill.departement >= 1)).first()

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 4)).all():
            db_session.delete(queasy)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    del_old_rbill()

    counters = db_session.query(Counters).filter(
            (Counters.counter_no == 121)).first()

    if counters:
        counters.counter = 0


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 191)).first()

    if queasy:
        queasy.number1 = 0
        queasy.number2 = 0


    return generate_output()