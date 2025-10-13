#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Res_line

t_bill_data, T_bill = create_model_like(Bill, {"bl_recid":int})

def write_billbl(t_bill_data:[T_bill]):

    prepare_cache ([Bill, Res_line])

    success_flag = False
    bill = res_line = None

    t_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bill, res_line


        nonlocal t_bill

        return {"success_flag": success_flag}

    t_bill = query(t_bill_data, first=True)

    if t_bill:

        bill = get_cache (Bill, {"_recid": [(eq, t_bill.bl_recid)]})

        if not bill:
            bill = Bill()
            db_session.add(bill)

        buffer_copy(t_bill, bill,except_fields=["flag"])
        pass
        success_flag = True

        if bill.reslinnr != bill.parent_nr:

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

            if res_line and res_line.resstatus == 12 and res_line.zinr != bill.zinr:
                pass
                res_line.zinr = bill.zinr


                pass

    return generate_output()