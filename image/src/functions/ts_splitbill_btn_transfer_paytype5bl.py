from functions.additional_functions import *
import decimal
from datetime import date
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from models import H_bill_line, H_bill, H_artikel, Artikel, Kellner, Htparam, Kellne1, H_umsatz, Umsatz, H_journal, H_compli, L_artikel, H_rezept, Gl_acct, Gl_cost, Queasy

def ts_splitbill_btn_transfer_paytype5bl(curr_select:int, rec_id_h_bill:int, p_artnr:int, balance:decimal, price_decimal:int, transdate:date, dept:int, change_str:str, price:decimal, add_zeit:int, hoga_card:str, cancel_str:str, curr_waiter:int, amount_foreign:decimal, curr_room:str, user_init:str, cc_comment:str, guestnr:int, tischnr:int):
    billart = 0
    qty = 0
    description = ""
    amount = 0
    bill_date = None
    fl_code = 0
    t_h_bill_line_list = []
    h_bill_line = h_bill = h_artikel = artikel = kellner = htparam = kellne1 = h_umsatz = umsatz = h_journal = h_compli = l_artikel = h_rezept = gl_acct = gl_cost = queasy = None

    t_h_bill_line = h_bline = h_art = fr_art = kellner1 = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    H_bline = H_bill_line
    H_art = H_artikel
    Fr_art = Artikel
    Kellner1 = Kellner

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, amount, bill_date, fl_code, t_h_bill_line_list, h_bill_line, h_bill, h_artikel, artikel, kellner, htparam, kellne1, h_umsatz, umsatz, h_journal, h_compli, l_artikel, h_rezept, gl_acct, gl_cost, queasy
        nonlocal h_bline, h_art, fr_art, kellner1


        nonlocal t_h_bill_line, h_bline, h_art, fr_art, kellner1
        nonlocal t_h_bill_line_list
        return {"billart": billart, "qty": qty, "description": description, "amount": amount, "bill_date": bill_date, "fl_code": fl_code, "t-h-bill-line": t_h_bill_line_list}

    def adjust_compliment_umsatz(curr_select:int):

        nonlocal billart, qty, description, amount, bill_date, fl_code, t_h_bill_line_list, h_bill_line, h_bill, h_artikel, artikel, kellner, htparam, kellne1, h_umsatz, umsatz, h_journal, h_compli, l_artikel, h_rezept, gl_acct, gl_cost, queasy
        nonlocal h_bline, h_art, fr_art, kellner1


        nonlocal t_h_bill_line, h_bline, h_art, fr_art, kellner1
        nonlocal t_h_bill_line_list

        h_mwst:decimal = 0
        h_service:decimal = 0
        epreis:decimal = 0
        amount:decimal = 0
        f_cost:decimal = 0
        b_cost:decimal = 0
        cost:decimal = 0
        f_eknr:int = 0
        b_eknr:int = 0
        H_bline = H_bill_line
        H_art = H_artikel
        Fr_art = Artikel
        Kellner1 = Kellner

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_eknr = finteger

        kellner1 = db_session.query(Kellner1).filter(
                (Kellner1.kellner_nr == h_bill.kellner_nr) &  (Kellner1.departement == h_bill.departement)).first()

        kellne1 = db_session.query(Kellne1).filter(
                (Kellne1.kellner_nr == h_bill.kellner_nr) &  (Kellne1.departement == h_bill.departement)).first()

        h_bline = db_session.query(H_bline).filter(
                (H_bline.rechnr == h_bill.rechnr) &  (h_bill_line.waehrungsnr == curr_select)).first()
        while None != h_bline:

            h_art = db_session.query(H_art).filter(
                    (H_art.artnr == h_bline.artnr) &  (H_art.departement == h_bline.departement)).first()

            if h_art.artart == 0:
                h_service = 0
                h_mwst = 0
                amount = 0

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

                h_journal = db_session.query(H_journal).filter(
                        (H_journal.bill_datum == h_bline.bill_datum) &  (H_journal.zeit == h_bline.zeit) &  (H_journal.sysdate == h_bline.sysdate) &  (H_journal.artnr == h_bline.artnr) &  (H_journal.departement == h_bline.departement)).first()
                h_journal.betrag = h_bline.betrag

                h_journal = db_session.query(H_journal).first()

                h_bill = db_session.query(H_bill).first()
                h_bill.gesamtumsatz = h_bill.gesamtumsatz - h_bline.betrag

                h_bill = db_session.query(H_bill).first()
            h_compli = H_compli()
            db_session.add(h_compli)

            h_compli.datum = h_bline.bill_datum
            h_compli.departement = h_bline.departement
            h_compli.rechnr = h_bline.rechnr
            h_compli.artnr = h_bline.artnr
            h_compli.anzahl = h_bline.anzahl
            h_compli.epreis = h_bline.epreis
            h_compli.p_artnr = p_artnr
            f_cost = 0
            b_cost = 0

            fr_art = db_session.query(Fr_art).filter(
                    (Fr_art.departement == h_art.departement) &  (Fr_art.artnr == h_art.artnrfront)).first()

            if h_art.artnrlager != 0:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_art.artnrlager)).first()

                if l_artikel:

                    if fr_art.endkum == f_eknr:
                        f_cost = l_artikel.vk_preis * h_bline.anzahl

                    elif fr_art.endkum == b_eknr:
                        b_cost = l_artikel.vk_preis * h_bline.anzahl

            elif h_art.artnrrezept != 0:
                cost = 0

                h_rezept = db_session.query(H_rezept).filter(
                        (H_rezept.artnrrezept == h_art.artnrrezept)).first()

                if h_rezept:
                    cost = cal_cost(h_rezept.artnrrezept, 1, cost)

                    if fr_art.endkum == f_eknr:
                        f_cost = cost * h_bline.anzahl

                    elif fr_art.endkum == b_eknr:
                        b_cost = cost * h_bline.anzahl
            else:

                if fr_art.endkum == f_eknr:
                    f_cost = h_art.prozent * h_bline.anzahl

                elif fr_art.endkum == b_eknr:
                    b_cost = h_art.prozent * h_bline.anzahl

            if f_cost != 0 or b_cost != 0:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 110)).first()
                bill_date = htparam.fdate

                if transdate != None:
                    bill_date = transdate
                else:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 253)).first()

                    if htparam.flogical and bill_date < get_current_date():
                        bill_date = bill_date + 1

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == fr_art.bezeich1)).first()

                if gl_acct:

                    gl_cost = db_session.query(Gl_cost).filter(
                            (Gl_cost.fibukonto == gl_acct.fibukonto) &  (Gl_cost.datum == bill_date)).first()

                    if not gl_cost:
                        gl_cost = Gl_cost()
                        db_session.add(gl_cost)

                        gl_cost.fibukonto = gl_acct.fibukonto
                        gl_cost.datum = bill_date
                    gl_cost.f_betrag = gl_cost.f_betrag - f_cost
                    gl_cost.b_betrag = gl_cost.b_betrag - b_cost
                    gl_cost.betrag = gl_cost.betrag - f_cost - b_cost

                    gl_cost = db_session.query(Gl_cost).first()

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.departement == dept) &  (H_artikel.artnr == p_artnr)).first()

                fr_art = db_session.query(Fr_art).filter(
                        (Fr_art.artnr == h_artikel.artnrfront) &  (Fr_art.departement == 0)).first()

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == fr_art.fibukonto)).first()

                if gl_acct:

                    gl_cost = db_session.query(Gl_cost).filter(
                            (Gl_cost.fibukonto == gl_acct.fibukonto) &  (Gl_cost.datum == bill_date)).first()

                    if not gl_cost:
                        gl_cost = Gl_cost()
                        db_session.add(gl_cost)

                        gl_cost.fibukonto = gl_acct.fibukonto
                        gl_cost.datum = bill_date
                    gl_cost.f_betrag = gl_cost.f_betrag + f_cost
                    gl_cost.b_betrag = gl_cost.b_betrag + b_cost
                    gl_cost.betrag = gl_cost.betrag + f_cost + b_cost

                    gl_cost = db_session.query(Gl_cost).first()

            h_bline = db_session.query(H_bline).filter(
                    (H_bline.rechnr == h_bill.rechnr) &  (h_bill_line.waehrungsnr == curr_select)).first()

    def del_queasy():

        nonlocal billart, qty, description, amount, bill_date, fl_code, t_h_bill_line_list, h_bill_line, h_bill, h_artikel, artikel, kellner, htparam, kellne1, h_umsatz, umsatz, h_journal, h_compli, l_artikel, h_rezept, gl_acct, gl_cost, queasy
        nonlocal h_bline, h_art, fr_art, kellner1


        nonlocal t_h_bill_line, h_bline, h_art, fr_art, kellner1
        nonlocal t_h_bill_line_list

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 >= 0) &  (Queasy.deci2 >= 0)).all():
            db_session.delete(queasy)

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id_h_bill)).first()
    adjust_compliment_umsatz(curr_select)

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