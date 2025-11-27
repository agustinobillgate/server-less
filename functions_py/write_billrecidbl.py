#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Bill

t_bill_data, T_bill = create_model_like(Bill, {"bl_recid":int})

def write_billrecidbl(t_bill_data:[T_bill]):
    success_flag = False
    bill = None

    t_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bill


        nonlocal t_bill

        return {"success_flag": success_flag}

    t_bill = query(t_bill_data, first=True)

    if t_bill:

        # bill = get_cache (Bill, {"_recid": [(eq, t_bill.bl_recid)]})
        bill = db_session.query(Bill).filter(Bill._recid == t_bill.bl_recid).with_for_update().first()

        if bill:
            buffer_copy(t_bill, bill,except_fields=["flag"])
            success_flag = True

    return generate_output()