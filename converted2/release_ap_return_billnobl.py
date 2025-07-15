#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit

def release_ap_return_billnobl(case_type:int, bill_no:string, i_datum:date):

    prepare_cache ([L_kredit])

    datum = None
    saldo = to_decimal("0.0")
    avail_kredit = False
    l_kredit = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum, saldo, avail_kredit, l_kredit
        nonlocal case_type, bill_no, i_datum

        return {"datum": datum, "saldo": saldo, "avail_kredit": avail_kredit}


    if case_type == 1:

        l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, bill_no)],"zahlkonto": [(eq, 0)],"counter": [(ne, 0)]})

        if l_kredit:
            avail_kredit = True
            datum = l_kredit.rgdatum
            saldo =  to_decimal(l_kredit.saldo)

    elif case_type == 2:

        l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, bill_no)],"rgdatum": [(eq, i_datum)],"zahlkonto": [(eq, 0)],"counter": [(ne, 0)]})

        if l_kredit:
            saldo =  to_decimal(l_kredit.saldo)
            avail_kredit = True

    return generate_output()