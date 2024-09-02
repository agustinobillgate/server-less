from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bill, Guest

def ns_invoice_getbill_cashlesscodebl(mode_type:int, qr_code:str, curr_dept:int):
    bill_recid = 0
    gname = ""
    str_qrcode:str = ""
    bill = guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_recid, gname, str_qrcode, bill, guest


        return {"bill_recid": bill_recid, "gname": gname}

    str_qrcode = trim(qr_code)

    bill = db_session.query(Bill).filter(
            (Bill.flag == 0) &  (Bill.rechnr > 0) &  (Billtyp == curr_dept) &  (func.lower(Bill.vesrdepot2) == (str_qrcode).lower()) &  (Bill.resnr == 0) &  (Bill.reslinnr == 1)).first()

    if bill:
        bill_recid = bill._recid

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == bill.gastnr)).first()

        if guest:
            gname = guest.name

    return generate_output()