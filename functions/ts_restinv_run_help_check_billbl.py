#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def ts_restinv_run_help_check_billbl(case_type:int, tischnr:int, curr_dept:int):
    pvilanguage:int = 0
    lvcarea:string = "ts-restinv"
    t_h_bill_data = []
    h_bill = None

    t_h_bill = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pvilanguage, lvcarea, t_h_bill_data, h_bill
        nonlocal case_type, tischnr, curr_dept


        nonlocal t_h_bill
        nonlocal t_h_bill_data

        return {"t-h-bill": t_h_bill_data}

    if case_type == 1:

        h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)],"flag": [(eq, 0)]})

    elif case_type == 2:

        h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)]})

    elif case_type == 3:

        h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)],"flag": [(eq, 0)]})

        if h_bill:
            t_h_bill_data.clear()
            t_h_bill = T_h_bill()
            t_h_bill_data.append(t_h_bill)

            t_h_bill.bilname = translateExtended ("Table already has an active bill", lvcarea, "")

            return generate_output()
        else:

            return generate_output()

    elif case_type == 4:

        h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)],"flag": [(eq, 0)]})

        if not h_bill:
            t_h_bill_data.clear()
            t_h_bill = T_h_bill()
            t_h_bill_data.append(t_h_bill)

            t_h_bill.bilname = translateExtended ("There is no bill active on this table" + chr_unicode(10) +\
                    "Or bill on this table has been closed" + chr_unicode(10) +\
                    "Payment not possible", lvcarea, "")

            return generate_output()
        else:

            return generate_output()

    if h_bill:
        t_h_bill = T_h_bill()
        t_h_bill_data.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    return generate_output()