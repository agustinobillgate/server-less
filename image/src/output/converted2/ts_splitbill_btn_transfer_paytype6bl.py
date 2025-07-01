#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from models import H_bill_line, Kellner, H_bill, H_artikel, Kellne1, H_umsatz, Umsatz, H_compli, Queasy

def ts_splitbill_btn_transfer_paytype6bl(rec_id_h_bill:int, curr_select:int, p_artnr:int, balance:Decimal, price_decimal:int, transdate:date, dept:int, change_str:string, price:Decimal, add_zeit:int, hoga_card:string, cancel_str:string, curr_waiter:int, amount_foreign:Decimal, curr_room:string, user_init:string, cc_comment:string, guestnr:int, tischnr:int):

    prepare_cache ([Kellner, H_bill, H_artikel, H_umsatz, Umsatz, H_compli])

    billart = 0
    qty = 0
    description = ""
    amount = to_decimal("0.0")
    bill_date = None
    fl_code = 0
    t_h_bill_line_list = []
    h_bill_line = kellner = h_bill = h_artikel = kellne1 = h_umsatz = umsatz = h_compli = queasy = None

    t_h_bill_line = kellner1 = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    Kellner1 = create_buffer("Kellner1",Kellner)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, amount, bill_date, fl_code, t_h_bill_line_list, h_bill_line, kellner, h_bill, h_artikel, kellne1, h_umsatz, umsatz, h_compli, queasy
        nonlocal rec_id_h_bill, curr_select, p_artnr, balance, price_decimal, transdate, dept, change_str, price, add_zeit, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr, tischnr
        nonlocal kellner1


        nonlocal t_h_bill_line, kellner1
        nonlocal t_h_bill_line_list

        return {"billart": billart, "qty": qty, "description": description, "amount": amount, "bill_date": bill_date, "fl_code": fl_code, "t-h-bill-line": t_h_bill_line_list}

    def adjust_mealcoupon_umsatz(curr_select:int):

        nonlocal billart, qty, description, bill_date, fl_code, t_h_bill_line_list, h_bill_line, kellner, h_bill, h_artikel, kellne1, h_umsatz, umsatz, h_compli, queasy
        nonlocal rec_id_h_bill, p_artnr, balance, price_decimal, transdate, dept, change_str, price, add_zeit, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr, tischnr
        nonlocal kellner1


        nonlocal t_h_bill_line, kellner1
        nonlocal t_h_bill_line_list

        h_mwst:Decimal = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        epreis:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        h_bline = None
        h_art = None
        H_bline =  create_buffer("H_bline",H_bill_line)
        H_art =  create_buffer("H_art",H_artikel)

        kellner1 = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})

        kellne1 = get_cache (Kellne1, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})

        h_bline_obj_list = {}
        for h_bline, h_art in db_session.query(H_bline, H_art).join(H_art,(H_art.artnr == H_bline.artnr) & (H_art.departement == H_bline.departement) & (H_art.artart == 0)).filter(
                 (H_bline.rechnr == h_bill.rechnr) & (h_bill_line.waehrungsnr == curr_select)).order_by(H_bline._recid).all():
            if h_bline_obj_list.get(h_bline._recid):
                continue
            else:
                h_bline_obj_list[h_bline._recid] = True

            h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_art.artnr)],"departement": [(eq, h_art.departement)],"datum": [(eq, h_bline.bill_datum)]})
            h_umsatz.betrag =  to_decimal(h_umsatz.betrag) - to_decimal(h_bline.betrag)
            h_umsatz.anzahl = h_umsatz.anzahl - h_bline.anzahl
            pass

            umsatz = get_cache (Umsatz, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, h_art.departement)],"datum": [(eq, h_bline.bill_datum)]})
            umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(h_bline.betrag)
            umsatz.anzahl = umsatz.anzahl - h_bline.anzahl
            pass

            umsatz = get_cache (Umsatz, {"artnr": [(eq, kellner1.kumsatz_nr)],"departement": [(eq, h_bline.departement)],"datum": [(eq, h_bline.bill_datum)]})
            umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(h_bline.betrag)
            umsatz.anzahl = umsatz.anzahl - h_bline.anzahl
            pass
            h_compli = H_compli()
            db_session.add(h_compli)

            h_compli.datum = h_bline.bill_datum
            h_compli.departement = h_bline.departement
            h_compli.rechnr = h_bline.rechnr
            h_compli.artnr = h_bline.artnr
            h_compli.anzahl = h_bline.anzahl
            h_compli.epreis =  to_decimal(h_bline.epreis)
            h_compli.p_artnr = p_artnr


    def del_queasy():

        nonlocal billart, qty, description, amount, bill_date, fl_code, t_h_bill_line_list, h_bill_line, kellner, h_bill, h_artikel, kellne1, h_umsatz, umsatz, h_compli, queasy
        nonlocal rec_id_h_bill, curr_select, p_artnr, balance, price_decimal, transdate, dept, change_str, price, add_zeit, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr, tischnr
        nonlocal kellner1


        nonlocal t_h_bill_line, kellner1
        nonlocal t_h_bill_line_list

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 4) & (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) & (Queasy.number2 >= 0) & (Queasy.deci2 >= 0)).order_by(Queasy._recid).all():
            db_session.delete(queasy)
        pass


    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id_h_bill)]})
    adjust_mealcoupon_umsatz(curr_select)

    h_artikel = get_cache (H_artikel, {"departement": [(eq, h_bill.departement)],"artnr": [(eq, p_artnr)]})
    billart = h_artikel.artnr
    qty = 1
    description = h_artikel.bezeich
    amount =  - to_decimal(balance)
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
             (H_bill_line.departement == dept)).order_by(H_bill_line._recid).all():
        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_list.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid

    return generate_output()