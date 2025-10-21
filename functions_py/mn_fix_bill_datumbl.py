#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/10/2025
# time delta
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timedelta
from models import Htparam, Bill, Bill_line

def mn_fix_bill_datumbl():

    prepare_cache ([Htparam, Bill_line])

    htparam = bill = bill_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam, bill, bill_line

        return {}

    def fix_bill_datum():

        nonlocal htparam, bill, bill_line

        bill_date:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        # bill = get_cache (Bill, {"rechnr": [(gt, 0)],"datum": [(ge, (bill_date - timedelta(days=400)))]}, order_by="datum,_recid")
        bill = db_session.query(Bill).filter(
                 (Bill.rechnr > 0) & (Bill.datum >= (bill_date - timedelta(days=400)))).order_by(Bill.datum,Bill._recid).first()
        while None != bill:

            bill_line = db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid.desc()).first()

            if bill_line:

                if bill.datum == None or bill_line.bill_datum > bill.datum:
                    pass
                    bill.datum = bill_line.bill_datum


                    pass

            curr_recid = bill._recid
            bill = db_session.query(Bill).filter(
                     (Bill.rechnr > 0) & (Bill.datum >= (bill_date - timedelta(days=400))) & (Bill._recid > curr_recid)).first()


    fix_bill_datum()

    return generate_output()