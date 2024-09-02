from functions.additional_functions import *
import decimal
from datetime import date
from functions.check_rpaymentbl import check_rpaymentbl
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from models import H_bill_line, Guest, H_bill, H_artikel, Queasy

def ts_splitbill_btn_transfer_paytype1bl(pvilanguage:int, rec_id_h_bill:int, dept:int, guestnr:int, paid:decimal, price_decimal:int, transdate:date, change_str:str, tischnr:int, add_zeit:int, curr_select:int, hoga_card:str, cancel_str:str, curr_waiter:int, amount_foreign:decimal, curr_room:str, user_init:str, cc_comment:str):
    billart = 0
    qty = 0
    description = ""
    amount = 0
    price = 0
    bill_date = None
    fl_code = 0
    msg_str = ""
    t_h_bill_line_list = []
    h_bill_line = guest = h_bill = h_artikel = queasy = None

    t_h_bill_line = bill_guest = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    Bill_guest = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, amount, price, bill_date, fl_code, msg_str, t_h_bill_line_list, h_bill_line, guest, h_bill, h_artikel, queasy
        nonlocal bill_guest


        nonlocal t_h_bill_line, bill_guest
        nonlocal t_h_bill_line_list
        return {"billart": billart, "qty": qty, "description": description, "amount": amount, "price": price, "bill_date": bill_date, "fl_code": fl_code, "msg_str": msg_str, "t-h-bill-line": t_h_bill_line_list}

    def del_queasy():

        nonlocal billart, qty, description, amount, price, bill_date, fl_code, msg_str, t_h_bill_line_list, h_bill_line, guest, h_bill, h_artikel, queasy
        nonlocal bill_guest


        nonlocal t_h_bill_line, bill_guest
        nonlocal t_h_bill_line_list

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 >= 0) &  (Queasy.deci2 >= 0)).all():
            db_session.delete(queasy)

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id_h_bill)).first()
    billart, msg_str = get_output(check_rpaymentbl(pvilanguage, guestnr, h_bill.departement))

    if billart > 0:

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.departement == h_bill.departement) &  (H_artikel.artnrfront == billart) &  (H_artikel.artart == 2)).first()

        if h_artikel:

            bill_guest = db_session.query(Bill_guest).filter(
                    (Bill_guest.gastnr == guestnr)).first()
            billart = h_artikel.artnr
            qty = 1
            description = h_artikel.bezeich
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
        else:
            fl_code = 3

    for h_bill_line in db_session.query(H_bill_line).filter(
            (H_bill_line.departement == dept) &  (H_bill_line.rechnr == h_bill.rechnr)).all():
        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_list.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid

    return generate_output()