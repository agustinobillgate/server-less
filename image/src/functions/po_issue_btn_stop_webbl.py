from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, L_order, Bediener, L_artikel, L_orderhdr, L_liefumsatz, L_ophdr, L_bestand, L_pprice, Htparam, Gl_acct, L_kredit, Ap_journal

def po_issue_btn_stop_webbl(user_init:str, l_orderhdr_recid:int, f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, lief_nr:int, billdate:date, docu_nr:str, lscheinnr:str, curr_lager:int, t_amount:decimal, jobnr:int, curr_disc:int, crterm:int, op_list:[Op_list], t_l_order:[T_l_order]):
    fl_code = 0
    l_op = l_order = bediener = l_artikel = l_orderhdr = l_liefumsatz = l_ophdr = l_bestand = l_pprice = htparam = gl_acct = l_kredit = ap_journal = None

    op_list = t_l_order = l_order1 = l_op1 = l_price1 = l_od = None

    op_list_list, Op_list = create_model_like(L_op, {"rec_id":int})
    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":str, "jahrgang":int, "alkoholgrad":decimal, "curr_disc":int, "curr_disc2":int, "curr_vat":int})

    L_order1 = L_order
    L_op1 = L_op
    L_price1 = L_pprice
    L_od = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, l_op, l_order, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, gl_acct, l_kredit, ap_journal
        nonlocal l_order1, l_op1, l_price1, l_od


        nonlocal op_list, t_l_order, l_order1, l_op1, l_price1, l_od
        nonlocal op_list_list, t_l_order_list
        return {"fl_code": fl_code}

    def create_l_op():

        nonlocal fl_code, l_op, l_order, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, gl_acct, l_kredit, ap_journal
        nonlocal l_order1, l_op1, l_price1, l_od


        nonlocal op_list, t_l_order, l_order1, l_op1, l_price1, l_od
        nonlocal op_list_list, t_l_order_list

        anzahl:decimal = 0
        wert:decimal = 0
        tot_wert:decimal = 0
        tot_anz:decimal = 0
        curr_pos:int = 0
        L_order1 = L_order

        l_order = db_session.query(L_order).first()
        l_order.geliefert = l_order.geliefert + op_list.anzahl
        l_order.lief_fax[1] = bediener.username
        l_order.rechnungspreis = t_l_order.rechnungspreis
        l_order.rechnungswert = l_order.rechnungswert + t_l_order.rechnungswert
        l_order.lieferdatum_eff = t_l_order.lieferdatum_eff
        l_order.stornogrund = op_list.stornogrund

        l_order = db_session.query(L_order).first()

        l_order1 = db_session.query(L_order1).filter(
                (L_order1.docu_nr == l_orderhdr.docu_nr) &  (L_order1.pos == 0)).first()

        if l_order1:
            l_order1.rechnungspreis = l_order1.rechnungspreis + op_list.einzelpreis
            l_order1.rechnungswert = l_order1.rechnungswert + op_list.einzelpreis

            l_order1 = db_session.query(L_order1).first()

        if l_artikel.ek_aktuell != op_list.einzelpreis:

            l_artikel = db_session.query(L_artikel).first()
            l_artikel.ek_letzter = l_artikel.ek_aktuell
            l_artikel.ek_aktuell = op_list.einzelpreis

            l_artikel = db_session.query(L_artikel).first()

        l_liefumsatz = db_session.query(L_liefumsatz).filter(
                (L_liefumsatz.lief_nr == op_list.lief_nr) &  (L_liefumsatz.datum == billdate)).first()

        if not l_liefumsatz:
            l_liefumsatz = L_liefumsatz()
            db_session.add(l_liefumsatz)

            l_liefumsatz.datum = billdate
            l_liefumsatz.lief_nr = lief_nr


        l_liefumsatz.gesamtumsatz = l_liefumsatz.gesamtumsatz + op_list.einzelpreis
        l_op = L_op()
        db_session.add(l_op)

        buffer_copy(op_list, l_op)
        curr_pos = l_op_pos()
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr
        l_op.flag = True

        l_op = db_session.query(L_op).first()
        create_purchase_book()
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = op_list.datum
        l_op.lager_nr = op_list.lager_nr
        l_op.artnr = op_list.artnr
        l_op.lief_nr = op_list.lief_nr
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl = op_list.anzahl
        l_op.einzelpreis = op_list.einzelpreis
        l_op.warenwert = op_list.warenwert
        l_op.op_art = 3
        l_op.herkunftflag = 2
        l_op.docu_nr = op_list.docu_nr
        l_op.lscheinnr = op_list.lscheinnr
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr
        l_op.flag = True
        l_op.stornogrund = op_list.stornogrund

        l_op = db_session.query(L_op).first()

        l_ophdr = db_session.query(L_ophdr).filter(
                (L_ophdr.lscheinnr == op_list.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STI")).first()

        if not l_ophdr:
            l_ophdr = L_ophdr()
            db_session.add(l_ophdr)

            l_ophdr.datum = op_list.datum
            l_ophdr.lager_nr = op_list.lager_nr
            l_ophdr.docu_nr = op_list.docu_nr
            l_ophdr.lscheinnr = op_list.lscheinnr
            l_ophdr.op_typ = "STI"

            l_ophdr = db_session.query(L_ophdr).first()

        l_ophdr = db_session.query(L_ophdr).filter(
                (L_ophdr.lscheinnr == op_list.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT")).first()

        if not l_ophdr:
            l_ophdr = L_ophdr()
            db_session.add(l_ophdr)

            l_ophdr.datum = op_list.datum
            l_ophdr.lager_nr = op_list.lager_nr
            l_ophdr.docu_nr = op_list.docu_nr
            l_ophdr.lscheinnr = op_list.lscheinnr
            l_ophdr.op_typ = "STT"
            l_ophdr.fibukonto = op_list.stornogrund
            l_ophdr.betriebsnr = jobnr

            l_ophdr = db_session.query(L_ophdr).first()

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate):

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == op_list.lager_nr) &  (L_bestand.artnr == l_artikel.artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = op_list.lager_nr
                l_bestand.artnr = l_artikel.artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang = l_bestand.anz_eingang + op_list.anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + op_list.warenwert
            l_bestand.anz_ausgang = l_bestand.anz_ausgang + op_list.anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang + op_list.warenwert

            l_bestand = db_session.query(L_bestand).first()

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0) &  (L_bestand.artnr == l_artikel.artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = 0
                l_bestand.artnr = l_artikel.artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang = l_bestand.anz_eingang + op_list.anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + op_list.warenwert
            l_bestand.anz_ausgang = l_bestand.anz_ausgang + op_list.anzahl
            l_bestand.wert_ausgang = l_bestand.wert_ausgang + op_list.warenwert

            l_bestand = db_session.query(L_bestand).first()

    def l_op_pos():

        nonlocal fl_code, l_op, l_order, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, gl_acct, l_kredit, ap_journal
        nonlocal l_order1, l_op1, l_price1, l_od


        nonlocal op_list, t_l_order, l_order1, l_op1, l_price1, l_od
        nonlocal op_list_list, t_l_order_list

        pos = 0

        def generate_inner_output():
            return pos
        L_op1 = L_op
        pos = 1


        return generate_inner_output()

    def create_purchase_book():

        nonlocal fl_code, l_op, l_order, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, gl_acct, l_kredit, ap_journal
        nonlocal l_order1, l_op1, l_price1, l_od


        nonlocal op_list, t_l_order, l_order1, l_op1, l_price1, l_od
        nonlocal op_list_list, t_l_order_list

        max_anz:int = 0
        curr_anz:int = 0
        created:bool = False
        i:int = 0
        L_price1 = L_pprice

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 225)).first()
        max_anz = finteger

        if max_anz == 0:
            max_anz = 1
        curr_anz = l_artikel.lieferfrist

        if curr_anz >= max_anz:

            l_price1 = db_session.query(L_price1).filter(
                    (L_price1.artnr == l_op.artnr) &  (L_price1.counter == 1)).first()

            if l_price1:
                l_price1.docu_nr = l_op.docu_nr
                l_price1.artnr = l_op.artnr
                l_price1.anzahl = l_op.anzahl
                l_price1.einzelpreis = l_op.einzelpreis
                l_price1.warenwert = l_op.warenwert
                l_price1.bestelldatum = l_op.datum
                l_price1.lief_nr = l_op.lief_nr
                l_price1.counter = 0


                created = True
            for i in range(2,curr_anz + 1) :

                l_pprice = db_session.query(L_pprice).filter(
                        (L_pprice.artnr == l_op.artnr) &  (L_pprice.counter == i)).first()

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

            l_pprice.docu_nr = l_op.docu_nr
            l_pprice.artnr = l_op.artnr
            l_pprice.anzahl = l_op.anzahl
            l_pprice.einzelpreis = l_op.einzelpreis
            l_pprice.warenwert = l_op.warenwert
            l_pprice.bestelldatum = l_op.datum
            l_pprice.lief_nr = l_op.lief_nr
            l_pprice.counter = curr_anz + 1
            l_pprice.betriebsnr = curr_disc

            l_pprice = db_session.query(L_pprice).first()

            l_artikel = db_session.query(L_artikel).first()
            l_artikel.lieferfrist = curr_anz + 1

            l_artikel = db_session.query(L_artikel).first()

    def create_ap():

        nonlocal fl_code, l_op, l_order, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, gl_acct, l_kredit, ap_journal
        nonlocal l_order1, l_op1, l_price1, l_od


        nonlocal op_list, t_l_order, l_order1, l_op1, l_price1, l_od
        nonlocal op_list_list, t_l_order_list

        ap_license:bool = False
        ap_acct:str = ""
        do_it:bool = True

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

            l_kredit.name = docu_nr
            l_kredit.lief_nr = lief_nr
            l_kredit.lscheinnr = lscheinnr
            l_kredit.rgdatum = billdate
            l_kredit.saldo = t_amount
            l_kredit.ziel = crterm
            l_kredit.netto = t_amount
            l_kredit.bediener_nr = bediener.nr


            ap_journal = Ap_journal()
            db_session.add(ap_journal)

            ap_journal.lief_nr = lief_nr
            ap_journal.docu_nr = docu_nr
            ap_journal.lscheinnr = lscheinnr
            ap_journal.rgdatum = billdate
            ap_journal.saldo = t_amount
            ap_journal.netto = t_amount
            ap_journal.userinit = bediener.userinit
            ap_journal.zeit = get_current_time_in_seconds()

    def close_po():

        nonlocal fl_code, l_op, l_order, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, gl_acct, l_kredit, ap_journal
        nonlocal l_order1, l_op1, l_price1, l_od


        nonlocal op_list, t_l_order, l_order1, l_op1, l_price1, l_od
        nonlocal op_list_list, t_l_order_list

        closed:bool = True
        L_od = L_order

        l_od_obj_list = []
        for l_od, l_artikel in db_session.query(L_od, L_artikel).join(L_artikel,(L_artikel.artnr == L_od.artnr)).filter(
                (func.lower(L_od.(docu_nr).lower()) == (docu_nr).lower()) &  (L_od.artnr > 0) &  (L_od.pos > 0) &  (L_od.loeschflag == 0)).all():
            if l_od._recid in l_od_obj_list:
                continue
            else:
                l_od_obj_list.append(l_od._recid)

            if (l_od.anzahl * l_artikel.lief_einheit) > l_od.geliefert:
                closed = False
                break

        if not closed:

            return

        l_od = db_session.query(L_od).filter(
                (func.lower(L_od.(docu_nr).lower()) == (docu_nr).lower()) &  (L_od.pos == 0)).first()
        l_od.loeschflag = 1
        l_od.lieferdatum_eff = billdate
        l_od.lief_fax[2] = bediener.username

        l_od = db_session.query(L_od).first()

        for l_od in db_session.query(L_od).filter(
                (func.lower(L_od.(docu_nr).lower()) == (docu_nr).lower()) &  (L_od.pos > 0) &  (L_od.loeschflag == 0)).all():
            l_od.loeschflag = 1
            l_od.lieferdatum = billdate

        fl_code = 1


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    for op_list in query(op_list_list):

        t_l_order = query(t_l_order_list, filters=(lambda t_l_order :t_l_order.rec_id == op_list.rec_id), first=True)

        if t_l_order:

            l_order = db_session.query(L_order).filter(
                    (L_order._recid == t_L_order.rec_id)).first()

            l_artikel = db_session.query(L_artikel).filter(
                    (l_artikel.artnr == t_l_order.artnr)).first()

            l_orderhdr = db_session.query(L_orderhdr).filter(
                    (L_orderhdr._recid == l_orderhdr_recid)).first()
            create_l_op()

    if lief_nr != 0:
        create_ap()
    close_po()

    return generate_output()