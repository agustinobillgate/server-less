#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def read_h_bill1bl(case_type:int, rechno:int, deptno:int):
    t_h_bill_list = []
    h_bill = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"hbill_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_bill_list, h_bill
        nonlocal case_type, rechno, deptno


        nonlocal t_h_bill
        nonlocal t_h_bill_list

        return {"t-h-bill": t_h_bill_list}

    def cr_hbill():

        nonlocal t_h_bill_list, h_bill
        nonlocal case_type, rechno, deptno


        nonlocal t_h_bill
        nonlocal t_h_bill_list


        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.hbill_recid = h_bill._recid


    if case_type == 1:

        h_bill = get_cache (H_bill, {"rechnr": [(eq, rechno)],"departement": [(eq, deptno)]})

        if h_bill:
            cr_hbill()

    return generate_output()