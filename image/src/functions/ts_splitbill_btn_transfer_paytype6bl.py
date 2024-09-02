from functions.additional_functions import *
import decimal
from datetime import date
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from models import H_bill_line, Kellner, H_bill, H_artikel, Kellne1, H_umsatz, Umsatz, H_compli, Queasy

def ts_splitbill_btn_transfer_paytype6bl(rec_id_h_bill:int, curr_select:int, p_artnr:int, balance:decimal, price_decimal:int, transdate:date, dept:int, change_str:str, price:decimal, add_zeit:int, hoga_card:str, cancel_str:str, curr_waiter:int, amount_foreign:decimal, curr_room:str, user_init:str, cc_comment:str, guestnr:int, tischnr:int):
    billart = 0
    qty = 0
    description = ""
    amount = 0
    bill_date = None
    fl_code = 0
    t_h_bill_line_list = []
    h_bill_line = kellner = h_bill = h_artikel = kellne1 = h_umsatz = umsatz = h_compli = queasy = None

    t_h_bill_line = kellner1 = h_bline = h_art = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    Kellner1 = Kellner
    H_bline = H_bill_line
    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, amount, bill_date, fl_code, t_h_bill_line_list, h_bill_line, kellner, h_bill, h_artikel, kellne1, h_umsatz, umsatz, h_compli, queasy
        nonlocal kellner1, h_bline, h_art


        nonlocal t_h_bill_line, kellner1, h_bline, h_art
        nonlocal t_h_bill_line_list
        return {"billart": billart, "qty": qty, "description": description, "amount": amount, "bill_date": bill_date, "fl_code": fl_code, "t-h-bill-line": t_h_bill_line_list}

    def adjust_mealcoupon_umsatz(curr_select:int):

        nonlocal billart, qty, description, amount, bill_date, fl_code, t_h_bill_line_list, h_bill_line, kellner, h_bill, h_artikel, kellne1, h_umsatz, umsatz, h_compli, queasy
        nonlocal kellner1, h_bline, h_art


        nonlocal t_h_bill_line, kellner1, h_bline, h_art
        nonlocal t_h_bill_line_list

        h_mwst:decimal = 0
        h_service:decimal = 0
        epreis:decimal = 0
        amount:decimal = 0
        H_bline = H_bill_line
        H_art = H_artikel

        kellner1 = db_session.query(Kellner1).filter(
                (Kellner1.kellner_nr == h_bill.kellner_nr) &  (Kellner1.departement == h_bill.departement)).first()

        kellne1 = db_session.query(Kellne1).filter(
                (Kellne1.kellner_nr == h_bill.kellner_nr) &  (Kellne1.departement == h_bill.departement)).first()

        h_bline_obj_list = []
        for h_bline, h_art in db_session.query(H_bline, H_art).join(H_art,(H_art.artnr == H_bline.artnr) &  (H_art.departement == H_bline.departement) &  (H_art.artart == 0)).filter(
                (H_bline.rechnr == h_bill.rechnr) &  (h_bill_line.waehrungsnr == curr_select)).all():
            if h_bline._recid in h_bline_obj_list:
                continue
            else:
                h_bline_obj_list.append(h_bline._recid)

            h_umsatz = db_session.query(H_umsatz).filter(
                    (H_umsatz.artnr == h_art.artnr) &  (H_umsatz.departement == h_art.departement) &  (H_umsatz.datum == h_bline.bill_datum)).first()
            h_umsatz.betrag = h_umsatz.betrag - h_bline.betrag
            h_umsatz.anzahl = h_umsatz.anzahl - h_bline.anzahl

            h_umsatz = db_session.query(H_umsatz).first()

            umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.artnr == h_art.artnrfront) &  (Umsatz.departement == h_art.departement) &  (Umsatz.datum == h_bline.bill_datum)).first()
            umsatz.betrag = umsatz.betrag - h_bline.betrag
            umsatz.anzahl = umsatz.anzahl - h_bline.anzahl

            umsatz = db_session.query(Umsatz).first()

            umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.artnr == kellner1.kumsatz_nr) &  (Umsatz.departement == h_bline.departement) &  (Umsatz.datum == h_bline.bill_datum)).first()
            umsatz.betrag = umsatz.betrag - h_bline.betrag
            umsatz.anzahl = umsatz.anzahl - h_bline.anzahl

            umsatz = db_session.query(Umsatz).first()
            h_compli = H_compli()
            db_session.add(h_compli)

            h_compli.datum = h_bline.bill_datum
            h_compli.departement = h_bline.departement
            h_compli.rechnr = h_bline.rechnr
            h_compli.artnr = h_bline.artnr
            h_compli.anzahl = h_bline.anzahl
            h_compli.epreis = h_bline.epreis
            h_compli.p_artnr = p_artnr

    def del_queasy():

        nonlocal billart, qty, description, amount, bill_date, fl_code, t_h_bill_line_list, h_bill_line, kellner, h_bill, h_artikel, kellne1, h_umsatz, umsatz, h_compli, queasy
        nonlocal kellner1, h_bline, h_art


        nonlocal t_h_bill_line, kellner1, h_bline, h_art
        nonlocal t_h_bill_line_list

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 >= 0) &  (Queasy.deci2 >= 0)).all():
            db_session.delete(queasy)

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id_h_bill)).first()
    adjust_mealcoupon_umsatz(curr_select)

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.departement == h_bill.departement) &  (H_artikel.artnr == p_artnr)).first()
    billart = h_artikel.artnr
    qty = 1
    description = h_artikel.bezeich
    amount = - balance
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
            (H_bill_line.departement == dept)).all():
        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_list.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid

    return generate_output()