#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_order, Gl_acct, Bediener, L_artikel, L_orderhdr, L_liefumsatz, L_ophdr, L_bestand, L_pprice, Htparam, L_kredit, Ap_journal

op_list_list, Op_list = create_model_like(L_op, {"rec_id":int})
t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":string, "jahrgang":int, "alkoholgrad":Decimal, "curr_disc":int, "curr_disc2":int, "curr_vat":int})

def po_issue_btn_stop_webbl(user_init:string, l_orderhdr_recid:int, f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, lief_nr:int, billdate:date, docu_nr:string, lscheinnr:string, curr_lager:int, t_amount:Decimal, jobnr:int, curr_disc:int, crterm:int, op_list_list:[Op_list], t_l_order_list:[T_l_order]):

    prepare_cache ([L_op, L_order, Bediener, L_artikel, L_orderhdr, L_liefumsatz, L_ophdr, L_bestand, L_pprice, Htparam, L_kredit, Ap_journal])

    fl_code = 0
    gl_notfound:bool = False
    l_op = l_order = gl_acct = bediener = l_artikel = l_orderhdr = l_liefumsatz = l_ophdr = l_bestand = l_pprice = htparam = l_kredit = ap_journal = None

    op_list = t_l_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, gl_notfound, l_op, l_order, gl_acct, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, l_kredit, ap_journal
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, curr_lager, t_amount, jobnr, curr_disc, crterm


        nonlocal op_list, t_l_order

        return {"fl_code": fl_code}

    def create_l_op():

        nonlocal fl_code, gl_notfound, l_op, l_order, gl_acct, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, l_kredit, ap_journal
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, curr_lager, t_amount, jobnr, curr_disc, crterm


        nonlocal op_list, t_l_order

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        l_order1 = None
        curr_pos:int = 0
        L_order1 =  create_buffer("L_order1",L_order)
        pass
        l_order.geliefert =  to_decimal(l_order.geliefert) + to_decimal(op_list.anzahl)
        l_order.lief_fax[1] = bediener.username
        l_order.rechnungspreis =  to_decimal(t_l_order.rechnungspreis)
        l_order.rechnungswert =  to_decimal(l_order.rechnungswert) + to_decimal(t_l_order.rechnungswert)
        l_order.lieferdatum_eff = t_l_order.lieferdatum_eff
        l_order.stornogrund = op_list.stornogrund


        pass

        l_order1 = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)]})

        if l_order1:
            l_order1.rechnungspreis =  to_decimal(l_order1.rechnungspreis) + to_decimal(op_list.einzelpreis)
            l_order1.rechnungswert =  to_decimal(l_order1.rechnungswert) + to_decimal(op_list.einzelpreis)


            pass

        if l_artikel.ek_aktuell != op_list.einzelpreis:
            pass
            l_artikel.ek_letzter =  to_decimal(l_artikel.ek_aktuell)
            l_artikel.ek_aktuell =  to_decimal(op_list.einzelpreis)
            pass

        l_liefumsatz = get_cache (L_liefumsatz, {"lief_nr": [(eq, op_list.lief_nr)],"datum": [(eq, billdate)]})

        if not l_liefumsatz:
            l_liefumsatz = L_liefumsatz()
            db_session.add(l_liefumsatz)

            l_liefumsatz.datum = billdate
            l_liefumsatz.lief_nr = lief_nr


        l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) + to_decimal(op_list.einzelpreis)
        l_op = L_op()
        db_session.add(l_op)

        buffer_copy(op_list, l_op)
        curr_pos = l_op_pos()
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr
        l_op.flag = True


        pass
        create_purchase_book()
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = op_list.datum
        l_op.lager_nr = op_list.lager_nr
        l_op.artnr = op_list.artnr
        l_op.lief_nr = op_list.lief_nr
        l_op.zeit = get_current_time_in_seconds()
        l_op.anzahl =  to_decimal(op_list.anzahl)
        l_op.einzelpreis =  to_decimal(op_list.einzelpreis)
        l_op.warenwert =  to_decimal(op_list.warenwert)
        l_op.op_art = 3
        l_op.herkunftflag = 2
        l_op.docu_nr = op_list.docu_nr
        l_op.lscheinnr = op_list.lscheinnr
        l_op.pos = curr_pos
        l_op.fuellflag = bediener.nr
        l_op.flag = True
        l_op.stornogrund = op_list.stornogrund


        pass

        l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, op_list.lscheinnr)],"op_typ": [(eq, "sti")]})

        if not l_ophdr:
            l_ophdr = L_ophdr()
            db_session.add(l_ophdr)

            l_ophdr.datum = op_list.datum
            l_ophdr.lager_nr = op_list.lager_nr
            l_ophdr.docu_nr = op_list.docu_nr
            l_ophdr.lscheinnr = op_list.lscheinnr
            l_ophdr.op_typ = "STI"


            pass

        l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, op_list.lscheinnr)],"op_typ": [(eq, "stt")]})

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


            pass

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate):

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, op_list.lager_nr)],"artnr": [(eq, l_artikel.artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = op_list.lager_nr
                l_bestand.artnr = l_artikel.artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(op_list.anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(op_list.warenwert)
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(op_list.anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(op_list.warenwert)


            pass

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_artikel.artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = 0
                l_bestand.artnr = l_artikel.artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(op_list.anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(op_list.warenwert)
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(op_list.anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(op_list.warenwert)


            pass


    def l_op_pos():

        nonlocal fl_code, gl_notfound, l_op, l_order, gl_acct, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, l_kredit, ap_journal
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, curr_lager, t_amount, jobnr, curr_disc, crterm


        nonlocal op_list, t_l_order

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)
        pos = 1

        return generate_inner_output()


    def create_purchase_book():

        nonlocal fl_code, gl_notfound, l_op, l_order, gl_acct, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, l_kredit, ap_journal
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, curr_lager, t_amount, jobnr, curr_disc, crterm


        nonlocal op_list, t_l_order

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
                l_price1.docu_nr = l_op.docu_nr
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

            l_pprice.docu_nr = l_op.docu_nr
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


    def create_ap():

        nonlocal fl_code, gl_notfound, l_op, l_order, gl_acct, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, l_kredit, ap_journal
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, curr_lager, t_amount, jobnr, curr_disc, crterm


        nonlocal op_list, t_l_order

        ap_license:bool = False
        ap_acct:string = ""
        do_it:bool = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 986)]})
        ap_acct = htparam.fchar

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, ap_acct)]})

        if not gl_acct:
            do_it = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1016)]})
        ap_license = htparam.flogical

        if ap_license and do_it:
            l_kredit = L_kredit()
            db_session.add(l_kredit)

            l_kredit.name = docu_nr
            l_kredit.lief_nr = lief_nr
            l_kredit.lscheinnr = lscheinnr
            l_kredit.rgdatum = billdate
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

        nonlocal fl_code, gl_notfound, l_op, l_order, gl_acct, bediener, l_artikel, l_orderhdr, l_liefumsatz, l_ophdr, l_bestand, l_pprice, htparam, l_kredit, ap_journal
        nonlocal user_init, l_orderhdr_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lief_nr, billdate, docu_nr, lscheinnr, curr_lager, t_amount, jobnr, curr_disc, crterm


        nonlocal op_list, t_l_order

        l_od = None
        closed:bool = True
        L_od =  create_buffer("L_od",L_order)

        l_od_obj_list = {}
        l_od = L_order()
        l_artikel = L_artikel()
        for l_od.geliefert, l_od.rechnungswert, l_od.lief_fax, l_od.rechnungspreis, l_od.lieferdatum_eff, l_od.stornogrund, l_od._recid, l_od.anzahl, l_od.loeschflag, l_od.lieferdatum, l_artikel.ek_aktuell, l_artikel.endkum, l_artikel.artnr, l_artikel.lieferfrist, l_artikel.ek_letzter, l_artikel.lief_einheit, l_artikel._recid in db_session.query(L_od.geliefert, L_od.rechnungswert, L_od.lief_fax, L_od.rechnungspreis, L_od.lieferdatum_eff, L_od.stornogrund, L_od._recid, L_od.anzahl, L_od.loeschflag, L_od.lieferdatum, L_artikel.ek_aktuell, L_artikel.endkum, L_artikel.artnr, L_artikel.lieferfrist, L_artikel.ek_letzter, L_artikel.lief_einheit, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_od.artnr)).filter(
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
        l_od.loeschflag = 1
        l_od.lieferdatum_eff = billdate
        l_od.lief_fax[2] = bediener.username
        pass

        for l_od in db_session.query(L_od).filter(
                 (L_od.docu_nr == (docu_nr).lower()) & (L_od.pos > 0) & (L_od.loeschflag == 0)).order_by(L_od._recid).all():
            l_od.loeschflag = 1
            l_od.lieferdatum = billdate
            pass
        fl_code = 1

    for op_list in query(op_list_list, filters=(lambda op_list: op_list.stornogrund.lower()  != "" and op_list.stornogrund.lower()  != ("00000000").lower()  and op_list.stornogrund.lower()  != None)):

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, op_list.stornogrund)]})

        if not gl_acct:
            gl_notfound = True
            break

    if gl_notfound:
        fl_code = 2

        return generate_output()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    for op_list in query(op_list_list):

        t_l_order = query(t_l_order_list, filters=(lambda t_l_order: t_l_order.rec_id == op_list.rec_id), first=True)

        if t_l_order:

            l_order = get_cache (L_order, {"_recid": [(eq, t_l_order.rec_id)]})

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, t_l_order.artnr)]})

            l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, l_orderhdr_recid)]})
            create_l_op()

    if lief_nr != 0:
        create_ap()
    close_po()

    return generate_output()