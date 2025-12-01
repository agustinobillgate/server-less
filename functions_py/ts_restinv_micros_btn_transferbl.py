#using conversion tools version: 1.0.0.117
# ----------------------------------------
# Rd, 01/12/2025, with_for_update added
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def ts_restinv_micros_btn_transferbl(h_bill_recid:int, balance_foreign:Decimal, balance:Decimal, transf_str:string):
    billart = 0
    qty = 0
    price = to_decimal("0.0")
    amount_foreign = to_decimal("0.0")
    amount = to_decimal("0.0")
    gname = ""
    desc_str = ""
    transfer_zinr = ""
    t_h_bill_data = []
    h_bill = None

    t_h_bill = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    db_session = local_storage.db_session
    transf_str = transf_str.strip()

    def generate_output():
        nonlocal billart, qty, price, amount_foreign, amount, gname, desc_str, transfer_zinr, t_h_bill_data, h_bill
        nonlocal h_bill_recid, balance_foreign, balance, transf_str


        nonlocal t_h_bill
        nonlocal t_h_bill_data

        return {"billart": billart, "qty": qty, "price": price, "amount_foreign": amount_foreign, "amount": amount, "gname": gname, "desc_str": desc_str, "transfer_zinr": transfer_zinr, "t-h-bill": t_h_bill_data}

    # h_bill = get_cache (H_bill, {"_recid": [(eq, h_bill_recid)]})
    h_bill = db_session.query(H_bill).filter(
        (H_bill._recid == h_bill_recid)).with_for_update().first()
    
    billart = 0
    qty = 1
    price =  to_decimal("0")
    amount_foreign =  - to_decimal(balance_foreign)
    amount =  - to_decimal(balance)
    gname = ""
    desc_str = transf_str
    gname = transf_str
    transfer_zinr = entry(1, entry(0, transf_str, "*") , " ")


    pass
    h_bill.bilname = gname
    h_bill.flag = 1


    pass
    t_h_bill = T_h_bill()
    t_h_bill_data.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()