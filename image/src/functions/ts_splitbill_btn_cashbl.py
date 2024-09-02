from functions.additional_functions import *
import decimal
from datetime import date
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from models import H_bill_line, Htparam, H_artikel, H_bill, Queasy

def ts_splitbill_btn_cashbl(pvilanguage:int, dept:int, rec_id_h_bill:int, multi_cash:bool, cash_artno:int, cash_foreign:bool, pay_voucher:bool, full_paid:bool, voucher_nr:str, amt:decimal, changed:decimal, changed_foreign:decimal, lchange:decimal, amount:decimal, transdate:date, change_str:str, tischnr:int, add_zeit:int, curr_select:int, hoga_card:str, cancel_str:str, curr_waiter:int, amount_foreign:decimal, curr_room:str, user_init:str, cc_comment:str, guestnr:int, cash_type:int):
    billart = 0
    qty = 0
    description = ""
    price = 0
    answer = False
    bill_date = None
    fl_code = 0
    t_h_bill_line_list = []
    lvcarea:str = "TS_splitbill"
    price_decimal:int = 0
    h_bill_line = htparam = h_artikel = h_bill = queasy = None

    t_h_bill_line = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, price, answer, bill_date, fl_code, t_h_bill_line_list, lvcarea, price_decimal, h_bill_line, htparam, h_artikel, h_bill, queasy


        nonlocal t_h_bill_line
        nonlocal t_h_bill_line_list
        return {"billart": billart, "qty": qty, "description": description, "price": price, "answer": answer, "bill_date": bill_date, "fl_code": fl_code, "t-h-bill-line": t_h_bill_line_list}

    def del_queasy():

        nonlocal billart, qty, description, price, answer, bill_date, fl_code, t_h_bill_line_list, lvcarea, price_decimal, h_bill_line, htparam, h_artikel, h_bill, queasy


        nonlocal t_h_bill_line
        nonlocal t_h_bill_line_list

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 >= 0) &  (Queasy.deci2 >= 0)).all():
            db_session.delete(queasy)

    if multi_cash or cash_type == 1:
        billart = cash_artno
    else:

        if cash_foreign:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 854)).first()
        else:

            if not pay_voucher:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 855)).first()
            else:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 1001)).first()
        billart = htparam.finteger

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.departement == dept) &  (H_artikel.artnr == billart)).first()
    qty = 1
    description = h_artikel.bezeich

    if cash_type == 1:
        description = replace_str(description, " ", "")

    if voucher_nr != "":
        description = description + " " + voucher_nr
    price = 0
    bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, h_artikel._recid, h_artikel.artart, h_artikel.artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))
    answer = False

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id_h_bill)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    if full_paid and amt != 0:
        add_zeit = 1

        if multi_cash:

            if changed != 0:
                amount = changed
                amount_foreign = changed_foreign
                change_str = translateExtended ("(Change)", lvcarea, "")
                bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, h_artikel._recid, h_artikel.artart, h_artikel.artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))

            if lchange != 0:
                add_zeit = add_zeit + 1
                amount = lchange
                amount_foreign = lchange
                change_str = translateExtended ("(Change)", lvcarea, "")

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 855)).first()
                billart = htparam.finteger

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.departement == dept) &  (H_artikel.artnr == billart)).first()
                description = h_artikel.bezeich
                change_str = translateExtended ("(Change)", lvcarea, "")
                bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, h_artikel._recid, h_artikel.artart, h_artikel.artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))
        else:
            amount = - amt
            change_str = translateExtended ("(Change)", lvcarea, "")
            bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, h_artikel._recid, h_artikel.artart, h_artikel.artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))
    add_zeit = 0

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