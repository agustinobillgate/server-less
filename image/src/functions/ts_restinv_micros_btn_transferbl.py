from functions.additional_functions import *
import decimal
from models import H_bill

def ts_restinv_micros_btn_transferbl(h_bill_recid:int, balance_foreign:decimal, balance:decimal, transf_str:str):
    billart = 0
    qty = 0
    price = 0
    amount_foreign = 0
    amount = 0
    gname = ""
    desc_str = ""
    transfer_zinr = ""
    t_h_bill_list = []
    h_bill = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, price, amount_foreign, amount, gname, desc_str, transfer_zinr, t_h_bill_list, h_bill


        nonlocal t_h_bill
        nonlocal t_h_bill_list
        return {"billart": billart, "qty": qty, "price": price, "amount_foreign": amount_foreign, "amount": amount, "gname": gname, "desc_str": desc_str, "transfer_zinr": transfer_zinr, "t-h-bill": t_h_bill_list}

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == h_bill_recid)).first()
    billart = 0
    qty = 1
    price = 0
    amount_foreign = - balance_foreign
    amount = - balance
    gname = ""
    desc_str = transf_str
    gname = transf_str
    transfer_zinr = entry(1, entry(0, transf_str, "*") , " ")

    h_bill = db_session.query(H_bill).first()
    h_bill.bilname = gname
    h_bill.flag = 1

    h_bill = db_session.query(H_bill).first()
    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()