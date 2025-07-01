#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.release_ap_return_billnobl import release_ap_return_billnobl

def ap_cancelpayment_querybl(bill_no:int, datum:date):
    datum1 = None
    saldo = to_decimal("0.0")
    avail_kredit = False
    msg_str = ""

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum1, saldo, avail_kredit, msg_str
        nonlocal bill_no, datum

        return {"datum1": datum1, "saldo": saldo, "avail_kredit": avail_kredit, "msg_str": msg_str}


    if datum == None:
        datum1, saldo, avail_kredit = get_output(release_ap_return_billnobl(1, bill_no, None))
    else:
        datum1, saldo, avail_kredit = get_output(release_ap_return_billnobl(2, bill_no, datum))

        if not avail_kredit:
            msg_str = "No such A/P record found!"

            return generate_output()

    return generate_output()