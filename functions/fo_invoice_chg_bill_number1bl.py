#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Res_line

def fo_invoice_chg_bill_number1bl(bil_recid:int, curr_billnr:int):

    prepare_cache ([Bill, Res_line])

    bill = res_line = None

    bill1 = None

    Bill1 = create_buffer("Bill1",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill, res_line
        nonlocal bil_recid, curr_billnr
        nonlocal bill1


        nonlocal bill1

        return {"bil_recid": bil_recid}


    bill1 = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if bill1:

        bill = get_cache (Bill, {"resnr": [(eq, bill1.resnr)],"parent_nr": [(eq, bill1.parent_nr)],"flag": [(eq, 0)],"zinr": [(eq, bill1.zinr)],"billnr": [(eq, curr_billnr)]})

        if not bill:

            bill = get_cache (Bill, {"resnr": [(eq, bill1.resnr)],"parent_nr": [(eq, bill1.parent_nr)],"flag": [(eq, 0)],"billnr": [(eq, curr_billnr)]})

            if bill:

                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                if res_line:
                    bill.zinr = res_line.zinr
                pass

        if bill:
            bil_recid = bill._recid
    else:

        return generate_output()

    return generate_output()