from functions.additional_functions import *
import decimal
from models import Guest, Htparam

def fo_invoice_chg_bill_number3bl(bill_gastnr:int):
    kreditlimit = to_decimal("0.0")
    guest = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal kreditlimit, guest, htparam
        nonlocal bill_gastnr


        return {"kreditlimit": kreditlimit}


    guest = db_session.query(Guest).filter(
             (Guest.gastnr == bill_gastnr)).first()

    if guest.kreditlimit != 0:
        kreditlimit =  to_decimal(guest.kreditlimit)
    else:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 68)).first()

        if htparam.fdecimal != 0:
            kreditlimit =  to_decimal(htparam.fdecimal)
        else:
            kreditlimit =  to_decimal(htparam.finteger)

    return generate_output()