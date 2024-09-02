from functions.additional_functions import *
import decimal
from models import Guest, Htparam

def fo_invoice_chg_bill_number3bl(bill_gastnr:int):
    kreditlimit = 0
    guest = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal kreditlimit, guest, htparam


        return {"kreditlimit": kreditlimit}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == bill_gastnr)).first()

    if guest.kreditlimit != 0:
        kreditlimit = guest.kreditlimit
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 68)).first()

        if htparam.fdecimal != 0:
            kreditlimit = htparam.fdecimal
        else:
            kreditlimit = htparam.finteger

    return generate_output()