from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.create_lartjob import create_lartjob
from models import L_op, Bediener, L_lieferant, L_ophdr, L_artikel, L_liefumsatz, Htparam, Gl_acct, L_kredit, Ap_journal, L_pprice, L_bestand

def s_stockiss_btn_gobl(op_list:[Op_list], f_endkum:int, b_endkum:int, m_endkum:int, lscheinnr:str, billdate:date, curr_lager:int, jobnr:int, lief_nr:int, fb_closedate:date, m_closedate:date, user_init:str, t_amount:decimal):
    created = False
    s_artnr = 0
    qty = 0
    price = 0
    cost_acct = ""
    err_code = 0
    curr_pos:int = 0
    l_op = bediener = l_lieferant = l_ophdr = l_artikel = l_liefumsatz = htparam = gl_acct = l_kredit = ap_journal = l_pprice = l_bestand = None

    op_list = l_op1 = buf_lieferant = l_art = l_price1 = None

    op_list_list, Op_list = create_model_like(L_op, {"a_bezeich":str})

    L_op1 = L_op
    Buf_lieferant = L_lieferant
    L_art = L_artikel
    L_price1 = L_pprice

    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, s_artnr, qty, price, cost_acct, err_code, curr_pos, l_op, bediener, l_lieferant, l_ophdr, l_artikel, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal l_op1, buf_lieferant, l_art, l_price1


        nonlocal op_list, l_op1, buf_lieferant, l_art, l_price1
        nonlocal op_list_list
        return {"created": created, "s_artnr": s_artnr, "qty": qty, "price": price, "cost_acct": cost_acct, "err_code": err_code}

    def l_op_pos():

        nonlocal created, s_artnr, qty, price, cost_acct, err_code, curr_pos, l_op, bediener, l_lieferant, l_ophdr, l_artikel, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal l_op1, buf_lieferant, l_art, l_price1


        nonlocal op_list, l_op1, buf_lieferant, l_art, l_price1
        nonlocal op_list_list

        pos = 0

        def generate_inner_output():
            return pos
        L_op1 = L_op
        pos = 1


        return generate_inner_output()

    def create_l_op():

        nonlocal created, s_artnr, qty, price, cost_acct, err_code, curr_pos, l_op, bediener, l_lieferant, l_ophdr, l_artikel, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal l_op1, buf_lieferant, l_art, l_price1


        nonlocal op_list, l_op1, buf_lieferant, l_art, l_price1
        nonlocal op_list_list

        anzahl:decimal = 0
        wert:decimal = 0
        tot_anz:decimal = 0
        tot_wert:decimal = 0
        avrg_price:decimal = 0
        Buf_lieferant = L_lieferant

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == s_artnr)).first()
        anzahl = qty
        wert = qty * price
        wert = round(wert, 2)

        buf_lieferant = db_session.query(Buf_lieferant).filter(
                (Buf_lieferant.lief_nr == lief_nr)).first()

        if buf_lieferant:

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
        create_purchase_book(s_artnr, price, qty, billdate, lief_nr)

        if (l_artikel.ek_aktuell != price) and price != 0:

            l_artikel = db_session.query(L_artikel).first()
            l_artikel.ek_letzter = l_artikel.ek_aktuell
            l_artikel.ek_aktuell = price

            l_artikel = db_session.query(L_artikel).first()

    def create_ap():

        nonlocal created, s_artnr, qty, price, cost_acct, err_code, curr_pos, l_op, bediener, l_lieferant, l_ophdr, l_artikel, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal l_op1, buf_lieferant, l_art, l_price1


        nonlocal op_list, l_op1, buf_lieferant, l_art, l_price1
        nonlocal op_list_list

        ap_license:bool = False
        ap_acct:str = ""
        do_it:bool = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1016)).first()
        ap_license = htparam.flogical

        if not ap_license:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 986)).first()
        ap_acct = htparam.fchar

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (ap_acct).lower())).first()

        if not gl_acct:
            do_it = False

        if not do_it:

            return
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
        l_kredit.bediener_nr = bediener.nr


        ap_journal = Ap_journal()
        db_session.add(ap_journal)

        ap_journal.lief_nr = lief_nr
        ap_journal.docu_nr = lscheinnr
        ap_journal.lscheinnr = lscheinnr
        ap_journal.rgdatum = billdate
        ap_journal.saldo = t_amount
        ap_journal.netto = t_amount
        ap_journal.userinit = bediener.userinit
        ap_journal.zeit = get_current_time_in_seconds()

    def create_purchase_book(s_artnr:int, price:decimal, qty:decimal, datum:date, lief_nr:int):

        nonlocal created, s_artnr, cost_acct, err_code, curr_pos, l_op, bediener, l_lieferant, l_ophdr, l_artikel, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal l_op1, buf_lieferant, l_art, l_price1


        nonlocal op_list, l_op1, buf_lieferant, l_art, l_price1
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

    def create_l_op1(curr_lager:int):

        nonlocal created, s_artnr, qty, price, cost_acct, err_code, curr_pos, l_op, bediener, l_lieferant, l_ophdr, l_artikel, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice, l_bestand
        nonlocal l_op1, buf_lieferant, l_art, l_price1


        nonlocal op_list, l_op1, buf_lieferant, l_art, l_price1
        nonlocal op_list_list

        anzahl:decimal = 0
        wert:decimal = 0
        tot_anz:decimal = 0
        tot_wert:decimal = 0
        avrg_price:decimal = 0
        L_art = L_artikel

        l_art = db_session.query(L_art).filter(
                (L_art.artnr == s_artnr)).first()
        anzahl = qty
        wert = qty * price
        wert = round(wert, 2)


        l_op = L_op()
        db_session.add(l_op)

        l_op.lief_nr = lief_nr
        l_op.datum = billdate
        l_op.lager_nr = curr_lager
        l_op.artnr = s_artnr
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl = anzahl
        l_op.einzelpreis = price
        l_op.warenwert = wert
        l_op.op_art = 3
        l_op.herkunftflag = 2
        l_op.docu_nr = lscheinnr
        l_op.lscheinnr = lscheinnr
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr
        l_op.flag = True
        l_op.stornogrund = cost_acct

        l_op = db_session.query(L_op).first()

        if jobnr != 0:
            get_output(create_lartjob(l_ophdr._recid, s_artnr, anzahl, wert, billdate, True))

        if ((l_art.endkum == f_endkum or l_art.endkum == b_endkum) and billdate <= fb_closedate) or (l_art.endkum >= m_endkum and billdate <= m_closedate):

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
            l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

            l_bestand = db_session.query(L_bestand).first()

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0) &  (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = 0
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert
            l_bestand.anz_ausgang = l_bestand.anz_ausgang + anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang + wert

            l_bestand = db_session.query(L_bestand).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if lief_nr != 0:

        l_lieferant = db_session.query(L_lieferant).filter(
                (L_lieferant.lief_nr == lief_nr)).first()

        if not l_lieferant:

            return generate_output()

    l_op = db_session.query(L_op).filter(
                (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (func.lower(L_op.(lscheinnr).lower()) == (lscheinnr).lower())).first()

    if l_op:
        err_code = 1

        return generate_output()

    l_ophdr = db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr.op_typ) == "STI")).first()

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

    for op_list in query(op_list_list):
        created = True
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty = op_list.anzahl
        price = op_list.warenwert / qty
        cost_acct = op_list.stornogrund


        create_l_op()

    if lief_nr != 0:
        create_ap()

    l_ophdr = db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr.op_typ) == "STT")).first()

    if not l_ophdr:
        l_ophdr = L_ophdr()
        db_session.add(l_ophdr)

        l_ophdr.datum = billdate
        l_ophdr.lager_nr = curr_lager
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "STT"
        l_ophdr.fibukonto = cost_acct
        l_ophdr.betriebsnr = jobnr

        l_ophdr = db_session.query(L_ophdr).first()
    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1

    for op_list in query(op_list_list):
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty = op_list.anzahl
        price = op_list.warenwert / qty
        cost_acct = op_list.stornogrund


        create_l_op1(op_list.lager_nr)

    return generate_output()