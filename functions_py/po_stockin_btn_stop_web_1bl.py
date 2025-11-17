#using conversion tools version: 1.0.0.119

# ============================
# Rulita, 17-11-2025 | E86F77
# - New Compile Program
# ============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_order, L_artikel, Bediener, Queasy, L_orderhdr, L_bestand, L_liefumsatz, L_ophdr, Htparam, Gl_acct, L_kredit, Ap_journal, L_pprice

op_list_data, Op_list = create_model_like(L_op, {"rec_id":int, "vat_no":int, "vat_value":Decimal})
t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int, "art_bezeich":string, "jahrgang":int, "alkoholgrad":Decimal, "lief_einheit":Decimal, "curr_disc":int, "curr_disc2":int, "curr_vat":int})

def po_stockin_btn_stop_web_1bl(user_init:string, l_orderhdr_recid:int, f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, lief_nr:int, billdate:date, docu_nr:string, lscheinnr:string, crterm:int, curr_lager:int, t_amount:Decimal, op_list_data:[Op_list], t_l_order_data:[T_l_order]):

    prepare_cache ([L_op, L_order, L_artikel, Bediener, L_orderhdr, L_bestand, L_liefumsatz, L_ophdr, Htparam, L_kredit, Ap_journal, L_pprice])

    fl_code = 0
    tot_wert:Decimal = to_decimal("0.0")
    tot_anz:Decimal = to_decimal("0.0")
    curr_pos:int = 0
    l_op = l_order = l_artikel = bediener = queasy = l_orderhdr = l_bestand = l_liefumsatz = l_ophdr = htparam = gl_acct = l_kredit = ap_journal = l_pprice = None

    op_list = t_l_order = l_art = l_order1 = None

    L_art = create_buffer("L_art",L_artikel)
    L_order1 = create_buffer("L_order1",L_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, tot_wert, tot_anz, curr_pos, l_op, l_order, l_artikel, bediener, queasy, l_orderhdr, l_bestand, l_liefumsatz, l_ophdr, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, crterm, curr_lager, t_amount
        nonlocal l_art, l_order1


        nonlocal op_list, t_l_order, l_art, l_order1

        return {"fl_code": fl_code}

    def create_l_op():

        nonlocal fl_code, tot_wert, tot_anz, curr_pos, l_op, l_order, l_artikel, bediener, queasy, l_orderhdr, l_bestand, l_liefumsatz, l_ophdr, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, crterm, curr_lager, t_amount
        nonlocal l_art, l_order1


        nonlocal op_list, t_l_order, l_art, l_order1

        update_price:Decimal = to_decimal("0.0")

        if l_order:
            pass
            l_order.geliefert =  to_decimal(l_order.geliefert) + to_decimal(op_list.anzahl)
            l_order.rechnungspreis =  to_decimal(t_l_order.rechnungspreis)
            l_order.rechnungswert =  to_decimal(l_order.rechnungswert) + to_decimal(t_l_order.rechnungswert)
            l_order.lieferdatum_eff = t_l_order.lieferdatum_eff
            l_order.lief_fax[1] = bediener.username


            pass
            pass

        l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, l_orderhdr_recid)]})

        if l_orderhdr:

            l_order1 = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)]})

            if l_order1:
                pass
                l_order1.rechnungspreis =  to_decimal(l_order1.rechnungspreis) + to_decimal(op_list.einzelpreis)
                l_order1.rechnungswert =  to_decimal(l_order1.rechnungswert) + to_decimal(op_list.einzelpreis)


                pass
                pass

        if l_art:
            update_price =  to_decimal(op_list.einzelpreis) / to_decimal(l_art.lief_einheit)

            if l_art.ek_aktuell != update_price:
                pass
                l_art.ek_letzter =  to_decimal(l_art.ek_aktuell)
                l_art.ek_aktuell =  to_decimal(update_price)


                pass

            if ((l_art.endkum == f_endkum or l_art.endkum == b_endkum) and billdate <= fb_closedate) or (l_art.endkum >= m_endkum and billdate <= m_closedate):

                l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_art.artnr)]})

                if not l_bestand:
                    l_bestand = L_bestand()
                    db_session.add(l_bestand)

                    l_bestand.anf_best_dat = billdate
                    l_bestand.artnr = l_art.artnr
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(op_list.anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(op_list.warenwert)
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                    tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)


                else:
                    pass
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(op_list.anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(op_list.warenwert)
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                    tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)


                    pass
                    pass

                l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, op_list.lager_nr)],"artnr": [(eq, l_art.artnr)]})

                if not l_bestand:
                    l_bestand = L_bestand()
                    db_session.add(l_bestand)

                    l_bestand.anf_best_dat = billdate
                    l_bestand.artnr = l_art.artnr
                    l_bestand.lager_nr = op_list.lager_nr
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(op_list.anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(op_list.warenwert)


                else:
                    pass
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(op_list.anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(op_list.warenwert)


                    pass
                    pass
                pass

                if tot_anz != 0:
                    l_art.vk_preis =  to_decimal(tot_wert) / to_decimal(tot_anz)
                pass

        l_liefumsatz = get_cache (L_liefumsatz, {"lief_nr": [(eq, op_list.lief_nr)],"datum": [(eq, billdate)]})

        if not l_liefumsatz:
            l_liefumsatz = L_liefumsatz()
            db_session.add(l_liefumsatz)

            l_liefumsatz.datum = billdate
            l_liefumsatz.lief_nr = op_list.lief_nr
            l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) + to_decimal(op_list.warenwert)


        else:
            pass
            l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) + to_decimal(op_list.warenwert)


            pass
            pass
        l_op = L_op()
        db_session.add(l_op)

        buffer_copy(op_list, l_op)
        curr_pos = l_op_pos()
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr

        queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_op.lscheinnr)],"number1": [(eq, l_op.artnr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 304
            queasy.char1 = l_op.lscheinnr
            queasy.number1 = l_op.artnr
            queasy.number2 = op_list.vat_no
            queasy.deci1 =  to_decimal(op_list.vat_value)


            pass
        pass
        create_purchase_book()
        pass
        pass

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

        nonlocal fl_code, tot_wert, tot_anz, curr_pos, l_op, l_order, l_artikel, bediener, queasy, l_orderhdr, l_bestand, l_liefumsatz, l_ophdr, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, crterm, curr_lager, t_amount
        nonlocal l_art, l_order1


        nonlocal op_list, t_l_order, l_art, l_order1

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)
        pos = 1

        return generate_inner_output()


    def create_ap():

        nonlocal fl_code, tot_wert, tot_anz, curr_pos, l_op, l_order, l_artikel, bediener, queasy, l_orderhdr, l_bestand, l_liefumsatz, l_ophdr, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, crterm, curr_lager, t_amount
        nonlocal l_art, l_order1


        nonlocal op_list, t_l_order, l_art, l_order1

        ap_license:bool = False
        ap_acct:string = ""
        do_it:bool = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1016)]})

        if htparam:
            ap_license = htparam.flogical

        if not ap_license:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 986)]})

        if htparam:
            ap_acct = htparam.fchar

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, ap_acct)]})

        if not gl_acct:
            do_it = False

        if do_it:
            l_kredit = L_kredit()
            db_session.add(l_kredit)

            l_kredit.name = docu_nr
            l_kredit.lief_nr = lief_nr
            l_kredit.lscheinnr = lscheinnr
            l_kredit.rgdatum = billdate
            l_kredit.datum = None
            l_kredit.saldo =  to_decimal(t_amount)
            l_kredit.ziel = crterm
            l_kredit.netto =  to_decimal(t_amount)
            l_kredit.bediener_nr = bediener.nr


            ap_journal = Ap_journal()
            db_session.add(ap_journal)

            ap_journal.lief_nr = lief_nr
            ap_journal.docu_nr = docu_nr
            ap_journal.lscheinnr = lscheinnr
            ap_journal.rgdatum = billdate
            ap_journal.saldo =  to_decimal(t_amount)
            ap_journal.netto =  to_decimal(t_amount)
            ap_journal.userinit = bediener.userinit
            ap_journal.zeit = get_current_time_in_seconds()


    def close_po():

        nonlocal fl_code, tot_wert, tot_anz, curr_pos, l_op, l_order, l_artikel, bediener, queasy, l_orderhdr, l_bestand, l_liefumsatz, l_ophdr, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, crterm, curr_lager, t_amount
        nonlocal l_art, l_order1


        nonlocal op_list, t_l_order, l_art, l_order1

        l_od = None
        closed:bool = True
        L_od =  create_buffer("L_od",L_order)

        l_od_obj_list = {}
        l_od = L_order()
        l_artikel = L_artikel()
        for l_od.geliefert, l_od.rechnungswert, l_od.rechnungspreis, l_od.lieferdatum_eff, l_od.lief_fax, l_od._recid, l_artikel.lief_einheit, l_artikel._recid, l_artikel.ek_aktuell, l_artikel.endkum, l_artikel.artnr, l_artikel.lieferfrist, l_artikel.ek_letzter, l_artikel.vk_preis in db_session.query(L_od.geliefert, L_od.rechnungswert, L_od.rechnungspreis, L_od.lieferdatum_eff, L_od.lief_fax, L_od._recid, L_artikel.lief_einheit, L_artikel._recid, L_artikel.ek_aktuell, L_artikel.endkum, L_artikel.artnr, L_artikel.lieferfrist, L_artikel.ek_letzter, L_artikel.vk_preis).join(L_artikel,(L_artikel.artnr == L_od.artnr)).filter(
                 (L_od.docu_nr == (docu_nr).lower()) & (L_od.artnr > 0) & (L_od.pos > 0) & (L_od.loeschflag == 0)).order_by(L_od._recid).yield_per(100):
            if l_od_obj_list.get(l_od._recid):
                continue
            else:
                l_od_obj_list[l_od._recid] = True

            if (l_od.anzahl * l_artikel.lief_einheit) > l_od.geliefert:
                closed = False
                break

        if not closed:

            return

        l_od = get_cache (L_order, {"docu_nr": [(eq, docu_nr)],"pos": [(eq, 0)]})

        if l_od:
            pass
            l_od.loeschflag = 1
            l_od.lieferdatum_eff = billdate
            l_od.lief_fax[2] = bediener.username


            pass
            pass

        for l_od in db_session.query(L_od).filter(
                 (L_od.docu_nr == (docu_nr).lower()) & (L_od.pos > 0) & (L_od.loeschflag == 0)).order_by(L_od._recid).all():
            l_od.loeschflag = 1
            l_od.lieferdatum = billdate


            pass
        fl_code = 1


    def create_purchase_book():

        nonlocal fl_code, tot_wert, tot_anz, curr_pos, l_op, l_order, l_artikel, bediener, queasy, l_orderhdr, l_bestand, l_liefumsatz, l_ophdr, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, crterm, curr_lager, t_amount
        nonlocal l_art, l_order1


        nonlocal op_list, t_l_order, l_art, l_order1

        max_anz:int = 0
        curr_anz:int = 0
        created:bool = False
        curr_disc:int = 0
        i:int = 0
        l_price1 = None
        L_price1 =  create_buffer("L_price1",L_pprice)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 225)]})

        if htparam:
            max_anz = htparam.finteger

        if max_anz == 0:
            max_anz = 1
        curr_anz = l_art.lieferfrist

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
            l_art.lieferfrist = curr_anz + 1
            pass

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    for op_list in query(op_list_data):

        t_l_order = query(t_l_order_data, filters=(lambda t_l_order: t_l_order.rec_id == op_list.rec_id), first=True)

        if t_l_order:

            l_order = get_cache (L_order, {"_recid": [(eq, t_l_order.rec_id)]})

            l_art = get_cache (L_artikel, {"artnr": [(eq, t_l_order.artnr)]})
            create_l_op()

    if lief_nr != 0:
        create_ap()
    close_po()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 331) & ((Queasy.char2 == ("Inv-Cek Reciving").lower()) | (Queasy.char2 == ("Inv-Cek Reorg").lower()) | (Queasy.char2 == ("Inv-Cek Journal").lower()))).order_by(Queasy._recid).all():
        db_session.delete(queasy)

    return generate_output()