#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from models import H_bill_line, H_bill, H_artikel, Artikel, Kellner, Htparam, Kellne1, H_umsatz, Umsatz, H_journal, H_compli, L_artikel, H_rezept, Gl_acct, Gl_cost, Queasy

def ts_splitbill_btn_transfer_paytype5bl(curr_select:int, rec_id_h_bill:int, p_artnr:int, balance:Decimal, price_decimal:int, transdate:date, dept:int, change_str:string, price:Decimal, add_zeit:int, hoga_card:string, cancel_str:string, curr_waiter:int, amount_foreign:Decimal, curr_room:string, user_init:string, cc_comment:string, guestnr:int, tischnr:int):

    prepare_cache ([H_bill, H_artikel, Htparam, H_umsatz, Umsatz, H_journal, H_compli, L_artikel, H_rezept, Gl_acct, Gl_cost])

    billart = 0
    qty = 0
    description = ""
    amount = to_decimal("0.0")
    bill_date = None
    fl_code = 0
    t_h_bill_line_list = []
    h_bill_line = h_bill = h_artikel = artikel = kellner = htparam = kellne1 = h_umsatz = umsatz = h_journal = h_compli = l_artikel = h_rezept = gl_acct = gl_cost = queasy = None

    t_h_bill_line = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, amount, bill_date, fl_code, t_h_bill_line_list, h_bill_line, h_bill, h_artikel, artikel, kellner, htparam, kellne1, h_umsatz, umsatz, h_journal, h_compli, l_artikel, h_rezept, gl_acct, gl_cost, queasy
        nonlocal curr_select, rec_id_h_bill, p_artnr, balance, price_decimal, transdate, dept, change_str, price, add_zeit, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr, tischnr


        nonlocal t_h_bill_line
        nonlocal t_h_bill_line_list

        return {"billart": billart, "qty": qty, "description": description, "amount": amount, "bill_date": bill_date, "fl_code": fl_code, "t-h-bill-line": t_h_bill_line_list}

    def adjust_compliment_umsatz(curr_select:int):

        nonlocal billart, qty, description, bill_date, fl_code, t_h_bill_line_list, h_bill_line, h_bill, h_artikel, artikel, kellner, htparam, kellne1, h_umsatz, umsatz, h_journal, h_compli, l_artikel, h_rezept, gl_acct, gl_cost, queasy
        nonlocal rec_id_h_bill, p_artnr, balance, price_decimal, transdate, dept, change_str, price, add_zeit, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr, tischnr


        nonlocal t_h_bill_line
        nonlocal t_h_bill_line_list

        h_mwst:Decimal = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        epreis:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        f_cost:Decimal = to_decimal("0.0")
        b_cost:Decimal = to_decimal("0.0")
        cost:Decimal = to_decimal("0.0")
        f_eknr:int = 0
        b_eknr:int = 0
        h_bline = None
        h_art = None
        fr_art = None
        kellner1 = None
        H_bline =  create_buffer("H_bline",H_bill_line)
        H_art =  create_buffer("H_art",H_artikel)
        Fr_art =  create_buffer("Fr_art",Artikel)
        Kellner1 =  create_buffer("Kellner1",Kellner)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_eknr = htparam.finteger

        kellner1 = db_session.query(Kellner1).filter(
                 (Kellner1.kellner_nr == h_bill.kellner_nr) & (Kellner1.departement == h_bill.departement)).first()

        kellne1 = get_cache (Kellne1, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})

        h_bline = db_session.query(H_bline).filter(
                 (H_bline.rechnr == h_bill.rechnr) & (h_bill_line.waehrungsnr == curr_select)).first()
        while None != h_bline:

            h_art = get_cache (H_artikel, {"artnr": [(eq, h_bline.artnr)],"departement": [(eq, h_bline.departement)]})

            if h_art.artart == 0:
                h_service =  to_decimal("0")
                h_mwst =  to_decimal("0")
                amount =  to_decimal("0")

                h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_art.artnr)],"departement": [(eq, h_art.departement)],"datum": [(eq, h_bline.bill_datum)]})
                h_umsatz.betrag =  to_decimal(h_umsatz.betrag) - to_decimal(h_bline.betrag)
                h_umsatz.anzahl = h_umsatz.anzahl - h_bline.anzahl
                pass

                umsatz = get_cache (Umsatz, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, h_art.departement)],"datum": [(eq, h_bline.bill_datum)]})
                umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(h_bline.betrag)
                umsatz.anzahl = umsatz.anzahl - h_bline.anzahl
                pass

                h_journal = get_cache (H_journal, {"bill_datum": [(eq, h_bline.bill_datum)],"zeit": [(eq, h_bline.zeit)],"sysdate": [(eq, h_bline.sysdate)],"artnr": [(eq, h_bline.artnr)],"departement": [(eq, h_bline.departement)]})
                h_journal.betrag =  to_decimal(h_bline.betrag)
                pass
                pass
                h_bill.gesamtumsatz =  to_decimal(h_bill.gesamtumsatz) - to_decimal(h_bline.betrag)
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
            f_cost =  to_decimal("0")
            b_cost =  to_decimal("0")

            fr_art = db_session.query(Fr_art).filter(
                     (Fr_art.departement == h_art.departement) & (Fr_art.artnr == h_art.artnrfront)).first()

            if h_art.artnrlager != 0:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_art.artnrlager)]})

                if l_artikel:

                    if fr_art.endkum == f_eknr:
                        f_cost =  to_decimal(l_artikel.vk_preis) * to_decimal(h_bline.anzahl)

                    elif fr_art.endkum == b_eknr:
                        b_cost =  to_decimal(l_artikel.vk_preis) * to_decimal(h_bline.anzahl)

            elif h_art.artnrrezept != 0:
                cost =  to_decimal("0")

                h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_art.artnrrezept)]})

                if h_rezept:
                    cost = cal_cost(h_rezept.artnrrezept, 1, cost)

                    if fr_art.endkum == f_eknr:
                        f_cost =  to_decimal(cost) * to_decimal(h_bline.anzahl)

                    elif fr_art.endkum == b_eknr:
                        b_cost =  to_decimal(cost) * to_decimal(h_bline.anzahl)
            else:

                if fr_art.endkum == f_eknr:
                    f_cost =  to_decimal(h_art.prozent) * to_decimal(h_bline.anzahl)

                elif fr_art.endkum == b_eknr:
                    b_cost =  to_decimal(h_art.prozent) * to_decimal(h_bline.anzahl)

            if f_cost != 0 or b_cost != 0:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
                bill_date = htparam.fdate

                if transdate != None:
                    bill_date = transdate
                else:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

                    if htparam.flogical and bill_date < get_current_date():
                        bill_date = bill_date + timedelta(days=1)

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fr_art.bezeich1)]})

                if gl_acct:

                    gl_cost = get_cache (Gl_cost, {"fibukonto": [(eq, gl_acct.fibukonto)],"datum": [(eq, bill_date)]})

                    if not gl_cost:
                        gl_cost = Gl_cost()
                        db_session.add(gl_cost)

                        gl_cost.fibukonto = gl_acct.fibukonto
                        gl_cost.datum = bill_date
                    gl_cost.f_betrag =  to_decimal(gl_cost.f_betrag) - to_decimal(f_cost)
                    gl_cost.b_betrag =  to_decimal(gl_cost.b_betrag) - to_decimal(b_cost)
                    gl_cost.betrag =  to_decimal(gl_cost.betrag) - to_decimal(f_cost) - to_decimal(b_cost)
                    pass

                h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, p_artnr)]})

                fr_art = db_session.query(Fr_art).filter(
                         (Fr_art.artnr == h_artikel.artnrfront) & (Fr_art.departement == 0)).first()

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fr_art.fibukonto)]})

                if gl_acct:

                    gl_cost = get_cache (Gl_cost, {"fibukonto": [(eq, gl_acct.fibukonto)],"datum": [(eq, bill_date)]})

                    if not gl_cost:
                        gl_cost = Gl_cost()
                        db_session.add(gl_cost)

                        gl_cost.fibukonto = gl_acct.fibukonto
                        gl_cost.datum = bill_date
                    gl_cost.f_betrag =  to_decimal(gl_cost.f_betrag) + to_decimal(f_cost)
                    gl_cost.b_betrag =  to_decimal(gl_cost.b_betrag) + to_decimal(b_cost)
                    gl_cost.betrag =  to_decimal(gl_cost.betrag) + to_decimal(f_cost) + to_decimal(b_cost)
                    pass

            curr_recid = h_bline._recid
            h_bline = db_session.query(H_bline).filter(
                     (H_bline.rechnr == h_bill.rechnr) & (h_bill_line.waehrungsnr == curr_select) & (H_bline._recid > curr_recid)).first()


    def del_queasy():

        nonlocal billart, qty, description, amount, bill_date, fl_code, t_h_bill_line_list, h_bill_line, h_bill, h_artikel, artikel, kellner, htparam, kellne1, h_umsatz, umsatz, h_journal, h_compli, l_artikel, h_rezept, gl_acct, gl_cost, queasy
        nonlocal curr_select, rec_id_h_bill, p_artnr, balance, price_decimal, transdate, dept, change_str, price, add_zeit, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr, tischnr


        nonlocal t_h_bill_line
        nonlocal t_h_bill_line_list

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 4) & (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) & (Queasy.number2 >= 0) & (Queasy.deci2 >= 0)).order_by(Queasy._recid).all():
            db_session.delete(queasy)
        pass


    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id_h_bill)]})
    adjust_compliment_umsatz(curr_select)

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