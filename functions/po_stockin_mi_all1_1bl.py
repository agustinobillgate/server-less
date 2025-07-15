#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, Bediener, L_orderhdr, L_artikel, L_bestand, L_liefumsatz, L_op, Queasy, L_ophdr, L_pprice, Htparam

def po_stockin_mi_all1_1bl(user_init:string, l_order_recid:int, l_orderhdr_recid:int, docu_nr:string, exchg_rate:Decimal, price_decimal:int, billdate:date, f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, curr_lager:int, lief_nr:int, lscheinnr:string, t_amount:Decimal):

    prepare_cache ([L_order, Bediener, L_orderhdr, L_artikel, L_bestand, L_liefumsatz, L_op, L_ophdr, L_pprice, Htparam])

    created = False
    s_list_data = []
    t_l_order_data = []
    s_artnr:int = 0
    qty:Decimal = to_decimal("0.0")
    s_qty:int = 0
    price:Decimal = to_decimal("0.0")
    curr_disc:int = 0
    curr_vat:int = 0
    curr_disc2:int = 0
    curr_vat1:int = 0
    epreis:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    l_order = bediener = l_orderhdr = l_artikel = l_bestand = l_liefumsatz = l_op = queasy = l_ophdr = l_pprice = htparam = None

    t_l_order = s_list = l_od = None

    t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int, "art_bezeich":string, "jahrgang":int, "alkoholgrad":Decimal, "lief_einheit":Decimal})
    s_list_data, S_list = create_model("S_list", {"artnr":int, "qty":Decimal, "s_qty":Decimal, "wert":Decimal, "op_recid":int, "ss_artnr":[int,3], "ss_in":[int,3], "ss_out":[int,3]})

    L_od = create_buffer("L_od",L_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, s_list_data, t_l_order_data, s_artnr, qty, s_qty, price, curr_disc, curr_vat, curr_disc2, curr_vat1, epreis, amount, l_order, bediener, l_orderhdr, l_artikel, l_bestand, l_liefumsatz, l_op, queasy, l_ophdr, l_pprice, htparam
        nonlocal user_init, l_order_recid, l_orderhdr_recid, docu_nr, exchg_rate, price_decimal, billdate, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, curr_lager, lief_nr, lscheinnr, t_amount
        nonlocal l_od


        nonlocal t_l_order, s_list, l_od
        nonlocal t_l_order_data, s_list_data

        return {"t_amount": t_amount, "created": created, "s-list": s_list_data, "t-l-order": t_l_order_data}

    def create_l_op(wert:Decimal, disp_flag:bool):

        nonlocal created, s_list_data, t_l_order_data, s_artnr, qty, s_qty, price, curr_disc, curr_vat, curr_disc2, curr_vat1, epreis, amount, l_order, bediener, l_orderhdr, l_artikel, l_bestand, l_liefumsatz, l_op, queasy, l_ophdr, l_pprice, htparam
        nonlocal user_init, l_order_recid, l_orderhdr_recid, docu_nr, exchg_rate, price_decimal, billdate, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, curr_lager, lief_nr, lscheinnr, t_amount
        nonlocal l_od


        nonlocal t_l_order, s_list, l_od
        nonlocal t_l_order_data, s_list_data

        anzahl:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        l_order1 = None
        curr_pos:int = 0
        orig_preis:Decimal = to_decimal("0.0")
        L_order1 =  create_buffer("L_order1",L_order)
        anzahl =  to_decimal(qty) * to_decimal(l_order.txtnr) + to_decimal(s_qty)

        if l_order.flag:
            epreis =  to_decimal(price) / to_decimal(l_order.txt)
        else:
            epreis =  to_decimal(price)
        pass
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
        pass

        l_order1 = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)]})
        l_order1.rechnungspreis =  to_decimal(l_order1.rechnungspreis) + to_decimal(wert)
        l_order1.rechnungswert =  to_decimal(l_order1.rechnungswert) + to_decimal(wert)


        pass

        if l_artikel.ek_aktuell != epreis:
            pass
            l_artikel.ek_letzter =  to_decimal(l_artikel.ek_aktuell)
            l_artikel.ek_aktuell =  to_decimal(epreis)


            pass

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate):

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_artikel.artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.anf_best_dat = billdate
                l_bestand.artnr = l_artikel.artnr


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
            tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) -\
                    l_bestand.anz_ausgang
            tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) -\
                    l_bestand.wert_ausgang


            pass

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, l_artikel.artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.anf_best_dat = billdate
                l_bestand.artnr = l_artikel.artnr
                l_bestand.lager_nr = curr_lager


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)


            pass
            pass

            if tot_anz != 0:
                l_artikel.vk_preis =  to_decimal(tot_wert) / to_decimal(tot_anz)
            pass

        l_liefumsatz = get_cache (L_liefumsatz, {"lief_nr": [(eq, lief_nr)],"datum": [(eq, billdate)]})

        if not l_liefumsatz:
            l_liefumsatz = L_liefumsatz()
            db_session.add(l_liefumsatz)

            l_liefumsatz.datum = billdate
            l_liefumsatz.lief_nr = lief_nr


        l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) + to_decimal(wert)
        orig_preis =  to_decimal(epreis) / to_decimal((1) - to_decimal(curr_disc) / to_decimal(10000)) / to_decimal((1) - to_decimal(curr_disc2) / to_decimal(10000)) /\
                (1 + to_decimal(curr_vat) / to_decimal("10000") )


        pass
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


        pass
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.op_recid = l_op._recid
        s_list.artnr = l_op.artnr
        s_list.qty =  to_decimal(qty)
        s_list.s_qty =  to_decimal(s_qty)
        s_list.wert =  to_decimal(wert)

        queasy = get_cache (Queasy, {"key": [(eq, 20)],"number1": [(eq, l_op.artnr)]})

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

        l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "sti")],"lager_nr": [(eq, curr_lager)],"datum": [(eq, billdate)]})

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

        nonlocal created, s_list_data, t_l_order_data, s_artnr, qty, s_qty, price, curr_disc, curr_vat, curr_disc2, curr_vat1, epreis, amount, l_order, bediener, l_orderhdr, l_artikel, l_bestand, l_liefumsatz, l_op, queasy, l_ophdr, l_pprice, htparam
        nonlocal user_init, l_order_recid, l_orderhdr_recid, docu_nr, exchg_rate, price_decimal, billdate, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, curr_lager, lief_nr, lscheinnr, t_amount
        nonlocal l_od


        nonlocal t_l_order, s_list, l_od
        nonlocal t_l_order_data, s_list_data

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)
        pos = 1

        return generate_inner_output()


    def create_purchase_book():

        nonlocal s_list_data, t_l_order_data, s_artnr, qty, s_qty, price, curr_disc, curr_vat, curr_disc2, curr_vat1, epreis, amount, l_order, bediener, l_orderhdr, l_artikel, l_bestand, l_liefumsatz, l_op, queasy, l_ophdr, l_pprice, htparam
        nonlocal user_init, l_order_recid, l_orderhdr_recid, docu_nr, exchg_rate, price_decimal, billdate, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, curr_lager, lief_nr, lscheinnr, t_amount
        nonlocal l_od


        nonlocal t_l_order, s_list, l_od
        nonlocal t_l_order_data, s_list_data

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

            l_price1 = get_cache (L_pprice, {"artnr": [(eq, l_op.artnr)],"counter": [(eq, 1)]})

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

                l_pprice = get_cache (L_pprice, {"artnr": [(eq, l_op.artnr)],"counter": [(eq, i)]})

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
            pass
            pass
            l_artikel.lieferfrist = curr_anz + 1
            pass

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    l_order = get_cache (L_order, {"_recid": [(eq, l_order_recid)]})

    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, l_orderhdr_recid)]})

    for l_od in db_session.query(L_od).filter(
             (L_od.docu_nr == (docu_nr).lower()) & (L_od.pos > 0) & (L_od.loeschflag == 0)).order_by(L_od._recid).all():

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_od.artnr)]})

        l_order = get_cache (L_order, {"_recid": [(eq, l_od._recid)]})
        s_artnr = l_od.artnr

        if l_od.angebot_lief[0] == 0:
            qty =  to_decimal(l_od.anzahl) - to_decimal(l_od.geliefert)
            s_qty = 0
        else:
            qty =  to_decimal(l_od.anzahl) - to_decimal(l_od.geliefert) - to_decimal("1")
            s_qty = l_od.txtnr - l_od.angebot_lief[0]

        if qty != 0 or s_qty != 0:
            price =  to_decimal(l_od.einzelpreis)
            curr_disc = to_int(substring(l_od.quality, 0, 2)) * 100 + to_int(substring(l_od.quality, 3, 2))
            curr_vat = to_int(substring(l_od.quality, 6, 2)) * 100 + to_int(substring(l_od.quality, 9, 2))
            curr_disc2 = 0

            if length(l_od.quality) >= 17:
                curr_disc2 = to_int(substring(l_od.quality, 12, 2)) * 100 + to_int(substring(l_od.quality, 15, 2))
            curr_vat1 = l_artikel.alkoholgrad * 100

            if l_od.flag:
                epreis =  to_decimal(price) / to_decimal(l_od.txt)
            else:
                epreis =  to_decimal(price)
            amount =  to_decimal(qty) * to_decimal(price) + to_decimal(s_qty) * to_decimal(epreis)
            amount =  to_decimal(amount) * to_decimal(exchg_rate)
            amount =  to_decimal(round (amount , price_decimal))
            create_l_op(amount, False)
            created = True

    for l_order in db_session.query(L_order).filter(
             (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.loeschflag == 0)).order_by(L_order._recid).all():
        t_l_order = T_l_order()
        t_l_order_data.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})
        t_l_order.art_bezeich = l_artikel.bezeich
        t_l_order.jahrgang = l_artikel.jahrgang
        t_l_order.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)
        t_l_order.lief_einheit =  to_decimal(l_artikel.lief_einheit)

    return generate_output()