#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Htparam, H_bill_line

def prepare_ts_biltransferbl(h_recid:int):

    prepare_cache ([Htparam])

    multi_vat = False
    dept = 0
    splitted = False
    t_h_bill_list = []
    h_bill = htparam = h_bill_line = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal multi_vat, dept, splitted, t_h_bill_list, h_bill, htparam, h_bill_line
        nonlocal h_recid


        nonlocal t_h_bill
        nonlocal t_h_bill_list

        return {"multi_vat": multi_vat, "dept": dept, "splitted": splitted, "t-h-bill": t_h_bill_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 271)]})

    if htparam and htparam.feldtyp == 4:
        multi_vat = htparam.flogical

    h_bill = get_cache (H_bill, {"_recid": [(eq, h_recid)]})

    if h_bill:
        dept = h_bill.departement

        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, dept)],"waehrungsnr": [(gt, 0)]})

        if h_bill_line:
            splitted = True
        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    return generate_output()