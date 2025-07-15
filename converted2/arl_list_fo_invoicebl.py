#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Bill

def arl_list_fo_invoicebl(recid_resline:int):

    prepare_cache ([Res_line, Bill])

    inp_rechnr = 0
    res_line = bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal inp_rechnr, res_line, bill
        nonlocal recid_resline

        return {"inp_rechnr": inp_rechnr}


    res_line = get_cache (Res_line, {"_recid": [(eq, recid_resline)]})

    if res_line:

        bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"zinr": [(eq, res_line.zinr)],"flag": [(eq, 0)]})

        if bill:
            inp_rechnr = bill.rechnr
    else:

        return generate_output()

    return generate_output()