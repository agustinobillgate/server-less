from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, Bediener, L_artikel, L_ophdr, Dml_art, Dml_artdep, L_bestand, L_lieferant, L_liefumsatz, Htparam, Gl_acct, L_kredit, Ap_journal, L_pprice

def dml_stockin_btn_gobl(pvilanguage:int, op_list:[Op_list], curr_dept:int, billdate:date, curr_lager:int, lscheinnr:str, lief_nr:int, f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, user_init:str, t_amount:decimal):
    s_artnr = 0
    qty = 0
    price = 0
    err_code = 0
    msg_str = ""
    curr_pos:int = 0
    created:bool = False
    lvcarea:str = "dml_stockin"
    l_op = bediener = l_artikel = l_ophdr = dml_art = dml_artdep = l_bestand = l_lieferant = l_liefumsatz = htparam = gl_acct = l_kredit = ap_journal = l_pprice = None

    op_list = t_op_list = sys_user = l_art = l_op1 = d_art = d_art1 = l_price1 = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str})
    t_op_list_list, T_op_list = create_model_like(Op_list)

    Sys_user = Bediener
    L_art = L_artikel
    L_op1 = L_op
    D_art = Dml_art
    D_art1 = Dml_artdep
    L_price1 = L_pprice

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_artnr, qty, price, err_code, msg_str, curr_pos, created, lvcarea, l_op, bediener, l_artikel, l_ophdr, dml_art, dml_artdep, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal sys_user, l_art, l_op1, d_art, d_art1, l_price1


        nonlocal op_list, t_op_list, sys_user, l_art, l_op1, d_art, d_art1, l_price1
        nonlocal op_list_list, t_op_list_list
        return {"s_artnr": s_artnr, "qty": qty, "price": price, "err_code": err_code, "msg_str": msg_str}

    def l_op_pos():

        nonlocal s_artnr, qty, price, err_code, msg_str, curr_pos, created, lvcarea, l_op, bediener, l_artikel, l_ophdr, dml_art, dml_artdep, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal sys_user, l_art, l_op1, d_art, d_art1, l_price1


        nonlocal op_list, t_op_list, sys_user, l_art, l_op1, d_art, d_art1, l_price1
        nonlocal op_list_list, t_op_list_list

        pos = 0

        def generate_inner_output():
            return pos
        L_op1 = L_op
        pos = 1


        return generate_inner_output()

    def create_l_op():

        nonlocal s_artnr, qty, price, err_code, msg_str, curr_pos, created, lvcarea, l_op, bediener, l_artikel, l_ophdr, dml_art, dml_artdep, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal sys_user, l_art, l_op1, d_art, d_art1, l_price1


        nonlocal op_list, t_op_list, sys_user, l_art, l_op1, d_art, d_art1, l_price1
        nonlocal op_list_list, t_op_list_list

        anzahl:decimal = 0
        wert:decimal = 0
        tot_anz:decimal = 0
        tot_wert:decimal = 0
        avrg_price:decimal = 0
        D_art = Dml_art
        D_art1 = Dml_artdep
        anzahl = qty
        wert = qty * price
        wert = round(wert, 2)

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
                        (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = curr_lager
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

        l_op.lief_nr = lief_nr
        l_op.datum = billdate
        l_op.lager_nr = curr_lager
        l_op.artnr = s_artnr
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl = anzahl
        l_op.einzelpreis = price
        l_op.warenwert = wert
        l_op.op_art = 1
        l_op.herkunftflag = 1
        l_op.docu_nr = lscheinnr
        l_op.lscheinnr = lscheinnr
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr

        l_op = db_session.query(L_op).first()

        if curr_dept == 0:

            d_art = db_session.query(D_art).filter(
                        (D_art.artnr == s_artnr) &  (D_art.datum == billdate)).first()
            d_art.geliefert = d_art.geliefert + anzahl

            d_art = db_session.query(D_art).first()

        elif curr_dept > 0:

            d_art1 = db_session.query(D_art1).filter(
                        (D_art1.artnr == s_artnr) &  (D_art1.datum == billdate) &  (D_art1.departement == curr_dept)).first()
            d_art1.geliefert = d_art1.geliefert + anzahl

            d_art1 = db_session.query(D_art1).first()
        create_purchase_book(s_artnr, price, anzahl, billdate, lief_nr)

        if (l_artikel.ek_aktuell != price) and price != 0:

            l_artikel = db_session.query(L_artikel).first()
            l_artikel.ek_letzter = l_artikel.ek_aktuell
            l_artikel.ek_aktuell = price

            l_artikel = db_session.query(L_artikel).first()

        return

        msg_str = msg_str + chr(2) + translateExtended ("Incoming record can not be ctreated : ", lvcarea, "") + to_string(s_artnr, "9999999")

    def create_ap():

        nonlocal s_artnr, qty, price, err_code, msg_str, curr_pos, created, lvcarea, l_op, bediener, l_artikel, l_ophdr, dml_art, dml_artdep, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal sys_user, l_art, l_op1, d_art, d_art1, l_price1


        nonlocal op_list, t_op_list, sys_user, l_art, l_op1, d_art, d_art1, l_price1
        nonlocal op_list_list, t_op_list_list

        ap_license:bool = False
        ap_acct:str = ""
        do_it:bool = True
        L_op1 = L_op

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1016)).first()
        ap_license = htparam.flogical

        if not ap_license:

            return

        l_op1 = db_session.query(L_op1).filter(
                (func.lower(L_op1.(lscheinnr).lower()) == (lscheinnr).lower()) &  (L_op1.loeschflag == 0) &  (L_op1.pos >= 1)).first()

        if not l_op1:
            err_code = 1

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

        nonlocal s_artnr, err_code, msg_str, curr_pos, created, lvcarea, l_op, bediener, l_artikel, l_ophdr, dml_art, dml_artdep, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal sys_user, l_art, l_op1, d_art, d_art1, l_price1


        nonlocal op_list, t_op_list, sys_user, l_art, l_op1, d_art, d_art1, l_price1
        nonlocal op_list_list, t_op_list_list

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


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

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
    t_amount = 0

    for op_list in query(op_list_list):
        op_list.docu_nr = lscheinnr
        op_list.lscheinnr = lscheinnr
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty = op_list.anzahl
        price = op_list.warenwert / qty
        t_amount = t_amount + op_list.warenwert
        curr_lager = op_list.lager_nr

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == s_artnr)).first()
        create_l_op()
        created = True

    if lief_nr != 0 and t_amount != 0:
        create_ap()

    for op_list in query(op_list_list):
        l_art = db_session.query(L_art).filter((L_art.artnr == op_list.artnr)).first()
        if not l_art:
            continue

        sys_user = db_session.query(Sys_user).filter((Sys_user.nr == op_list.fuellflag)).first()
        if not sys_user:
            continue

        t_op_list = T_op_list()
        t_op_list_list.append(t_op_list)

        buffer_copy(op_list, t_op_list)
        t_op_list.bezeich = l_artikel.bezeich
        t_op_list.username = bediener.username


    op_list_list.clear()

    for t_op_list in query(t_op_list_list):
        op_list = Op_list()
        op_list_list.append(op_list)

        buffer_copy(t_op_list, op_list)

    return generate_output()