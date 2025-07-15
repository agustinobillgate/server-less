from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bill, Bill_line, Billjournal, Guest

def testbill():
    str:str = ""
    found_flag:bool = False
    bill = bill_line = billjournal = guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str, found_flag, bill, bill_line, billjournal, guest

        return {}


    for bill in db_session.query(Bill).order_by(Bill.datum.desc()).all():

        if bill.gastnr == 0:
            found_flag = True
            pass

            if bill.rechnr > 0:
                str = "*" + to_string(bill.rechnr) + ";"

                bill_line = db_session.query(Bill_line).filter(
                         (Bill_line.rechnr == bill.rechnr)).first()
                pass

                for billjournal in db_session.query(Billjournal).filter(
                         (Billjournal.rechnr == bill.rechnr)).order_by(Billjournal._recid).all():
                    pass

                for billjournal in db_session.query(Billjournal).filter(
                         (substring(Billjournal.bezeich, 0, len((str).lower() )) == (str).lower())).order_by(Billjournal._recid).all():
                    pass
        else:

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == bill.gastnr)).first()

            if not guest:
                pass

                if bill.rechnr > 0:

                    bill_line = db_session.query(Bill_line).filter(
                             (Bill_line.rechnr == bill.rechnr)).first()
                    pass

    if not found_flag:

    return generate_output()