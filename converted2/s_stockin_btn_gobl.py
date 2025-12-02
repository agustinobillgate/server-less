#using conversion tools version: 1.0.0.117

# ==============================================
# Rulita, 02-12-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from models import L_op, L_ophdr, L_artikel, L_bestand, L_lieferant, L_liefumsatz, Htparam, Gl_acct, L_kredit, Ap_journal, L_pprice

op_list_data, Op_list = create_model_like(L_op, {"a_bezeich":string})

def s_stockin_btn_gobl(s_artnr:int, qty:Decimal, op_list_data:[Op_list], f_endkum:int, b_endkum:int, m_endkum:int, lief_nr:int, lscheinnr:string, billdate:date, curr_lager:int, fb_closedate:date, m_closedate:date, bediener_nr:int, bediener_userinit:string):

    prepare_cache ([L_op, L_ophdr, L_artikel, L_bestand, L_liefumsatz, Htparam, L_kredit, Ap_journal, L_pprice])

    err_flag = 0
    err_flag2 = 0
    price = to_decimal("0.0")
    created = False
    printer_nr = 0
    curr_pos:int = 0
    t_amount:Decimal = to_decimal("0.0")
    pos:int = 0
    l_op = l_ophdr = l_artikel = l_bestand = l_lieferant = l_liefumsatz = htparam = gl_acct = l_kredit = ap_journal = l_pprice = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, err_flag2, price, created, printer_nr, curr_pos, t_amount, pos, l_op, l_ophdr, l_artikel, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal s_artnr, qty, f_endkum, b_endkum, m_endkum, lief_nr, lscheinnr, billdate, curr_lager, fb_closedate, m_closedate, bediener_nr, bediener_userinit


        nonlocal op_list

        return {"s_artnr": s_artnr, "qty": qty, "err_flag": err_flag, "err_flag2": err_flag2, "price": price, "created": created, "printer_nr": printer_nr}

    def l_op_pos():

        nonlocal err_flag, err_flag2, price, created, printer_nr, curr_pos, t_amount, pos, l_op, l_ophdr, l_artikel, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal s_artnr, qty, f_endkum, b_endkum, m_endkum, lief_nr, lscheinnr, billdate, curr_lager, fb_closedate, m_closedate, bediener_nr, bediener_userinit


        nonlocal op_list

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)
        pos = 1

        return generate_inner_output()


    def create_l_op():

        nonlocal err_flag, err_flag2, price, created, printer_nr, curr_pos, t_amount, pos, l_op, l_ophdr, l_artikel, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal s_artnr, qty, f_endkum, b_endkum, m_endkum, lief_nr, lscheinnr, billdate, curr_lager, fb_closedate, m_closedate, bediener_nr, bediener_userinit


        nonlocal op_list

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        tot_anz:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")

        # l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
        l_artikel = db_session.query(L_artikel).filter(
                 (L_artikel.artnr == s_artnr)).with_for_update().first()
        anzahl =  to_decimal(qty)
        wert =  to_decimal(qty) * to_decimal(price)
        wert =  to_decimal(round (wert , 2) )

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate):

            # l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, s_artnr)]})
            l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) & (L_bestand.artnr == s_artnr)).with_for_update().first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate
            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
            pass
            tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
            tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)

            if tot_anz != 0:
                avrg_price =  to_decimal(tot_wert) / to_decimal(tot_anz)
                # pass
                l_artikel.vk_preis =  to_decimal(avrg_price)
                # pass

            # l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, op_list.lager_nr)],"artnr": [(eq, s_artnr)]})
            l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == op_list.lager_nr) & (L_bestand.artnr == s_artnr)).with_for_update().first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.lager_nr = op_list.lager_nr
                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = billdate


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)


            pass

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

        if l_lieferant:

            # l_liefumsatz = get_cache (L_liefumsatz, {"lief_nr": [(eq, lief_nr)],"datum": [(eq, billdate)]})
            l_liefumsatz = db_session.query(L_liefumsatz).filter(
                (L_liefumsatz.lief_nr == lief_nr) & (L_liefumsatz.datum == billdate)).with_for_update().first()

            if not l_liefumsatz:
                l_liefumsatz = L_liefumsatz()
                db_session.add(l_liefumsatz)

                l_liefumsatz.datum = billdate
                l_liefumsatz.lief_nr = lief_nr
            l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) + to_decimal(wert)
            pass
        l_op = L_op()
        db_session.add(l_op)

        buffer_copy(op_list, l_op)
        l_op.pos = curr_pos
        l_op.lief_nr = lief_nr


        pass
        create_purchase_book(s_artnr, price, anzahl, billdate, lief_nr)

        if (l_artikel.ek_aktuell != price) and price != 0:
            # pass
            l_artikel.ek_letzter =  to_decimal(l_artikel.ek_aktuell)
            l_artikel.ek_aktuell =  to_decimal(price)
            # pass
        
        db_session.refresh(l_artikel, with_for_update=True)

        return
        err_flag2 = 1


    def create_ap():

        nonlocal err_flag, err_flag2, price, created, printer_nr, curr_pos, t_amount, pos, l_op, l_ophdr, l_artikel, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal s_artnr, qty, f_endkum, b_endkum, m_endkum, lief_nr, lscheinnr, billdate, curr_lager, fb_closedate, m_closedate, bediener_nr, bediener_userinit


        nonlocal op_list

        ap_license:bool = False
        ap_acct:string = ""
        do_it:bool = True
        l_op1 = None
        L_op1 =  create_buffer("L_op1",L_op)

        l_op1 = get_cache (L_op, {"lscheinnr": [(eq, lscheinnr)],"loeschflag": [(eq, 0)],"pos": [(ge, 1)]})

        if not l_op1:
            err_flag = 2

            return

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

            l_kredit.name = lscheinnr
            l_kredit.lief_nr = lief_nr
            l_kredit.lscheinnr = lscheinnr
            l_kredit.rgdatum = billdate
            l_kredit.datum = None
            l_kredit.saldo =  to_decimal(t_amount)
            l_kredit.ziel = 30
            l_kredit.netto =  to_decimal(t_amount)
            l_kredit.bediener_nr = bediener_nr
            ap_journal = Ap_journal()
            db_session.add(ap_journal)

            ap_journal.lief_nr = lief_nr
            ap_journal.docu_nr = lscheinnr
            ap_journal.lscheinnr = lscheinnr
            ap_journal.rgdatum = billdate
            ap_journal.saldo =  to_decimal(t_amount)
            ap_journal.netto =  to_decimal(t_amount)
            ap_journal.userinit = bediener_userinit
            ap_journal.zeit = get_current_time_in_seconds()


    def create_purchase_book(s_artnr:int, price:Decimal, qty:Decimal, datum:date, lief_nr:int):

        nonlocal err_flag, err_flag2, printer_nr, curr_pos, t_amount, pos, l_op, l_ophdr, l_artikel, l_bestand, l_lieferant, l_liefumsatz, htparam, gl_acct, l_kredit, ap_journal, l_pprice
        nonlocal f_endkum, b_endkum, m_endkum, lscheinnr, billdate, curr_lager, fb_closedate, m_closedate, bediener_nr, bediener_userinit


        nonlocal op_list

        max_anz:int = 0
        curr_anz:int = 0
        created:bool = False
        i:int = 0
        l_art = None
        l_price1 = None
        L_art =  create_buffer("L_art",L_artikel)
        L_price1 =  create_buffer("L_price1",L_pprice)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 225)]})
        max_anz = htparam.finteger

        if max_anz == 0:
            max_anz = 1

        # l_art = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
        l_art = db_session.query(L_artikel).filter(
                 (L_artikel.artnr == s_artnr)).with_for_update().first()
        curr_anz = l_art.lieferfrist

        if curr_anz >= max_anz:

            # l_price1 = get_cache (L_pprice, {"artnr": [(eq, s_artnr)],"counter": [(eq, 1)]})
            l_price1 = db_session.query(L_pprice).filter(
                     (L_pprice.artnr == s_artnr) & (L_pprice.counter == 1)).with_for_update().first()

            if l_price1:
                l_price1.docu_nr = lscheinnr
                l_price1.artnr = s_artnr
                l_price1.anzahl =  to_decimal(qty)
                l_price1.einzelpreis =  to_decimal(price)
                l_price1.warenwert =  to_decimal(qty) * to_decimal(price)
                l_price1.bestelldatum = datum
                l_price1.lief_nr = lief_nr
                l_price1.counter = 0
                created = True
            for i in range(2,curr_anz + 1) :

                # l_pprice = get_cache (L_pprice, {"artnr": [(eq, s_artnr)],"counter": [(eq, i)]})
                l_pprice = db_session.query(L_pprice).filter(
                         (L_pprice.artnr == s_artnr) & (L_pprice.counter == i)).with_for_update().first()

                if l_pprice:
                    # pass
                    l_pprice.counter = l_pprice.counter - 1
                    # pass

            if created:
                l_price1.counter = curr_anz
                pass

        if not created:
            l_pprice = L_pprice()
            db_session.add(l_pprice)

            l_pprice.docu_nr = lscheinnr
            l_pprice.artnr = s_artnr
            l_pprice.anzahl =  to_decimal(qty)
            l_pprice.einzelpreis =  to_decimal(price)
            l_pprice.warenwert =  to_decimal(qty) * to_decimal(price)
            l_pprice.bestelldatum = datum
            l_pprice.lief_nr = lief_nr
            l_pprice.counter = curr_anz + 1
            pass
            pass
            l_art.lieferfrist = curr_anz + 1
            pass


    l_op = get_cache (L_op, {"op_art": [(eq, 1)],"loeschflag": [(le, 1)],"lscheinnr": [(eq, lscheinnr)]})

    if l_op:
        err_flag = 1

        return generate_output()

    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "sti")],"datum": [(eq, billdate)],"lager_nr": [(eq, curr_lager)]})

    if not l_ophdr:
        l_ophdr = L_ophdr()
        db_session.add(l_ophdr)

        l_ophdr.datum = billdate
        l_ophdr.lager_nr = curr_lager
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "STI"
        pass
    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1
    t_amount =  to_decimal("0")

    for op_list in query(op_list_data):
        op_list.docu_nr = lscheinnr
        op_list.lscheinnr = lscheinnr
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty =  to_decimal(op_list.anzahl)
        price =  to_decimal(op_list.warenwert) / to_decimal(qty)
        t_amount =  to_decimal(t_amount) + to_decimal(op_list.warenwert)


        create_l_op()
        created = True

    if lief_nr != 0 and t_amount != 0:
        create_ap()
    printer_nr = get_output(htpint(220))

    return generate_output()