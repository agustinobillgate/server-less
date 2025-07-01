#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from models import H_bill_line, Guest, H_bill, Htparam, H_artikel, Queasy

def ts_splitbill_btn_ccardbl(rec_id_h_bill:int, billart:int, balance:Decimal, paid:Decimal, price_decimal:int, dept:int, transdate:date, change_str:string, price:Decimal, add_zeit:int, curr_select:int, hoga_card:string, cancel_str:string, curr_waiter:int, amount_foreign:Decimal, curr_room:string, user_init:string, cc_comment:string, guestnr:int):

    prepare_cache ([H_bill, Htparam, H_artikel])

    qty = 0
    description = ""
    amount = to_decimal("0.0")
    fl_code = 0
    bill_date = None
    t_h_bill_line_list = []
    h_bill_line = guest = h_bill = htparam = h_artikel = queasy = None

    t_h_bill_line = bill_guest = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    Bill_guest = create_buffer("Bill_guest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal qty, description, amount, fl_code, bill_date, t_h_bill_line_list, h_bill_line, guest, h_bill, htparam, h_artikel, queasy
        nonlocal rec_id_h_bill, billart, balance, paid, price_decimal, dept, transdate, change_str, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr
        nonlocal bill_guest


        nonlocal t_h_bill_line, bill_guest
        nonlocal t_h_bill_line_list

        return {"qty": qty, "description": description, "amount": amount, "fl_code": fl_code, "bill_date": bill_date, "t-h-bill-line": t_h_bill_line_list}

    def del_queasy():

        nonlocal qty, description, amount, fl_code, bill_date, t_h_bill_line_list, h_bill_line, guest, h_bill, htparam, h_artikel, queasy
        nonlocal rec_id_h_bill, billart, balance, paid, price_decimal, dept, transdate, change_str, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr
        nonlocal bill_guest


        nonlocal t_h_bill_line, bill_guest
        nonlocal t_h_bill_line_list

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 4) & (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) & (Queasy.number2 >= 0) & (Queasy.deci2 >= 0)).order_by(Queasy._recid).all():
            db_session.delete(queasy)
        pass


    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id_h_bill)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 867)]})

    bill_guest = db_session.query(Bill_guest).filter(
                 (Bill_guest.gastnr == htparam.finteger)).first()

    h_artikel = get_cache (H_artikel, {"departement": [(eq, h_bill.departement)],"artnr": [(eq, billart)]})
    billart = h_artikel.artnr
    qty = 1
    description = h_artikel.bezeich

    if balance == - paid:
        amount =  - to_decimal(balance)
    else:
        amount =  to_decimal(paid)
    bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, h_artikel._recid, h_artikel.artart, h_artikel.artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))

    if round(h_bill.saldo, price_decimal) == 0:
        del_queasy()
        pass
        h_bill.flag = 1
        pass
        fl_code = 1
    else:
        fl_code = 2

    for h_bill_line in db_session.query(H_bill_line).filter(
             (H_bill_line.departement == dept) & (H_bill_line.rechnr == h_bill.rechnr)).order_by(H_bill_line._recid).all():
        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_list.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid

    return generate_output()