#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, Bediener, L_orderhdr, L_artikel, L_liefumsatz, L_op, L_ophdr, L_bestand, L_pprice, Htparam
from sqlalchemy.orm.attributes import flag_modified

def po_issue_create_l_opbl(amount:Decimal, user_init:string, recid_l_order:int, recid_l_orderhdr:int, l_art_artnr:int, price:Decimal, billdate:date, lief_nr:int, docu_nr:string, curr_disc:int, curr_disc2:int, curr_vat:int, curr_vat1:int, curr_lager:int, cost_acct:string, lscheinnr:string, jobnr:int, f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, s_artnr:int, t_amount:Decimal, qty:Decimal, s_qty:int):

    prepare_cache ([Bediener, L_orderhdr, L_artikel, L_liefumsatz, L_op, L_ophdr, L_bestand, L_pprice, Htparam])

    epreis = to_decimal("0.0")
    orig_preis = to_decimal("0.0")
    s_list_data = []
    t_l_order_data = []
    l_order = bediener = l_orderhdr = l_artikel = l_liefumsatz = l_op = l_ophdr = l_bestand = l_pprice = htparam = None

    s_list = t_l_order = None

    s_list_data, S_list = create_model("S_list", {"artnr":int, "qty":Decimal, "s_qty":Decimal, "wert":Decimal, "op_recid1":int, "op_recid2":int})
    t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":string, "jahrgang":int, "alkoholgrad":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal epreis, orig_preis, s_list_data, t_l_order_data, l_order, bediener, l_orderhdr, l_artikel, l_liefumsatz, l_op, l_ophdr, l_bestand, l_pprice, htparam
        nonlocal amount, user_init, recid_l_order, recid_l_orderhdr, l_art_artnr, price, billdate, lief_nr, docu_nr, curr_disc, curr_disc2, curr_vat, curr_vat1, curr_lager, cost_acct, lscheinnr, jobnr, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, s_artnr, t_amount, qty, s_qty


        nonlocal s_list, t_l_order
        nonlocal s_list_data, t_l_order_data

        return {"t_amount": t_amount, "qty": qty, "s_qty": s_qty, "epreis": epreis, "orig_preis": orig_preis, "s-list": s_list_data, "t-l-order": t_l_order_data}

    def create_l_op():

        nonlocal epreis, orig_preis, s_list_data, t_l_order_data, l_order, bediener, l_orderhdr, l_artikel, l_liefumsatz, l_op, l_ophdr, l_bestand, l_pprice, htparam
        nonlocal amount, user_init, recid_l_order, recid_l_orderhdr, l_art_artnr, price, billdate, lief_nr, docu_nr, curr_disc, curr_disc2, curr_vat, curr_vat1, curr_lager, cost_acct, lscheinnr, jobnr, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, s_artnr, t_amount, qty, s_qty


        nonlocal s_list, t_l_order
        nonlocal s_list_data, t_l_order_data

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        l_order1 = None
        curr_pos:int = 0
        L_order1 =  create_buffer("L_order1",L_order)
        
        db_session.refresh(l_order, with_for_update=True)

        while s_qty >= l_order.txtnr:
            s_qty = s_qty - l_order.txtnr
            qty =  to_decimal(qty) + to_decimal("1")

        anzahl =  to_decimal(qty) * to_decimal(l_order.txtnr) + to_decimal(s_qty)

        if l_order.flag:
            epreis =  to_decimal(price) / to_decimal(l_order.txtnr)
        else:
            epreis =  to_decimal(price)

        wert =  to_decimal(amount)
        l_order.geliefert =  to_decimal(l_order.geliefert) + to_decimal(qty)
        l_order.angebot_lief[0] = l_order.angebot_lief[0] + s_qty
        l_order.lief_fax[1] = bediener.username

        while l_order.angebot_lief[0] >= l_order.txtnr:
            l_order.angebot_lief[0] = l_order.angebot_lief[0] - l_order.txtnr
            l_order.geliefert =  to_decimal(l_order.geliefert) + to_decimal("1")

        l_order.rechnungspreis =  to_decimal(price)
        l_order.rechnungswert =  to_decimal(l_order.rechnungswert) + to_decimal(wert)
        l_order.lieferdatum_eff = billdate
        l_order.lief_fax[1] = bediener.username

        amount =  to_decimal(wert)
        t_amount =  to_decimal(t_amount) + to_decimal(wert)

        flag_modified(l_order, "angebot_lief")
        flag_modified(l_order, "lief_fax")

        db_session.flush()

        l_order1 = db_session.query(L_order1).filter(
                 (L_order1.docu_nr == l_orderhdr.docu_nr) & (L_order1.pos == 0)).with_for_update().first()
        l_order1.rechnungspreis =  to_decimal(l_order1.rechnungspreis) + to_decimal(wert)
        l_order1.rechnungswert =  to_decimal(l_order1.rechnungswert) + to_decimal(wert)

        if l_artikel.ek_aktuell != epreis:
            db_session.refresh(l_artikel, with_for_update=True)

            l_artikel.ek_letzter =  to_decimal(l_artikel.ek_aktuell)
            l_artikel.ek_aktuell =  to_decimal(epreis)

            db_session.flush()

        l_liefumsatz = db_session.query(L_liefumsatz).filter(
                 (L_liefumsatz.lief_nr == lief_nr) & (L_liefumsatz.datum == billdate)).with_for_update().first()

        if not l_liefumsatz:
            l_liefumsatz = L_liefumsatz()
            db_session.add(l_liefumsatz)

            l_liefumsatz.datum = billdate
            l_liefumsatz.lief_nr = lief_nr

        l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) + to_decimal(wert)
        orig_preis =  to_decimal(epreis) / to_decimal((1) - to_decimal(curr_disc) / to_decimal(10000)) / to_decimal((1) - to_decimal(curr_disc2) / to_decimal(10000)) / to_decimal((1) + to_decimal(curr_vat) / to_decimal(10000))
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = billdate
        l_op.lager_nr = curr_lager
        l_op.artnr = l_artikel.artnr
        l_op.lief_nr = lief_nr
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl =  to_decimal(anzahl)
        l_op.einzelpreis =  to_decimal(epreis)
        l_op.warenwert =  to_decimal(wert)
        l_op.deci1[0] = orig_preis
        l_op.deci1[1] = curr_disc / 100
        l_op.rueckgabegrund = curr_disc2

        if curr_vat != 0:
            l_op.deci1[2] = curr_vat / 100
            l_op.deci1[3] = price * l_op.deci1[2] / 100
        else:
            l_op.deci1[2] = curr_vat1 / 100
            l_op.deci1[3] = price * l_op.deci1[2] / 100

        l_op.op_art = 1
        l_op.herkunftflag = 2
        l_op.docu_nr = docu_nr
        l_op.lscheinnr = lscheinnr
        curr_pos = l_op_pos()
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr
        l_op.flag = True
        l_op.stornogrund = cost_acct
        flag_modified(l_op, "deci1")

        s_list = S_list()
        s_list_data.append(s_list)

        s_list.op_recid1 = l_op._recid
        s_list.artnr = l_op.artnr
        s_list.qty =  to_decimal(qty)
        s_list.s_qty =  to_decimal(s_qty)
        s_list.wert =  to_decimal(wert)

        create_purchase_book()

        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = billdate
        l_op.lager_nr = curr_lager
        l_op.artnr = l_artikel.artnr
        l_op.lief_nr = lief_nr
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl =  to_decimal(anzahl)
        l_op.einzelpreis =  to_decimal(epreis)
        l_op.warenwert =  to_decimal(wert)
        l_op.op_art = 3
        l_op.herkunftflag = 2
        l_op.docu_nr = docu_nr
        l_op.lscheinnr = lscheinnr
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr
        l_op.flag = True
        l_op.stornogrund = cost_acct
        
        s_list.op_recid2 = l_op._recid

        l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "sti")]})

        if not l_ophdr:
            l_ophdr = L_ophdr()
            db_session.add(l_ophdr)

            l_ophdr.datum = billdate
            l_ophdr.lager_nr = curr_lager
            l_ophdr.docu_nr = docu_nr
            l_ophdr.lscheinnr = lscheinnr
            l_ophdr.op_typ = "STI"
            pass

        l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "stt")]})

        if not l_ophdr:
            l_ophdr = L_ophdr()
            db_session.add(l_ophdr)

            l_ophdr.datum = billdate
            l_ophdr.lager_nr = curr_lager
            l_ophdr.docu_nr = docu_nr
            l_ophdr.lscheinnr = lscheinnr
            l_ophdr.op_typ = "STT"
            l_ophdr.fibukonto = cost_acct
            l_ophdr.betriebsnr = jobnr
            pass

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate):

            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == curr_lager) & (L_bestand.artnr == s_artnr)).with_for_update().first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = curr_lager
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate

            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)

            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == 0) & (L_bestand.artnr == s_artnr)).with_for_update().first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = 0
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate

            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)
            pass


    def l_op_pos():

        nonlocal epreis, orig_preis, s_list_data, t_l_order_data, l_order, bediener, l_orderhdr, l_artikel, l_liefumsatz, l_op, l_ophdr, l_bestand, l_pprice, htparam
        nonlocal amount, user_init, recid_l_order, recid_l_orderhdr, l_art_artnr, price, billdate, lief_nr, docu_nr, curr_disc, curr_disc2, curr_vat, curr_vat1, curr_lager, cost_acct, lscheinnr, jobnr, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, s_artnr, t_amount, qty, s_qty


        nonlocal s_list, t_l_order
        nonlocal s_list_data, t_l_order_data

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)
        pos = 1

        return generate_inner_output()


    def create_purchase_book():

        nonlocal epreis, orig_preis, s_list_data, t_l_order_data, l_order, bediener, l_orderhdr, l_artikel, l_liefumsatz, l_op, l_ophdr, l_bestand, l_pprice, htparam
        nonlocal amount, user_init, recid_l_order, recid_l_orderhdr, l_art_artnr, price, billdate, lief_nr, docu_nr, curr_disc, curr_disc2, curr_vat, curr_vat1, curr_lager, cost_acct, lscheinnr, jobnr, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, s_artnr, t_amount, qty, s_qty


        nonlocal s_list, t_l_order
        nonlocal s_list_data, t_l_order_data

        max_anz:int = 0
        curr_anz:int = 0
        created:bool = False
        i:int = 0
        l_price1 = None
        L_price1 =  create_buffer("L_price1",L_pprice)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 225)]})
        max_anz = htparam.finteger

        if max_anz == 0:
            max_anz = 1
            
        curr_anz = l_artikel.lieferfrist

        if curr_anz >= max_anz:

            l_price1 = db_session.query(L_price1).filter(
                     (L_price1.artnr == l_op.artnr) & (L_price1.counter == 1)).with_for_update().first()

            if l_price1:
                l_price1.docu_nr = docu_nr
                l_price1.artnr = l_op.artnr
                l_price1.anzahl =  to_decimal(l_op.anzahl)
                l_price1.einzelpreis =  to_decimal(l_op.einzelpreis)
                l_price1.warenwert =  to_decimal(l_op.warenwert)
                l_price1.bestelldatum = l_op.datum
                l_price1.lief_nr = l_op.lief_nr
                l_price1.counter = 0
                created = True
            for i in range(2,curr_anz + 1) :

                l_pprice = db_session.query(L_pprice).filter(
                         (L_pprice.artnr == l_op.artnr) & (L_pprice.counter == i)).with_for_update().first()

                if l_pprice:
                    pass
                    l_pprice.counter = l_pprice.counter - 1
                    pass

            if created:
                l_price1.counter = curr_anz
                pass

        if not created:
            l_pprice = L_pprice()
            db_session.add(l_pprice)

            l_pprice.docu_nr = docu_nr
            l_pprice.artnr = l_op.artnr
            l_pprice.anzahl =  to_decimal(l_op.anzahl)
            l_pprice.einzelpreis =  to_decimal(l_op.einzelpreis)
            l_pprice.warenwert =  to_decimal(l_op.warenwert)
            l_pprice.bestelldatum = l_op.datum
            l_pprice.lief_nr = l_op.lief_nr
            l_pprice.counter = curr_anz + 1
            l_pprice.betriebsnr = curr_disc

            db_session.refresh(l_artikel, with_for_update=True)
            l_artikel.lieferfrist = curr_anz + 1
            db_session.flush()

    l_order = db_session.query(L_order).filter(
             (L_order._recid == recid_l_order)).first()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, recid_l_orderhdr)]})

    l_artikel = db_session.query(L_artikel).filter(
             (L_artikel.artnr == l_art_artnr)).first()
    
    create_l_op()

    for l_order in db_session.query(L_order).filter(
             (L_order.pos > 0) & (L_order.loeschflag == 0)).order_by(L_order._recid).all():
        
        t_l_order = T_l_order()
        t_l_order_data.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})
        
        t_l_order.a_bezeich = l_artikel.bezeich
        t_l_order.jahrgang = l_artikel.jahrgang
        t_l_order.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)

    return generate_output()