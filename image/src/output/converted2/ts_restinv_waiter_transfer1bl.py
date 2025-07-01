#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def ts_restinv_waiter_transfer1bl(curr_dept:int):

    prepare_cache ([H_bill])

    hbill_list = []
    h_bill = None

    hbill = None

    hbill_list, Hbill = create_model("Hbill", {"kellner_nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal hbill_list, h_bill
        nonlocal curr_dept


        nonlocal hbill
        nonlocal hbill_list

        return {"hbill": hbill_list}

    for h_bill in db_session.query(H_bill).filter(
             (H_bill.departement == curr_dept) & (H_bill.flag == 0)).order_by(H_bill._recid).all():
        hbill = Hbill()
        hbill_list.append(hbill)

        hbill.kellner_nr = h_bill.kellner_nr

    return generate_output()