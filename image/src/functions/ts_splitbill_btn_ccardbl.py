from functions.additional_functions import *
import decimal
from datetime import date
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from models import H_bill_line, Guest, H_bill, Htparam, H_artikel, Queasy

def ts_splitbill_btn_ccardbl(rec_id_h_bill:int, billart:int, balance:decimal, paid:decimal, price_decimal:int, dept:int, transdate:date, change_str:str, price:decimal, add_zeit:int, curr_select:int, hoga_card:str, cancel_str:str, curr_waiter:int, amount_foreign:decimal, curr_room:str, user_init:str, cc_comment:str, guestnr:int):
    qty = 0
    description = ""
    amount = 0
    fl_code = 0
    bill_date = None
    t_h_bill_line_list = []
    h_bill_line = guest = h_bill = htparam = h_artikel = queasy = None

    t_h_bill_line = bill_guest = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    Bill_guest = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal qty, description, amount, fl_code, bill_date, t_h_bill_line_list, h_bill_line, guest, h_bill, htparam, h_artikel, queasy
        nonlocal bill_guest


        nonlocal t_h_bill_line, bill_guest
        nonlocal t_h_bill_line_list
        return {"qty": qty, "description": description, "amount": amount, "fl_code": fl_code, "bill_date": bill_date, "t-h-bill-line": t_h_bill_line_list}

    def del_queasy():

        nonlocal qty, description, amount, fl_code, bill_date, t_h_bill_line_list, h_bill_line, guest, h_bill, htparam, h_artikel, queasy
        nonlocal bill_guest


        nonlocal t_h_bill_line, bill_guest
        nonlocal t_h_bill_line_list

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 >= 0) &  (Queasy.deci2 >= 0)).all():
            db_session.delete(queasy)

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id_h_bill)).first()

    htparam = db_session.query(Htparam).filter(
                (htpara.paramnr == 867)).first()

    bill_guest = db_session.query(Bill_guest).filter(
                (Bill_guest.gastnr == htparam.finteger)).first()

    h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.departement == h_bill.departement) &  (H_artikel.artnr == billart)).first()
    billart = h_artikel.artnr
    qty = 1
    description = h_artikel.bezeich

    if balance == - paid:
        amount = - balance
    else:
        amount = paid
    bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, h_artikel._recid, h_artikel.artart, h_artikel.artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))

    if round(h_bill.saldo, price_decimal) == 0:
        del_queasy()

        h_bill = db_session.query(H_bill).first()
        h_bill.flag = 1

        h_bill = db_session.query(H_bill).first()
        fl_code = 1
    else:
        fl_code = 2


    for h_bill_line in db_session.query(H_bill_line).filter(
            (H_bill_line.departement == dept) &  (H_bill_line.rechnr == h_bill.rechnr)).all():
        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_list.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid

    return generate_output()