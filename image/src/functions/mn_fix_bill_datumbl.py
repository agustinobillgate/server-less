from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Bill, Bill_line

def mn_fix_bill_datumbl():
    htparam = bill = bill_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam, bill, bill_line


        return {}

    def fix_bill_datum():

        nonlocal htparam, bill, bill_line

        bill_date:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        bill = db_session.query(Bill).filter(
                (Bill.rechnr > 0) &  (Bill.datum >= (bill_date - 400))).first()
        while None != bill:

            bill_line = db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill.rechnr)).first()

            if bill_line:

                if bill.datum == None or bill_line.bill_datum > bill.datum:

                    bill = db_session.query(Bill).first()
                    bill.datum = bill_line.bill_datum

                    bill = db_session.query(Bill).first()

            bill = db_session.query(Bill).filter(
                    (Bill.rechnr > 0) &  (Bill.datum >= (bill_date - 400))).first()

    fix_bill_datum()

    return generate_output()