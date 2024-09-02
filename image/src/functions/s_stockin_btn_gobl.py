from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpint import htpint
from models import L_op, L_ophdr, L_artikel, L_bestand, L_lieferant, L_liefumsatz, Htparam, Gl_acct, L_kredit, Ap_journal, L_pprice

def s_stockin_btn_gobl(s_artnr:int, qty:decimal, op_list:[Op_list], f_endkum:int, b_endkum:int, m_endkum:int, lief_nr:int, lscheinnr:str, billdate:date, curr_lager:int, fb_closedate:date, m_closedate:date, bediener_nr:int, bediener_userinit:str):
    err_flag = 0
    err_flag2 = 0
    price = 0
    created = False
    printer_nr = 0
    curr_pos:int = 0
    t_amount:decimal = 0
    pos:int = 0
    l_op = l_ophdr = l_artikel = l_bestand = l_lieferant = l_liefumsatz = htparam = gl_acct = l_kredit = ap_journal = l_pprice = None

    op_list = l_op1 = l_art = l_price1 = None

    op_list_list, Op_list = create_model_like(L_op, {"a_bezeich":str})

    L_op1 = L_op
    L_art = L_artikel
    L_price1 = L_pprice

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, err_flag2, price, created, printer_nr, curr_pos, t_amount, pos, l_op, l_ophdr, l_artikel, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal l_op1, l_art, l_price1


        nonlocal op_list, l_op1, l_art, l_price1
        nonlocal op_list_list
        return {"err_flag": err_flag, "err_flag2": err_flag2, "price": price, "created": created, "printer_nr": printer_nr}

    def l_op_pos():

        nonlocal err_flag, err_flag2, price, created, printer_nr, curr_pos, t_amount, pos, l_op, l_ophdr, l_artikel, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal l_op1, l_art, l_price1


        nonlocal op_list, l_op1, l_art, l_price1
        nonlocal op_list_list

        pos = 0

        def generate_inner_output():
            return pos
        L_op1 = L_op
        pos = 1


        return generate_inner_output()

    def create_l_op():

        nonlocal err_flag, err_flag2, price, created, printer_nr, curr_pos, t_amount, pos, l_op, l_ophdr, l_artikel, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal l_op1, l_art, l_price1


        nonlocal op_list, l_op1, l_art, l_price1
        nonlocal op_list_list

        anzahl:decimal = 0
        wert:decimal = 0
        tot_anz:decimal = 0
        tot_wert:decimal = 0
        avrg_price:decimal = 0

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == s_artnr)).first()
        anzahl = qty
        wert = qty * price
        wert = round (wert, 2)

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate):

            l_bestand = db_session.query(L_bestand).filter(
                            (L_bestand.lager_nr == 0) &  (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate
            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert

            l_bestand = db_session.query(L_bestand).first()
            tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
            tot_wert = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang

            if tot_anz != 0:
                avrg_price = tot_wert / tot_anz

                l_artikel = db_session.query(L_artikel).first()
                l_artikel.vk_preis = avrg_price

                l_artikel = db_session.query(L_artikel).first()

            l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.lager_nr == op_list.lager_nr) &  (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = op_list.lager_nr
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert

            l_bestand = db_session.query(L_bestand).first()

        l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == lief_nr)).first()

        if l_lieferant:

            l_liefumsatz = db_session.query(L_liefumsatz).filter(
                        (L_liefumsatz.lief_nr == lief_nr) &  (L_liefumsatz.datum == billdate)).first()

            if not l_liefumsatz:
                l_liefumsatz = L_liefumsatz()
                db_session.add(l_liefumsatz)

                l_liefumsatz.datum = billdate
                l_liefumsatz.lief_nr = lief_nr
            l_liefumsatz.gesamtumsatz = l_liefumsatz.gesamtumsatz + wert

            l_liefumsatz = db_session.query(L_liefumsatz).first()
        l_op = L_op()
        db_session.add(l_op)

        buffer_copy(op_list, l_op)
        l_op.pos = curr_pos
        l_op.lief_nr = lief_nr

        l_op = db_session.query(L_op).first()
        create_purchase_book(s_artnr, price, anzahl, billdate, lief_nr)

        if (l_artikel.ek_aktuell != price) and price != 0:

            l_artikel = db_session.query(L_artikel).first()
            l_artikel.ek_letzter = l_artikel.ek_aktuell
            l_artikel.ek_aktuell = price

            l_artikel = db_session.query(L_artikel).first()

        return

        err_flag2 = 1

    def create_ap():

        nonlocal err_flag, err_flag2, price, created, printer_nr, curr_pos, t_amount, pos, l_op, l_ophdr, l_artikel, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal l_op1, l_art, l_price1


        nonlocal op_list, l_op1, l_art, l_price1
        nonlocal op_list_list

        ap_license:bool = False
        ap_acct:str = ""
        do_it:bool = True
        L_op1 = L_op

        l_op1 = db_session.query(L_op1).filter(
                (func.lower(L_op1.(lscheinnr).lower()) == (lscheinnr).lower()) &  (L_op1.loeschflag == 0) &  (L_op1.pos >= 1)).first()

        if not l_op1:
            err_flag = 2

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 986)).first()
        ap_acct = htparam.fchar

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (ap_acct).lower())).first()

        if not gl_acct:
            do_it = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1016)).first()
        ap_license = htparam.flogical

        if ap_license and do_it:
            l_kredit = L_kredit()
            db_session.add(l_kredit)

            l_kredit.name = lscheinnr
            l_kredit.lief_nr = lief_nr
            l_kredit.lscheinnr = lscheinnr
            l_kredit.rgdatum = billdate
            l_kredit.datum = None
            l_kredit.saldo = t_amount
            l_kredit.ziel = 30
            l_kredit.netto = t_amount
            l_kredit.bediener_nr = bediener_nr
            ap_journal = Ap_journal()
            db_session.add(ap_journal)

            ap_journal.lief_nr = lief_nr
            ap_journal.docu_nr = lscheinnr
            ap_journal.lscheinnr = lscheinnr
            ap_journal.rgdatum = billdate
            ap_journal.saldo = t_amount
            ap_journal.netto = t_amount
            ap_journal.userinit = bediener_userinit
            ap_journal.zeit = get_current_time_in_seconds()

    def create_purchase_book(s_artnr:int, price:decimal, qty:decimal, datum:date, lief_nr:int):

        nonlocal err_flag, err_flag2, created, printer_nr, curr_pos, t_amount, pos, l_op, l_ophdr, l_artikel, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal l_op1, l_art, l_price1


        nonlocal op_list, l_op1, l_art, l_price1
        nonlocal op_list_list

        max_anz:int = 0
        curr_anz:int = 0
        created:bool = False
        i:int = 0
        L_art = L_artikel
        L_price1 = L_pprice

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 225)).first()
        max_anz = htparam.finteger

        if max_anz == 0:
            max_anz = 1

        l_art = db_session.query(L_art).filter(
                (L_art.artnr == s_artnr)).first()
        curr_anz = l_art.lieferfrist

        if curr_anz >= max_anz:

            l_price1 = db_session.query(L_price1).filter(
                    (L_price1.artnr == s_artnr) &  (L_price1.counter == 1)).first()

            if l_price1:
                l_price1.docu_nr = lscheinnr
                l_price1.artnr = s_artnr
                l_price1.anzahl = qty
                l_price1.einzelpreis = price
                l_price1.warenwert = qty * price
                l_price1.bestelldatum = datum
                l_price1.lief_nr = lief_nr
                l_price1.counter = 0
                created = True
            for i in range(2,curr_anz + 1) :

                l_pprice = db_session.query(L_pprice).filter(
                        (L_pprice.artnr == s_artnr) &  (L_pprice.counter == i)).first()

                if l_pprice:

                    l_pprice = db_session.query(L_pprice).first()
                    l_pprice.counter = l_pprice.counter - 1

                    l_pprice = db_session.query(L_pprice).first()

            if created:
                l_price1.counter = curr_anz

                l_price1 = db_session.query(L_price1).first()

        if not created:
            l_pprice = L_pprice()
            db_session.add(l_pprice)

            l_pprice.docu_nr = lscheinnr
            l_pprice.artnr = s_artnr
            l_pprice.anzahl = qty
            l_pprice.einzelpreis = price
            l_pprice.warenwert = qty * price
            l_pprice.bestelldatum = datum
            l_pprice.lief_nr = lief_nr
            l_pprice.counter = curr_anz + 1

            l_pprice = db_session.query(L_pprice).first()

            l_art = db_session.query(L_art).first()
            l_art.lieferfrist = curr_anz + 1

            l_art = db_session.query(L_art).first()

    l_op = db_session.query(L_op).filter(
                (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (func.lower(L_op.(lscheinnr).lower()) == (lscheinnr).lower())).first()

    if l_op:
        err_flag = 1

        return generate_output()

    l_ophdr = db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.datum == billdate) &  (L_ophdr.lager_nr == curr_lager)).first()

    if not l_ophdr:
        l_ophdr = L_ophdr()
        db_session.add(l_ophdr)

        l_ophdr.datum = billdate
        l_ophdr.lager_nr = curr_lager
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "STI"

        l_ophdr = db_session.query(L_ophdr).first()
    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1
    t_amount = 0

    for op_list in query(op_list_list):
        op_list.docu_nr = lscheinnr
        op_list.lscheinnr = lscheinnr
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty = op_list.anzahl
        price = op_list.warenwert / qty
        t_amount = t_amount + op_list.warenwert


        create_l_op()
        created = True

    if lief_nr != 0 and t_amount != 0:
        create_ap()
    printer_nr = get_output(htpint(220))

    return generate_output()