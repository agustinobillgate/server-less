#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Bill, Counters

def ts_closeinv_pay_typegt1bl(bilrecid:int, recid_h_bill:int, balance_foreign:Decimal, balance:Decimal, pay_type:int):

    prepare_cache ([Bill, Counters])

    billart = 0
    qty = 0
    price = to_decimal("0.0")
    amount_foreign = to_decimal("0.0")
    amount = to_decimal("0.0")
    description = ""
    transfer_zinr = ""
    t_h_bill_list = []
    h_bill = bill = counters = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, price, amount_foreign, amount, description, transfer_zinr, t_h_bill_list, h_bill, bill, counters
        nonlocal bilrecid, recid_h_bill, balance_foreign, balance, pay_type


        nonlocal t_h_bill
        nonlocal t_h_bill_list

        return {"billart": billart, "qty": qty, "price": price, "amount_foreign": amount_foreign, "amount": amount, "description": description, "transfer_zinr": transfer_zinr, "t-h-bill": t_h_bill_list}

    bill = get_cache (Bill, {"_recid": [(eq, bilrecid)]})
    billart = 0
    qty = 1
    price =  to_decimal("0")
    amount_foreign =  - to_decimal(balance_foreign)
    amount =  - to_decimal(balance)

    if bill.rechnr == 0:

        counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
        counters.counter = counters.counter + 1
        pass
        pass
        bill.rechnr = counters.counter
        pass

    if pay_type == 2:
        description = "RmNo " + bill.zinr + " *" + to_string(bill.rechnr)
        transfer_zinr = bill.zinr

    elif pay_type == 3 or pay_type == 4:
        description = "Transfer" + " *" + to_string(bill.rechnr)

    h_bill = get_cache (H_bill, {"_recid": [(eq, recid_h_bill)]})
    h_bill.bilname = bill.name


    pass
    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()