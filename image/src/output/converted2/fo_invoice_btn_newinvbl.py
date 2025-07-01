#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.create_newbillbl import create_newbillbl
from models import Bill, Res_line

def fo_invoice_btn_newinvbl(bil_recid:int, bill_anzahl:int):

    prepare_cache ([Bill, Res_line])

    bill = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill, res_line
        nonlocal bil_recid, bill_anzahl

        return {}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if not bill:

        return generate_output()

    res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})
    bil_recid = get_output(create_newbillbl(res_line.resnr, res_line.reslinnr, bill.parent_nr, bill_anzahl))

    return generate_output()