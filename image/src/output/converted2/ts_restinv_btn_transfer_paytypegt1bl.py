#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Bill, Counters, Res_line

def ts_restinv_btn_transfer_paytypegt1bl(bilrecid:int, h_bill_recid:int, balance_foreign:Decimal, balance:Decimal, pay_type:int):

    prepare_cache ([Bill, Counters, Res_line])

    billart = 0
    qty = 0
    price = to_decimal("0.0")
    amount_foreign = to_decimal("0.0")
    amount = to_decimal("0.0")
    gname = ""
    description = ""
    transfer_zinr = ""
    t_h_bill_list = []
    h_bill = bill = counters = res_line = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, price, amount_foreign, amount, gname, description, transfer_zinr, t_h_bill_list, h_bill, bill, counters, res_line
        nonlocal bilrecid, h_bill_recid, balance_foreign, balance, pay_type


        nonlocal t_h_bill
        nonlocal t_h_bill_list

        return {"billart": billart, "qty": qty, "price": price, "amount_foreign": amount_foreign, "amount": amount, "gname": gname, "description": description, "transfer_zinr": transfer_zinr, "t-h-bill": t_h_bill_list}

    bill = get_cache (Bill, {"_recid": [(eq, bilrecid)]})

    if not bill:

        return generate_output()

    h_bill = get_cache (H_bill, {"_recid": [(eq, h_bill_recid)]})

    if not h_bill:

        return generate_output()
    billart = 0
    qty = 1
    price =  to_decimal("0")
    amount_foreign =  - to_decimal(balance_foreign)
    amount =  - to_decimal(balance)
    gname = ""

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

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

        if res_line and h_bill:
            gname = res_line.name
            pass
            h_bill.bilname = gname
            pass
        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    elif pay_type == 3 or pay_type == 4:
        description = "Transfer" + " *" + to_string(bill.rechnr)
        gname = bill.name
        pass
        h_bill.bilname = gname
        pass
        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    return generate_output()