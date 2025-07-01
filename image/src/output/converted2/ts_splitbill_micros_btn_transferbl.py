#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from models import H_bill_line, Kellner, H_bill, H_artikel, Queasy

def ts_splitbill_micros_btn_transferbl(rec_id_h_bill:int, curr_select:int, multi_vat:bool, balance:Decimal, transf_str:string, pay_type:int, transdate:date, price_decimal:int, exchg_rate:Decimal, foreign_rate:bool, dept:int, change_str:string, add_zeit:int, hoga_card:string, cancel_str:string, curr_waiter:int, curr_room:string, user_init:string, cc_comment:string, guestnr:int, tischnr:int, double_currency:bool, amount_foreign:Decimal):

    prepare_cache ([H_bill])

    err_flag = 0
    billart = 0
    qty = 0
    price = to_decimal("0.0")
    amount = to_decimal("0.0")
    transfer_zinr = ""
    bill_date = None
    fl_code = 0
    t_h_bill_line_list = []
    payment_found:bool = False
    h_bill_line = kellner = h_bill = h_artikel = queasy = None

    vat_list = t_h_bill_line = kellner1 = None

    vat_list_list, Vat_list = create_model("Vat_list", {"vatproz":Decimal, "vatamt":Decimal, "netto":Decimal, "betrag":Decimal, "fbetrag":Decimal})
    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    Kellner1 = create_buffer("Kellner1",Kellner)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, billart, qty, price, amount, transfer_zinr, bill_date, fl_code, t_h_bill_line_list, payment_found, h_bill_line, kellner, h_bill, h_artikel, queasy
        nonlocal rec_id_h_bill, curr_select, multi_vat, balance, transf_str, pay_type, transdate, price_decimal, exchg_rate, foreign_rate, dept, change_str, add_zeit, hoga_card, cancel_str, curr_waiter, curr_room, user_init, cc_comment, guestnr, tischnr, double_currency, amount_foreign
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_list, t_h_bill_line_list

        return {"amount_foreign": amount_foreign, "err_flag": err_flag, "billart": billart, "qty": qty, "price": price, "amount": amount, "transfer_zinr": transfer_zinr, "bill_date": bill_date, "fl_code": fl_code, "t-h-bill-line": t_h_bill_line_list}

    def del_queasy():

        nonlocal err_flag, billart, qty, price, amount, transfer_zinr, bill_date, fl_code, t_h_bill_line_list, payment_found, h_bill_line, kellner, h_bill, h_artikel, queasy
        nonlocal rec_id_h_bill, curr_select, multi_vat, balance, transf_str, pay_type, transdate, price_decimal, exchg_rate, foreign_rate, dept, change_str, add_zeit, hoga_card, cancel_str, curr_waiter, curr_room, user_init, cc_comment, guestnr, tischnr, double_currency, amount_foreign
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_list, t_h_bill_line_list

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 4) & (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) & (Queasy.number2 >= 0) & (Queasy.deci2 >= 0)).order_by(Queasy._recid).all():
            db_session.delete(queasy)

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id_h_bill)]})

    h_bill_line_obj_list = {}
    for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart != 0)).filter(
             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.waehrungsnr == curr_select)).order_by(H_bill_line._recid).yield_per(100):
        if h_bill_line_obj_list.get(h_bill_line._recid):
            continue
        else:
            h_bill_line_obj_list[h_bill_line._recid] = True


        payment_found = True
        break

    if payment_found and multi_vat:
        err_flag = 1

        return generate_output()
    billart = 0
    qty = 1
    price =  to_decimal("0")
    amount =  - to_decimal(balance)
    transfer_zinr = entry(1, entry(0, transf_str, "*") , " ")


    bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, 0, 1, 0, dept, amount, transdate, billart, transfer_zinr, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))

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