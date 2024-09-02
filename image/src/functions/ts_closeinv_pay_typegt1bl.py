from functions.additional_functions import *
import decimal
from models import H_bill, Bill, Counters

def ts_closeinv_pay_typegt1bl(bilrecid:int, recid_h_bill:int, balance_foreign:decimal, balance:decimal, pay_type:int):
    billart = 0
    qty = 0
    price = 0
    amount_foreign = 0
    amount = 0
    description = ""
    transfer_zinr = ""
    t_h_bill_list = []
    h_bill = bill = counters = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, price, amount_foreign, amount, description, transfer_zinr, t_h_bill_list, h_bill, bill, counters


        nonlocal t_h_bill
        nonlocal t_h_bill_list
        return {"billart": billart, "qty": qty, "price": price, "amount_foreign": amount_foreign, "amount": amount, "description": description, "transfer_zinr": transfer_zinr, "t-h-bill": t_h_bill_list}

    bill = db_session.query(Bill).filter(
            (Bill._recid == bilrecid)).first()
    billart = 0
    qty = 1
    price = 0
    amount_foreign = - balance_foreign
    amount = - balance

    if bill.rechnr == 0:

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 3)).first()
        counters = counters + 1

        counters = db_session.query(Counters).first()

        bill = db_session.query(Bill).first()
        bill.rechnr = counters

        bill = db_session.query(Bill).first()

    if pay_type == 2:
        description = "RmNo " + bill.zinr + " *" + to_string(bill.rechnr)
        transfer_zinr = bill.zinr

    elif pay_type == 3 or pay_type == 4:
        description = "Transfer" + " *" + to_string(bill.rechnr)

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == recid_h_bill)).first()
    h_bill.bilname = bill.name

    h_bill = db_session.query(H_bill).first()
    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()