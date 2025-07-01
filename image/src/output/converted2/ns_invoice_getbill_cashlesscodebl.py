#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Guest

def ns_invoice_getbill_cashlesscodebl(mode_type:int, qr_code:string, curr_dept:int):

    prepare_cache ([Bill, Guest])

    bill_recid = 0
    gname = ""
    str_qrcode:string = ""
    bill = guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_recid, gname, str_qrcode, bill, guest
        nonlocal mode_type, qr_code, curr_dept

        return {"bill_recid": bill_recid, "gname": gname}

    str_qrcode = trim(qr_code)

    bill = get_cache (Bill, {"flag": [(eq, 0)],"rechnr": [(gt, 0)],"billtyp": [(eq, curr_dept)],"vesrdepot2": [(eq, str_qrcode)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)]})

    if bill:
        bill_recid = bill._recid

        guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

        if guest:
            gname = guest.name

    return generate_output()