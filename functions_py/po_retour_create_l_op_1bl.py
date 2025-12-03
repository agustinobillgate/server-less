#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.reorg_monhand_init_onhandbl import reorg_monhand_init_onhandbl
from functions.reorg_monhand_update_eingang_1bl import reorg_monhand_update_eingang_1bl
from functions.reorg_monhand_update_ausgangbl import reorg_monhand_update_ausgangbl
from functions.reorg_monhand_update_averagebl import reorg_monhand_update_averagebl
from models import L_orderhdr, Bediener, Queasy, L_order, L_ophdr, L_artikel, L_op, L_bestand, L_liefumsatz
from sqlalchemy.orm.attributes import flag_modified

def po_retour_create_l_op_1bl(l_order_rec_id:int, s_artnr:int, docu_nr:string, exchg_rate:Decimal, price_decimal:int, lief_nr:int, curr_lager:int, lscheinnr:string, f_endkum:int, b_endkum:int, m_endkum:int, billdate:date, fb_closedate:date, m_closedate:date, reason:string, user_init:string, qty:Decimal, price:Decimal, amount:Decimal, s_qty:int, t_amount:Decimal):

    prepare_cache ([L_orderhdr, Bediener, Queasy, L_order, L_ophdr, L_op, L_bestand, L_liefumsatz])

    epreis = to_decimal("0.0")
    direct_issue = False
    ss_artnr:List[int] = create_empty_list(3,0)
    ss_in:List[int] = create_empty_list(3,0)
    ss_out:List[int] = create_empty_list(3,0)
    ss_content:List[int] = create_empty_list(3,0)
    l_orderhdr = bediener = queasy = l_order = l_ophdr = l_artikel = l_op = l_bestand = l_liefumsatz = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal epreis, direct_issue, ss_artnr, ss_in, ss_out, ss_content, l_orderhdr, bediener, queasy, l_order, l_ophdr, l_artikel, l_op, l_bestand, l_liefumsatz
        nonlocal l_order_rec_id, s_artnr, docu_nr, exchg_rate, price_decimal, lief_nr, curr_lager, lscheinnr, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, reason, user_init, qty, price, amount, s_qty, t_amount

        return {"t_amount": t_amount, "epreis": epreis, "direct_issue": direct_issue}

    def create_l_op():

        nonlocal epreis, direct_issue, ss_artnr, ss_in, ss_out, ss_content, l_orderhdr, bediener, queasy, l_order, l_ophdr, l_artikel, l_op, l_bestand, l_liefumsatz
        nonlocal l_order_rec_id, s_artnr, docu_nr, exchg_rate, price_decimal, lief_nr, curr_lager, lscheinnr, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, reason, user_init, qty, price, amount, s_qty, t_amount

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        l_order1 = None
        curr_pos:int = 0
        l_oph = None
        l_art = None
        L_order1 =  create_buffer("L_order1",L_order)
        L_oph =  create_buffer("L_oph",L_ophdr)
        L_art =  create_buffer("L_art",L_artikel)

        db_session.refresh(l_order, with_for_update=True)
        
        while s_qty >= l_order.txtnr:
            s_qty = s_qty - l_order.txtnr
            qty =  to_decimal(qty) + to_decimal("1")

        qty =  - to_decimal(qty)
        s_qty = - s_qty

        if s_qty >= l_order.txtnr:
            s_qty = l_order.txtnr
            
        anzahl =  to_decimal(qty) * to_decimal(l_order.txtnr) + to_decimal(s_qty)

        if l_order.flag:
            epreis =  to_decimal(price) / to_decimal(l_order.txtnr)
            wert =  to_decimal(qty) * to_decimal(price) + to_decimal(s_qty) * to_decimal(epreis)
        else:
            epreis =  to_decimal(price)
            wert =  to_decimal(anzahl) * to_decimal(epreis)

        wert =  to_decimal(wert) * to_decimal(exchg_rate)
        wert =  to_decimal(round (wert , price_decimal))
        l_order.geliefert =  to_decimal(l_order.geliefert) + to_decimal(anzahl)
        l_order.rechnungswert =  to_decimal(l_order.rechnungswert) + to_decimal(wert)
        l_order.lief_fax[1] = bediener.username
        amount =  to_decimal(wert)
        t_amount =  to_decimal(t_amount) + to_decimal(wert)
        
        db_session.flush()

        l_order1 = db_session.query(L_order).filter(
                 (L_order.docu_nr == l_orderhdr.docu_nr) & (L_order.pos == 0)).with_for_update().first()
        
        l_order1.rechnungspreis =  to_decimal(l_order1.rechnungspreis) + to_decimal(wert)
        l_order1.rechnungswert =  to_decimal(l_order1.rechnungswert) + to_decimal(wert)
        
        direct_issue = False

        l_art = db_session.query(L_art).filter(
                 (L_art.artnr == s_artnr)).first()

        l_op = db_session.query(L_op).filter(
                 (L_op.artnr == l_art.artnr) & (L_op.op_art == 3) & (L_op.lief_nr == lief_nr) & (L_op.herkunftflag == 2) & (L_op.lager_nr == curr_lager) & (L_op.flag)).first()

        if l_op:
            db_session.refresh(l_op, with_for_update=True)

            direct_issue = True
            l_op.anzahl =  to_decimal(l_op.anzahl) + to_decimal(anzahl)
            l_op.warenwert =  to_decimal(l_op.warenwert) + to_decimal(wert)

            db_session.flush()

        if not direct_issue:

            if ((l_art.endkum == f_endkum or l_art.endkum == b_endkum) and billdate <= fb_closedate) or (l_art.endkum >= m_endkum and billdate <= m_closedate):

                l_bestand =  db_session.query(L_bestand).filter(
                         (L_bestand.lager_nr == 0) & (L_bestand.artnr == l_art.artnr)).with_for_update().first()
                
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
                tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

                l_bestand = db_session.query(L_bestand).filter( 
                         (L_bestand.lager_nr == curr_lager) & (L_bestand.artnr == l_art.artnr)).with_for_update().first()

                if not l_bestand:
                    l_bestand = L_bestand()
                    db_session.add(l_bestand)

                    l_bestand.anf_best_dat = billdate
                    l_bestand.artnr = l_art.artnr
                    l_bestand.lager_nr = curr_lager

                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)

                if tot_anz != 0:
                    db_session.refresh(l_art, with_for_update=True)
                    l_art.vk_preis =  to_decimal(tot_wert) / to_decimal(tot_anz)
                    db_session.flush()

        elif direct_issue:

            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == 0) & (L_bestand.artnr == l_art.artnr)).with_for_update().first()

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
                l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
                l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)

            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == curr_lager) & (L_bestand.artnr == l_art.artnr)).with_for_update().first()

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
                l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
                l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)

        l_liefumsatz = db_session.query(L_liefumsatz).filter(
                 (L_liefumsatz.lief_nr == lief_nr) & (L_liefumsatz.datum == billdate)).with_for_update().first()

        if not l_liefumsatz:
            l_liefumsatz = L_liefumsatz()
            db_session.add(l_liefumsatz)

            l_liefumsatz.datum = billdate
            l_liefumsatz.lief_nr = lief_nr

        l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) + to_decimal(wert)
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = billdate
        l_op.lager_nr = curr_lager
        l_op.artnr = l_art.artnr
        l_op.lief_nr = lief_nr
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl =  to_decimal(anzahl)
        l_op.einzelpreis =  to_decimal(epreis)
        l_op.warenwert =  to_decimal(wert)
        l_op.op_art = 1
        l_op.herkunftflag = 1
        l_op.docu_nr = docu_nr
        l_op.lscheinnr = lscheinnr
        curr_pos = l_op_pos()
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr
        l_op.stornogrund = reason
        
        create_container()

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


    def l_op_pos():

        nonlocal epreis, direct_issue, ss_artnr, ss_in, ss_out, ss_content, l_orderhdr, bediener, queasy, l_order, l_ophdr, l_artikel, l_op, l_bestand, l_liefumsatz
        nonlocal l_order_rec_id, s_artnr, docu_nr, exchg_rate, price_decimal, lief_nr, curr_lager, lscheinnr, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, reason, user_init, qty, price, amount, s_qty, t_amount

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)
        pos = 1

        return generate_inner_output()


    def create_container():

        nonlocal epreis, direct_issue, ss_artnr, ss_in, ss_out, ss_content, l_orderhdr, bediener, queasy, l_order, l_ophdr, l_artikel, l_op, l_bestand, l_liefumsatz
        nonlocal l_order_rec_id, s_artnr, docu_nr, exchg_rate, price_decimal, lief_nr, curr_lager, lscheinnr, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, reason, user_init, qty, price, amount, s_qty, t_amount

        i:int = 0
        curr_pos:int = 0
        do_it:bool = False
        tot_anz:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        l_art = None
        L_art =  create_buffer("L_art",L_artikel)

        queasy = get_cache (Queasy, {"key": [(eq, 20)],"number1": [(eq, l_op.artnr)]})

        if not queasy:

            return
        for i in range(1,3 + 1) :
            do_it = False

            if ss_artnr[i - 1] != 0:

                l_art = db_session.query(L_art).filter(
                         (L_art.artnr == ss_artnr[i - 1])).first()
                do_it = None != l_art and (ss_in[i - 1] - ss_out[i - 1]) != 0

            if do_it:
                anzahl =  - to_decimal((ss_in[i - 1] - ss_out[i - 1]))
                wert =  to_decimal(l_art.ek_aktuell) * to_decimal(anzahl)
                t_amount =  to_decimal(t_amount) + to_decimal(wert)

                if ((l_art.endkum == f_endkum or l_art.endkum == b_endkum) and billdate <= fb_closedate) or (l_art.endkum >= m_endkum and billdate <= m_closedate):

                    l_bestand =  db_session.query(L_bestand).filter(
                             (L_bestand.lager_nr == 0) & (L_bestand.artnr == l_art.artnr)).with_for_update().first()

                    if not l_bestand:
                        l_bestand = L_bestand()
                        db_session.add(l_bestand)

                        l_bestand.anf_best_dat = billdate
                        l_bestand.artnr = l_art.artnr

                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                    tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
                   

                    l_bestand =  db_session.query(L_bestand).filter(
                             (L_bestand.lager_nr == curr_lager) & (L_bestand.artnr == l_art.artnr)).with_for_update().first()

                    if not l_bestand:
                        l_bestand = L_bestand()
                        db_session.add(l_bestand)

                        l_bestand.anf_best_dat = billdate
                        l_bestand.artnr = l_art.artnr
                        l_bestand.lager_nr = curr_lager
                        
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
                    
                    db_session.refresh(l_art, with_for_update=True)

                    if tot_anz != 0:
                        l_art.vk_preis =  to_decimal(tot_wert) / to_decimal(tot_anz)
                        db_session.flush()
                        
                l_op = L_op()
                db_session.add(l_op)

                l_op.datum = billdate
                l_op.lager_nr = curr_lager
                l_op.artnr = l_art.artnr
                l_op.lief_nr = lief_nr
                l_op.zeit = get_current_time_in_seconds()
                l_op.anzahl =  to_decimal(anzahl)
                l_op.einzelpreis =  to_decimal(l_art.ek_aktuell)
                l_op.warenwert =  to_decimal(wert)
                l_op.deci1[0] = l_art.ek_aktuell
                l_op.op_art = 1
                l_op.herkunftflag = 1
                l_op.docu_nr = docu_nr
                l_op.lscheinnr = lscheinnr
                curr_pos = l_op_pos()
                l_op.pos = curr_pos
                l_op.fuellflag = bediener.nr
                
                
                flag_modified(l_op, "deci1")


    def reorg_inv():

        nonlocal epreis, direct_issue, ss_artnr, ss_in, ss_out, ss_content, l_orderhdr, bediener, queasy, l_order, l_ophdr, l_artikel, l_op, l_bestand, l_liefumsatz
        nonlocal l_order_rec_id, s_artnr, docu_nr, exchg_rate, price_decimal, lief_nr, curr_lager, lscheinnr, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, reason, user_init, qty, price, amount, s_qty, t_amount

        inv_type:int = 0
        for inv_type in range(1,3 + 1) :
            get_output(reorg_monhand_init_onhandbl(inv_type))
            get_output(reorg_monhand_update_eingang_1bl(inv_type, user_init))
            get_output(reorg_monhand_update_ausgangbl(inv_type))
            get_output(reorg_monhand_update_averagebl(inv_type))

    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    queasy = get_cache (Queasy, {"key": [(eq, 20)],"number1": [(eq, s_artnr)]})

    if queasy:
        ss_artnr[0] = queasy.deci1
        ss_artnr[1] = queasy.deci2
        ss_artnr[2] = queasy.deci3
        ss_content[0] = to_int(substring(queasy.char3, 0, 3))
        ss_content[1] = to_int(substring(queasy.char3, 4, 3))
        ss_content[2] = to_int(substring(queasy.char3, 8, 3))

        if ss_content[0] != 0:
            ss_in[0] = round(qty / ss_content[0] - 0.6, 0) + 1

        if ss_content[1] != 0:
            ss_in[1] = round(qty / ss_content[1] - 0.6, 0) + 1

        if ss_content[2] != 0:
            ss_in[2] = round(qty / ss_content[2] - 0.6, 0) + 1

        ss_out[0] = ss_in[0]
        ss_out[1] = ss_in[1]
        ss_out[2] = ss_in[2]

    l_order = db_session.query(L_order).filter(
             (L_order._recid == l_order_rec_id)).first()

    create_l_op()
    reorg_inv()

    return generate_output()