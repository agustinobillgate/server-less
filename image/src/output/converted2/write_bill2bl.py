#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Res_line

t_bill_list, T_bill = create_model_like(Bill)

def write_bill2bl(t_bill_list:[T_bill]):

    prepare_cache ([Bill, Res_line])

    success_flag = False
    bill = res_line = None

    t_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bill, res_line


        nonlocal t_bill

        return {"success_flag": success_flag}

    t_bill = query(t_bill_list, first=True)

    if t_bill:

        bill = get_cache (Bill, {"rechnr": [(eq, t_bill.rechnr)]})

        if not bill:
            bill = Bill()
            db_session.add(bill)

        buffer_copy(t_bill, bill)
        success_flag = True

        if bill.reslinnr != bill.parent_nr:

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

            if res_line and res_line.resstatus == 12 and res_line.zinr != bill.zinr:
                pass
                res_line.zinr = bill.zinr


                pass
        pass

    return generate_output()