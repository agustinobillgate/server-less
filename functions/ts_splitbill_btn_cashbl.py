#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from models import H_bill_line, Htparam, H_artikel, H_bill, Queasy

def ts_splitbill_btn_cashbl(pvilanguage:int, dept:int, rec_id_h_bill:int, multi_cash:bool, cash_artno:int, cash_foreign:bool, pay_voucher:bool, full_paid:bool, voucher_nr:string, amt:Decimal, changed:Decimal, changed_foreign:Decimal, lchange:Decimal, amount:Decimal, transdate:date, change_str:string, tischnr:int, add_zeit:int, curr_select:int, hoga_card:string, cancel_str:string, curr_waiter:int, amount_foreign:Decimal, curr_room:string, user_init:string, cc_comment:string, guestnr:int, cash_type:int):

    prepare_cache ([Htparam, H_artikel, H_bill])

    billart = 0
    qty = 0
    description = ""
    price = to_decimal("0.0")
    answer = False
    bill_date = None
    fl_code = 0
    t_h_bill_line_data = []
    lvcarea:string = "TS-splitbill"
    price_decimal:int = 0
    h_bill_line = htparam = h_artikel = h_bill = queasy = None

    t_h_bill_line = None

    t_h_bill_line_data, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, price, answer, bill_date, fl_code, t_h_bill_line_data, lvcarea, price_decimal, h_bill_line, htparam, h_artikel, h_bill, queasy
        nonlocal pvilanguage, dept, rec_id_h_bill, multi_cash, cash_artno, cash_foreign, pay_voucher, full_paid, voucher_nr, amt, changed, changed_foreign, lchange, amount, transdate, change_str, tischnr, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr, cash_type


        nonlocal t_h_bill_line
        nonlocal t_h_bill_line_data

        return {"billart": billart, "qty": qty, "description": description, "price": price, "answer": answer, "bill_date": bill_date, "fl_code": fl_code, "t-h-bill-line": t_h_bill_line_data}

    if multi_cash or cash_type == 1:
        billart = cash_artno
    else:

        if cash_foreign:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 854)]})
        else:

            if not pay_voucher:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 855)]})
            else:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 1001)]})
        billart = htparam.finteger

    h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, billart)]})
    qty = 1
    description = h_artikel.bezeich

    if cash_type == 1:
        description = replace_str(description, " ", "")

    if voucher_nr != "":
        description = description + " " + voucher_nr
    price =  to_decimal("0")
    bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, h_artikel._recid, h_artikel.artart, h_artikel.artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))
    answer = False

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id_h_bill)]})

    if h_bill:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

        if htparam:
            price_decimal = htparam.finteger

        if full_paid and amt != 0:
            add_zeit = 1

            if multi_cash:

                if changed != 0:
                    amount =  to_decimal(changed)
                    amount_foreign =  to_decimal(changed_foreign)
                    change_str = translateExtended ("(Change)", lvcarea, "")
                    bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, h_artikel._recid, h_artikel.artart, h_artikel.artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))

                if lchange != 0:
                    add_zeit = add_zeit + 1
                    amount =  to_decimal(lchange)
                    amount_foreign =  to_decimal(lchange)
                    change_str = translateExtended ("(Change)", lvcarea, "")

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 855)]})
                    billart = htparam.finteger

                    h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, billart)]})
                    description = h_artikel.bezeich
                    change_str = translateExtended ("(Change)", lvcarea, "")
                    bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, h_artikel._recid, h_artikel.artart, h_artikel.artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))
            else:
                amount =  - to_decimal(amt)
                change_str = translateExtended ("(Change)", lvcarea, "")
                bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, h_artikel._recid, h_artikel.artart, h_artikel.artnrfront, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))
        add_zeit = 0

        if round(h_bill.saldo, price_decimal) == 0:

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 4) & (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) & (Queasy.number2 >= 0) & (Queasy.deci2 >= 0)).order_by(Queasy._recid).all():
                db_session.delete(queasy)
            pass
            h_bill.flag = 1
            pass
            fl_code = 1
        else:
            fl_code = 2

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.departement == dept) & (H_bill_line.rechnr == h_bill.rechnr)).order_by(H_bill_line._recid).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_data.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)
            t_h_bill_line.rec_id = h_bill_line._recid

    return generate_output()