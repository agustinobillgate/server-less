from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_order, Bediener, L_orderhdr, L_artikel, L_bestand, L_liefumsatz, L_op, Queasy, L_ophdr, L_pprice, Htparam

def po_stockin_mi_all1_1bl(user_init:str, l_order_recid:int, l_orderhdr_recid:int, docu_nr:str, exchg_rate:decimal, price_decimal:int, billdate:date, f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, curr_lager:int, lief_nr:int, lscheinnr:str, t_amount:decimal):
    created = False
    s_list_list = []
    t_l_order_list = []
    s_artnr:int = 0
    qty:decimal = 0
    s_qty:int = 0
    price:decimal = 0
    curr_disc:int = 0
    curr_vat:int = 0
    curr_disc2:int = 0
    curr_vat1:int = 0
    epreis:decimal = 0
    amount:decimal = 0
    l_order = bediener = l_orderhdr = l_artikel = l_bestand = l_liefumsatz = l_op = queasy = l_ophdr = l_pprice = htparam = None

    t_l_order = s_list = l_od = l_order1 = l_op1 = l_price1 = None

    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int, "art_bezeich":str, "jahrgang":int, "alkoholgrad":decimal, "lief_einheit":decimal})
    s_list_list, S_list = create_model("S_list", {"artnr":int, "qty":decimal, "s_qty":decimal, "wert":decimal, "op_recid":int, "ss_artnr":[int, 3], "ss_in":[int, 3], "ss_out":[int, 3]})

    L_od = L_order
    L_order1 = L_order
    L_op1 = L_op
    L_price1 = L_pprice

    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, s_list_list, t_l_order_list, s_artnr, qty, s_qty, price, curr_disc, curr_vat, curr_disc2, curr_vat1, epreis, amount, l_order, bediener, l_orderhdr, l_artikel, l_bestand, l_liefumsatz, l_op, queasy, l_ophdr, l_pprice, htparam
        nonlocal l_od, l_order1, l_op1, l_price1


        nonlocal t_l_order, s_list, l_od, l_order1, l_op1, l_price1
        nonlocal t_l_order_list, s_list_list
        return {"created": created, "s-list": s_list_list, "t-l-order": t_l_order_list}

    def create_l_op(wert:decimal, disp_flag:bool):

        nonlocal created, s_list_list, t_l_order_list, s_artnr, qty, s_qty, price, curr_disc, curr_vat, curr_disc2, curr_vat1, epreis, amount, l_order, bediener, l_orderhdr, l_artikel, l_bestand, l_liefumsatz, l_op, queasy, l_ophdr, l_pprice, htparam
        nonlocal l_od, l_order1, l_op1, l_price1


        nonlocal t_l_order, s_list, l_od, l_order1, l_op1, l_price1
        nonlocal t_l_order_list, s_list_list

        anzahl:decimal = 0
        tot_wert:decimal = 0
        tot_anz:decimal = 0
        curr_pos:int = 0
        orig_preis:decimal = 0
        L_order1 = L_order
        anzahl = qty * l_order.txtnr + s_qty

        if l_order.flag:
            epreis = price / l_order.txt
        else:
            epreis = price

        l_order = db_session.query(L_order).first()
        l_order.geliefert = l_order.geliefert + qty
        l_order.angebot_lief[0] = l_order.angebot_lief[0] + s_qty
        l_order.lief_fax[1] = bediener.username


        while l_order.angebot_lief[0] >= l_order.txtnr:
            l_order.angebot_lief[0] = l_order.angebot_lief[0] - l_order.txtnr
            l_order.geliefert = l_order.geliefert + 1


        l_order.rechnungspreis = price
        l_order.rechnungswert = l_order.rechnungswert + wert
        l_order.lieferdatum_eff = billdate
        l_order.lief_fax[1] = bediener.username
        amount = wert


        t_amount = t_amount + wert

        l_order = db_session.query(L_order).first()

        l_order1 = db_session.query(L_order1).filter(
                    (L_order1.docu_nr == l_orderhdr.docu_nr) &  (L_order1.pos == 0)).first()
        l_order1.rechnungspreis = l_order1.rechnungspreis + wert
        l_order1.rechnungswert = l_order1.rechnungswert + wert

        l_order1 = db_session.query(L_order1).first()

        if l_artikel.ek_aktuell != epreis:

            l_artikel = db_session.query(L_artikel).first()
            l_artikel.ek_letzter = l_artikel.ek_aktuell
            l_artikel.ek_aktuell = epreis

            l_artikel = db_session.query(L_artikel).first()

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate):

            l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.lager_nr == 0) &  (L_bestand.artnr == l_artikel.artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.anf_best_dat = billdate
                l_bestand.artnr = l_artikel.artnr


            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert
            tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang -\
                    l_bestand.anz_ausgang
            tot_wert = l_bestand.val_anf_best + l_bestand.wert_eingang -\
                    l_bestand.wert_ausgang

            l_bestand = db_session.query(L_bestand).first()

            l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.lager_nr == curr_lager) &  (L_bestand.artnr == l_artikel.artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.anf_best_dat = billdate
                l_bestand.artnr = l_artikel.artnr
                l_bestand.lager_nr = curr_lager


            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert

            l_bestand = db_session.query(L_bestand).first()

            l_artikel = db_session.query(L_artikel).first()

            if tot_anz != 0:
                l_artikel.vk_preis = tot_wert / tot_anz

            l_artikel = db_session.query(L_artikel).first()

        l_liefumsatz = db_session.query(L_liefumsatz).filter(
                    (L_liefumsatz.lief_nr == lief_nr) &  (L_liefumsatz.datum == billdate)).first()

        if not l_liefumsatz:
            l_liefumsatz = L_liefumsatz()
            db_session.add(l_liefumsatz)

            l_liefumsatz.datum = billdate
            l_liefumsatz.lief_nr = lief_nr


        l_liefumsatz.gesamtumsatz = l_liefumsatz.gesamtumsatz + wert
        orig_preis = epreis / (1 - curr_disc / 10000) / (1 - curr_disc2 / 10000) /\
                (1 + curr_vat / 10000)

        l_liefumsatz = db_session.query(L_liefumsatz).first()
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = billdate
        l_op.lager_nr = curr_lager
        l_op.artnr = l_artikel.artnr
        l_op.lief_nr = lief_nr
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl = anzahl
        l_op.einzelpreis = epreis
        l_op.warenwert = wert
        l_op.deci1[0] = orig_preis
        l_op.deci1[1] = curr_disc / 100
        l_op.rueckgabegrund = curr_disc2

        if curr_vat != 0:
            l_op.deci1[2] = curr_vat / 100
            l_op.deci1[3] = epreis * l_op.deci1[2] / 100


        else:
            l_op.deci1[2] = curr_vat1 / 100
            l_op.deci1[3] = epreis * l_op.deci1[2] / 100


        l_op.op_art = 1
        l_op.herkunftflag = 1
        l_op.docu_nr = docu_nr
        l_op.lscheinnr = lscheinnr


        curr_pos = l_op_pos()
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr

        l_op = db_session.query(L_op).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.op_recid = l_op._recid
        s_list.artnr = l_op.artnr
        s_list.qty = qty
        s_list.s_qty = s_qty
        s_list.wert = wert

        queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 20) &  (Queasy.number1 == l_op.artnr)).first()

        if queasy:
            s_list.ss_artnr[0] = ss_artnr[0]
            s_list.ss_artnr[1] = ss_artnr[1]
            s_list.ss_artnr[2] = ss_artnr[2]
            s_list.ss_in[0] = ss_in[0]
            s_list.ss_in[1] = ss_in[1]
            s_list.ss_in[2] = ss_in[2]
            s_list.ss_out[0] = ss_out[0]
            s_list.ss_out[1] = ss_out[1]
            s_list.ss_out[2] = ss_out[2]


        create_purchase_book()

        l_ophdr = db_session.query(L_ophdr).filter(
                    (func.lower(L_ophdr.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lager_nr == curr_lager) &  (L_ophdr.datum == billdate)).first()

        if not l_ophdr:
            l_ophdr = L_ophdr()
            db_session.add(l_ophdr)

            l_ophdr.datum = billdate
            l_ophdr.lager_nr = curr_lager
            l_ophdr.docu_nr = docu_nr
            l_ophdr.lscheinnr = lscheinnr
            l_ophdr.op_typ = "STI"

            l_ophdr = db_session.query(L_ophdr).first()


    def l_op_pos():

        nonlocal created, s_list_list, t_l_order_list, s_artnr, qty, s_qty, price, curr_disc, curr_vat, curr_disc2, curr_vat1, epreis, amount, l_order, bediener, l_orderhdr, l_artikel, l_bestand, l_liefumsatz, l_op, queasy, l_ophdr, l_pprice, htparam
        nonlocal l_od, l_order1, l_op1, l_price1


        nonlocal t_l_order, s_list, l_od, l_order1, l_op1, l_price1
        nonlocal t_l_order_list, s_list_list

        pos = 0

        def generate_inner_output():
            return pos
        L_op1 = L_op
        pos = 1


        return generate_inner_output()

    def create_purchase_book():

        nonlocal created, s_list_list, t_l_order_list, s_artnr, qty, s_qty, price, curr_disc, curr_vat, curr_disc2, curr_vat1, epreis, amount, l_order, bediener, l_orderhdr, l_artikel, l_bestand, l_liefumsatz, l_op, queasy, l_ophdr, l_pprice, htparam
        nonlocal l_od, l_order1, l_op1, l_price1


        nonlocal t_l_order, s_list, l_od, l_order1, l_op1, l_price1
        nonlocal t_l_order_list, s_list_list

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
                l_price1.docu_nr = docu_nr
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

            l_pprice.docu_nr = docu_nr
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


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    l_order = db_session.query(L_order).filter(
            (L_order._recid == l_order_recid)).first()

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == l_orderhdr_recid)).first()

    for l_od in db_session.query(L_od).filter(
            (func.lower(L_od.(docu_nr).lower()) == (docu_nr).lower()) &  (L_od.pos > 0) &  (L_od.loeschflag == 0)).all():

        l_artikel = db_session.query(L_artikel).filter(
                (l_artikel.artnr == l_od.artnr)).first()

        l_order = db_session.query(L_order).filter(
                (L_order._recid == l_od._recid)).first()
        s_artnr = l_od.artnr

        if l_od.angebot_lief[0] == 0:
            qty = l_od.anzahl - l_od.geliefert
            s_qty = 0
        else:
            qty = l_od.anzahl - l_od.geliefert - 1
            s_qty = l_od.txtnr - l_od.angebot_lief[0]

        if qty != 0 or s_qty != 0:
            price = l_od.einzelpreis
            curr_disc = to_int(substring(l_od.quality, 0, 2)) * 100 + to_int(substring(l_od.quality, 3, 2))
            curr_vat = to_int(substring(l_od.quality, 6, 2)) * 100 + to_int(substring(l_od.quality, 9, 2))
            curr_disc2 = 0

            if len(l_od.quality) >= 17:
                curr_disc2 = to_int(substring(l_od.quality, 12, 2)) * 100 + to_int(substring(l_od.quality, 15, 2))
            curr_vat1 = l_artikel.alkoholgrad * 100

            if l_od.flag:
                epreis = price / l_od.txt
            else:
                epreis = price
            amount = qty * price + s_qty * epreis
            amount = amount * exchg_rate
            amount = round (amount, price_decimal)
            create_l_op(amount, False)
            created = True

    for l_order in db_session.query(L_order).filter(
            (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.loeschflag == 0)).all():
        t_l_order = T_l_order()
        t_l_order_list.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_order.artnr)).first()
        t_l_order.art_bezeich = l_artikel.bezeich
        t_l_order.jahrgang = l_artikel.jahrgang
        t_l_order.alkoholgrad = l_artikel.alkoholgrad
        t_l_order.lief_einheit = l_artikel.lief_einheit

    return generate_output()