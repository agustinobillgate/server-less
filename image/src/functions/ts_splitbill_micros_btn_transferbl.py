from functions.additional_functions import *
import decimal
from datetime import date
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from models import H_bill_line, Kellner, H_bill, H_artikel, Queasy

def ts_splitbill_micros_btn_transferbl(rec_id_h_bill:int, curr_select:int, multi_vat:bool, balance:decimal, transf_str:str, pay_type:int, transdate:date, price_decimal:int, exchg_rate:decimal, foreign_rate:bool, dept:int, change_str:str, add_zeit:int, hoga_card:str, cancel_str:str, curr_waiter:int, curr_room:str, user_init:str, cc_comment:str, guestnr:int, tischnr:int, double_currency:bool, amount_foreign:decimal):
    err_flag = 0
    billart = 0
    qty = 0
    price = 0
    amount = 0
    transfer_zinr = ""
    bill_date = None
    fl_code = 0
    t_h_bill_line_list = []
    payment_found:bool = False
    h_bill_line = kellner = h_bill = h_artikel = queasy = None

    vat_list = t_h_bill_line = kellner1 = None

    vat_list_list, Vat_list = create_model("Vat_list", {"vatproz":decimal, "vatamt":decimal, "netto":decimal, "betrag":decimal, "fbetrag":decimal})
    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    Kellner1 = Kellner

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, billart, qty, price, amount, transfer_zinr, bill_date, fl_code, t_h_bill_line_list, payment_found, h_bill_line, kellner, h_bill, h_artikel, queasy
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_list, t_h_bill_line_list
        return {"err_flag": err_flag, "billart": billart, "qty": qty, "price": price, "amount": amount, "transfer_zinr": transfer_zinr, "bill_date": bill_date, "fl_code": fl_code, "t-h-bill-line": t_h_bill_line_list}

    def del_queasy():

        nonlocal err_flag, billart, qty, price, amount, transfer_zinr, bill_date, fl_code, t_h_bill_line_list, payment_found, h_bill_line, kellner, h_bill, h_artikel, queasy
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_list, t_h_bill_line_list

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 >= 0) &  (Queasy.deci2 >= 0)).all():
            db_session.delete(queasy)


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id_h_bill)).first()

    h_bill_line_obj_list = []
    for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement) &  (H_artikel.artart != 0)).filter(
            (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement) &  (H_bill_line.waehrungsnr == curr_select)).all():
        if h_bill_line._recid in h_bill_line_obj_list:
            continue
        else:
            h_bill_line_obj_list.append(h_bill_line._recid)


        payment_found = True
        break

    if payment_found and multi_vat:
        err_flag = 1

        return generate_output()
    billart = 0
    qty = 1
    price = 0
    amount = - balance
    transfer_zinr = entry(1, entry(0, transf_str, "*") , " ")


    bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, 0, 1, 0, dept, amount, transdate, billart, transfer_zinr, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))

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