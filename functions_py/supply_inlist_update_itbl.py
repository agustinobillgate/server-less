#using conversion tools version: 1.0.0.117

# ==============================================
# Rulita, 02-12-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_artikel, Queasy, L_order, Htparam, L_kredit, Ap_journal, Reslin_queasy, Dml_artdep, Dml_art, L_bestand, L_liefumsatz, L_pprice, Bediener

def supply_inlist_update_itbl(pvilanguage:int, cancel_reason:string, str_list_l_recid:int, str_list_billdate:date, str_list_qty:Decimal, bediener_nr:int, bediener_username:string, userinit:string):

    prepare_cache ([L_op, L_artikel, L_order, Htparam, Reslin_queasy, Dml_artdep, Dml_art, L_bestand, L_liefumsatz, Bediener])

    docu_nr = 0
    msg_str = ""
    lvcarea:string = "supply-inlist"
    avrg_price:Decimal = None
    direct_issue:bool = False
    from_date:date = None
    start_date:date = None
    end_date:date = None
    t_amount:Decimal = to_decimal("0.0")
    tot_receiving:Decimal = to_decimal("0.0")
    l_op = l_artikel = queasy = l_order = htparam = l_kredit = ap_journal = reslin_queasy = dml_artdep = dml_art = l_bestand = l_liefumsatz = l_pprice = bediener = None

    blop = None

    Blop = create_buffer("Blop",L_op)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal docu_nr, msg_str, lvcarea, avrg_price, direct_issue, from_date, start_date, end_date, t_amount, tot_receiving, l_op, l_artikel, queasy, l_order, htparam, l_kredit, ap_journal, reslin_queasy, dml_artdep, dml_art, l_bestand, l_liefumsatz, l_pprice, bediener
        nonlocal pvilanguage, cancel_reason, str_list_l_recid, str_list_billdate, str_list_qty, bediener_nr, bediener_username, userinit
        nonlocal blop


        nonlocal blop

        return {"docu_nr": docu_nr, "msg_str": msg_str}

    def update_it():

        nonlocal docu_nr, msg_str, lvcarea, avrg_price, direct_issue, from_date, start_date, end_date, t_amount, tot_receiving, l_op, l_artikel, queasy, l_order, htparam, l_kredit, ap_journal, reslin_queasy, dml_artdep, dml_art, l_bestand, l_liefumsatz, l_pprice, bediener
        nonlocal pvilanguage, cancel_reason, str_list_l_recid, str_list_billdate, str_list_qty, bediener_nr, bediener_username, userinit
        nonlocal blop


        nonlocal blop

        f_endkum:int = 0
        b_endkum:int = 0
        m_endkum:int = 0
        billdate:date = None
        fb_closedate:date = None
        m_closedate:date = None
        tot_anz:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        curr_pos:int = 0
        answer:bool = True
        tot_vat:Decimal = to_decimal("0.0")
        dml_no:int = 0
        dept_no:int = 0
        l_order1 = None
        l_op1 = None
        l_opbuff = None
        L_order1 =  create_buffer("L_order1",L_order)
        L_op1 =  create_buffer("L_op1",L_op)
        L_opbuff =  create_buffer("L_opbuff",L_op)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
        b_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
        m_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
        fb_closedate = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
        m_closedate = htparam.fdate

        # l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, l_op.lief_nr)],"name": [(eq, l_op.docu_nr)],"lscheinnr": [(eq, l_op.lscheinnr)],"opart": [(le, 2)],"zahlkonto": [(eq, 0)]})
        l_kredit = db_session.query(L_kredit).filter(L_kredit.lief_nr == l_op.lief_nr,
                 L_kredit.name == l_op.docu_nr,
                 L_kredit.lscheinnr == l_op.lscheinnr,
                 L_kredit.opart <= 2,
                 L_kredit.zahlkonto == 0).with_for_update().first()

        if not l_kredit:

            l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, l_op.lief_nr)],"lscheinnr": [(eq, l_op.lscheinnr)],"rgdatum": [(eq, l_op.datum)],"opart": [(le, 2)],"zahlkonto": [(eq, 0)]})

        if l_kredit:
            pass
            db_session.delete(l_kredit)
            pass

            # ap_journal = get_cache (Ap_journal, {"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.docu_nr)],"lscheinnr": [(eq, l_op.lscheinnr)]})
            ap_journal = db_session.query(Ap_journal).filter(Ap_journal.lief_nr == l_op.lief_nr,
                     Ap_journal.docu_nr == l_op.docu_nr,
                     Ap_journal.lscheinnr == l_op.lscheinnr).with_for_update().first()

            if ap_journal:
                # pass
                db_session.refresh(ap_journal, with_for_update=True)
                db_session.delete(ap_journal)
                pass

        if (substring(l_op.docu_nr, 0, 1) == ("P").lower()):

            # l_order = get_cache (L_order, {"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.docu_nr)],"artnr": [(eq, l_op.artnr)],"einzelpreis": [(eq, l_op.einzelpreis)]})
            l_order = db_session.query(L_order).filter(L_order.lief_nr == l_op.lief_nr,
                     L_order.docu_nr == l_op.docu_nr,
                     L_order.artnr == l_op.artnr,
                     L_order.einzelpreis == l_op.einzelpreis).with_for_update().first()

            if not l_order:

                # l_order = get_cache (L_order, {"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.docu_nr)],"artnr": [(eq, l_op.artnr)],"einzelpreis": [(eq, l_op.einzelpreis)],"geliefert": [(gt, str_list_qty)]})
                l_order = db_session.query(L_order).filter(L_order.lief_nr == l_op.lief_nr,
                         L_order.docu_nr == l_op.docu_nr,
                         L_order.artnr == l_op.artnr,
                         L_order.einzelpreis == l_op.einzelpreis,
                         L_order.geliefert > str_list_qty).with_for_update().first()

                if not l_order:

                    # l_order = get_cache (L_order, {"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.docu_nr)],"artnr": [(eq, l_op.artnr)]})
                    l_order = db_session.query(L_order).filter(L_order.lief_nr == l_op.lief_nr,
                             L_order.docu_nr == l_op.docu_nr,
                             L_order.artnr == l_op.artnr).with_for_update().first()

            if l_order:
                l_order.geliefert =  to_decimal(l_order.geliefert) - to_decimal(str_list_qty)
                l_order.rechnungswert =  to_decimal(l_order.rechnungswert) - to_decimal(l_op.warenwert)
                pass

                l_order1 = get_cache (L_order, {"docu_nr": [(eq, l_order.docu_nr)],"pos": [(eq, 0)]})
                l_order1.rechnungspreis =  to_decimal(l_order1.rechnungspreis) - to_decimal(l_op.warenwert)
                l_order1.rechnungswert =  to_decimal(l_order1.rechnungswert) - to_decimal(l_op.warenwert)
                pass

        elif substring(l_op.docu_nr, 0, 1) == ("D").lower() :
            dml_no = to_int(substring(l_op.docu_nr, 10, 2))
            dept_no = to_int(substring(l_op.docu_nr, 1, 2))

            if dml_no > 1:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("DML").lower()) & (to_int(entry(0, Reslin_queasy.char1, ";")) == l_op.artnr) & (Reslin_queasy.date1 == l_op.datum) & (to_int(entry(1, Reslin_queasy.char1, ";")) == dept_no) & (Reslin_queasy.number2 == dml_no)).with_for_update().first()

                if reslin_queasy:
                    reslin_queasy.deci3 =  to_decimal(reslin_queasy.deci3) - to_decimal(str_list_qty)


                    pass
                    pass
            else:

                # dml_artdep = get_cache (Dml_artdep, {"artnr": [(eq, l_op.artnr)],"datum": [(eq, l_op.datum)],"departement": [(eq, dept_no)]})
                dml_artdep = db_session.query(Dml_artdep).filter(
                         (Dml_artdep.artnr == l_op.artnr) & (Dml_artdep.datum == l_op.datum) & (Dml_artdep.departement == dept_no)).with_for_update().first()

                if dml_artdep:
                    dml_artdep.geliefert =  to_decimal(dml_artdep.geliefert) - to_decimal(str_list_qty)


                    pass
                    pass
                else:

                    # dml_art = get_cache (Dml_art, {"artnr": [(eq, l_op.artnr)],"datum": [(eq, l_op.datum)]})
                    dml_art = db_session.query(Dml_art).filter(
                             (Dml_art.artnr == l_op.artnr) & (Dml_art.datum == l_op.datum)).with_for_update().first()

                    if dml_art:
                        dml_art.geliefert =  to_decimal(dml_art.geliefert) - to_decimal(str_list_qty)
                        pass
                        pass

        if not direct_issue:

            if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and (str_list_billdate <= fb_closedate)) or ((l_artikel.endkum >= m_endkum) and (str_list_billdate <= m_closedate)):

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, 0)]})

                if l_bestand:
                    tot_anz =  to_decimal(l_bestand.anz_anf_best)
                    tot_wert =  to_decimal(l_bestand.val_anf_best)

                for l_opbuff in db_session.query(L_opbuff).filter(
                         (L_opbuff.artnr == l_op.artnr) & (L_opbuff.op_art == 1) & (L_opbuff.datum <= end_date) & (L_opbuff.loeschflag <= 1)).order_by(L_opbuff._recid).all():
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_opbuff.anzahl)
                    tot_wert =  to_decimal(tot_wert) + to_decimal(l_opbuff.warenwert)

                if tot_anz != 0:
                    avrg_price =  to_decimal(tot_wert) / to_decimal(tot_anz)
                else:

                    if l_bestand and l_bestand.anz_anf_best != 0:
                        avrg_price =  to_decimal(l_bestand.val_anf_best) / to_decimal(l_bestand.anz_anf_best)
                    else:
                        avrg_price =  to_decimal(l_artikel.vk_preis)

                if avrg_price != l_artikel.vk_preis:
                    # pass
                    db_session.refresh(l_artikel, with_for_update=True)
                    l_artikel.vk_preis =  to_decimal(avrg_price)
                    pass

            # l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_artikel.artnr)]})
            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == 0) & (L_bestand.artnr == l_artikel.artnr)).with_for_update().first()

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(str_list_qty)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)


                pass
                pass

            # l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, l_op.lager_nr)],"artnr": [(eq, l_artikel.artnr)]})
            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == l_op.lager_nr) & (L_bestand.artnr == l_artikel.artnr)).with_for_update().first()

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(str_list_qty)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)


                pass
                pass

        elif direct_issue:

            l_op1 = get_cache (L_op, {"lscheinnr": [(eq, l_op.lscheinnr)],"artnr": [(eq, l_op.artnr)],"op_art": [(eq, 3)],"loeschflag": [(ne, 2)],"lief_nr": [(eq, l_op.lief_nr)],"herkunftflag": [(eq, 2)],"lager_nr": [(eq, l_op.lager_nr)]})

            if l_op1:

                # l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_artikel.artnr)]})
                l_bestand = db_session.query(L_bestand).filter(
                         (L_bestand.lager_nr == 0) & (L_bestand.artnr == l_artikel.artnr)).with_for_update().first()

                if l_bestand:
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op1.anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op1.warenwert)
                    l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(l_op1.anzahl)
                    l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(l_op1.warenwert)


                    pass
                    pass

                # l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, l_op1.lager_nr)],"artnr": [(eq, l_artikel.artnr)]})
                l_bestand = db_session.query(L_bestand).filter(
                         (L_bestand.lager_nr == l_op1.lager_nr) & (L_bestand.artnr == l_artikel.artnr)).with_for_update().first()

                if l_bestand:
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op1.anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op1.warenwert)
                    l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(l_op1.anzahl)
                    l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(l_op1.warenwert)


                    pass
                    pass
                pass
            else:

                # l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_artikel.artnr)]})
                l_bestand = db_session.query(L_bestand).filter(
                         (L_bestand.lager_nr == 0) & (L_bestand.artnr == l_artikel.artnr)).with_for_update().first()

                if l_bestand:
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op.anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)


                    pass
                    pass

                # l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, l_op.lager_nr)],"artnr": [(eq, l_artikel.artnr)]})
                l_bestand = db_session.query(L_bestand).filter(
                         (L_bestand.lager_nr == l_op.lager_nr) & (L_bestand.artnr == l_artikel.artnr)).with_for_update().first()

                if l_bestand:
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op.anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)


                    pass
                    pass

            l_op1 = get_cache (L_op, {"artnr": [(eq, l_op.artnr)],"op_art": [(eq, 3)],"lief_nr": [(eq, l_op.lief_nr)],"lscheinnr": [(eq, l_op.lscheinnr)],"herkunftflag": [(eq, 2)],"lager_nr": [(eq, l_op.lager_nr)]})

            if l_op1:
                l_op1.loeschflag = 2
                l_op1.betriebsnr = bediener_nr
                pass

        # l_liefumsatz = get_cache (L_liefumsatz, {"lief_nr": [(eq, l_op.lief_nr)],"datum": [(eq, str_list_billdate)]})
        l_liefumsatz = db_session.query(L_liefumsatz).filter(
                 (L_liefumsatz.lief_nr == l_op.lief_nr) & (L_liefumsatz.datum == str_list_billdate)).with_for_update().first()

        if l_liefumsatz:
            l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) - to_decimal(l_op.warenwert)
        pass
        pass

        l_order = get_cache (L_order, {"docu_nr": [(eq, l_op.docu_nr)],"lief_nr": [(eq, l_op.lief_nr)],"pos": [(eq, 0)],"loeschflag": [(eq, 1)]})

        if l_order:
            docu_nr = recid (l_op)
            msg_str = msg_str + chr_unicode(2) + "&Q" + translateExtended ("Purchase Order closed; re-open it?", lvcarea, "")

        if substring(l_op.docu_nr, 0, 1) == ("D").lower()  or substring(l_op.docu_nr, 0, 1) == ("I").lower() :

            # l_pprice = get_cache (L_pprice, {"artnr": [(eq, l_op.artnr)],"bestelldatum": [(eq, l_op.datum)],"anzahl": [(eq, l_op.anzahl)],"einzelpreis": [(eq, l_op.einzelpreis)],"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.lscheinnr)]})
            l_pprice = db_session.query(L_pprice).filter(L_pprice.artnr == l_op.artnr,
                     L_pprice.bestelldatum == l_op.datum,
                     L_pprice.anzahl == l_op.anzahl,
                     L_pprice.einzelpreis == l_op.einzelpreis,
                     L_pprice.lief_nr == l_op.lief_nr,
                     L_pprice.docu_nr == l_op.lscheinnr).with_for_update().first()

            if l_pprice:
                # pass
                db_session.refresh(l_pprice, with_for_update=True)
                db_session.delete(l_pprice)
                pass

        elif substring(l_op.docu_nr, 0, 1) == ("P").lower() :

            # l_pprice = get_cache (L_pprice, {"artnr": [(eq, l_op.artnr)],"bestelldatum": [(eq, l_op.datum)],"anzahl": [(eq, l_op.anzahl)],"einzelpreis": [(eq, l_op.einzelpreis)],"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.docu_nr)]})
            l_pprice = db_session.query(L_pprice).filter(L_pprice.artnr == l_op.artnr,
                     L_pprice.bestelldatum == l_op.datum,
                     L_pprice.anzahl == l_op.anzahl,
                     L_pprice.einzelpreis == l_op.einzelpreis,
                     L_pprice.lief_nr == l_op.lief_nr,
                     L_pprice.docu_nr == l_op.docu_nr).with_for_update().first

            if l_pprice:
                # pass
                db_session.refresh(l_pprice, with_for_update=True)
                db_session.delete(l_pprice)
                pass

        for blop in db_session.query(Blop).filter(
                 (Blop.lscheinnr == l_op.lscheinnr) & (Blop.lief_nr > 0) & (Blop.loeschflag <= 1) & (Blop.op_art == 1)).order_by(Blop._recid).all():
            tot_vat =  to_decimal("0")

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, blop.lscheinnr)],"number1": [(eq, blop.artnr)]})

            if queasy:
                tot_vat = ( to_decimal(blop.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


            tot_receiving =  to_decimal(tot_receiving) + to_decimal((blop.warenwert) + to_decimal(tot_vat) )

        if tot_receiving != 0:

            bediener = get_cache (Bediener, {"userinit": [(eq, userinit)]})
            l_kredit = L_kredit()
            db_session.add(l_kredit)

            l_kredit.name = l_op.docu_nr
            l_kredit.lief_nr = l_op.lief_nr
            l_kredit.lscheinnr = l_op.lscheinnr
            l_kredit.rgdatum = l_op.datum
            l_kredit.datum = None
            l_kredit.ziel = 30
            l_kredit.saldo =  to_decimal(tot_receiving)
            l_kredit.netto =  to_decimal(tot_receiving)
            l_kredit.bediener_nr = bediener.nr


            ap_journal = Ap_journal()
            db_session.add(ap_journal)

            ap_journal.docu_nr = l_op.docu_nr
            ap_journal.lscheinnr = l_op.lscheinnr
            ap_journal.lief_nr = l_op.lief_nr
            ap_journal.rgdatum = l_op.datum
            ap_journal.zeit = l_op.zeit
            ap_journal.saldo =  to_decimal(tot_receiving)
            ap_journal.netto =  to_decimal(tot_receiving)

            if bediener:
                ap_journal.userinit = userinit
            pass
            pass
        pass
        pass
        pass
        pass


    def reorg_avrg_price(curr_artnr:int, from_date:date):

        nonlocal docu_nr, msg_str, lvcarea, avrg_price, direct_issue, start_date, end_date, t_amount, tot_receiving, l_op, l_artikel, queasy, l_order, htparam, l_kredit, ap_journal, reslin_queasy, dml_artdep, dml_art, l_bestand, l_liefumsatz, l_pprice, bediener
        nonlocal pvilanguage, cancel_reason, str_list_l_recid, str_list_billdate, str_list_qty, bediener_nr, bediener_username, userinit
        nonlocal blop


        nonlocal blop

        t_anz:Decimal = to_decimal("0.0")
        t_wert:Decimal = to_decimal("0.0")
        lbuff = None
        l_opbuff = None
        Lbuff =  create_buffer("Lbuff",L_bestand)
        L_opbuff =  create_buffer("L_opbuff",L_op)

        # l_bestand = get_cache (L_bestand, {"anf_best_dat": [(ge, start_date),(le, end_date)],"artnr": [(eq, curr_artnr)],"lager_nr": [(eq, l_op.lager_nr)]})
        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.anf_best_dat >= start_date) & (L_bestand.anf_best_dat <= end_date) & (L_bestand.artnr == curr_artnr) & (L_bestand.lager_nr == l_op.lager_nr)).with_for_update().first()

        if l_bestand:
            l_bestand.anz_eingang =  to_decimal("0")
            l_bestand.anz_ausgang =  to_decimal("0")
            l_bestand.wert_eingang =  to_decimal("0")
            l_bestand.wert_ausgang =  to_decimal("0")

        lbuff = get_cache (L_bestand, {"anf_best_dat": [(ge, start_date),(le, end_date)],"artnr": [(eq, curr_artnr)],"lager_nr": [(eq, 0)]})

        if lbuff:
            lbuff.anz_eingang =  to_decimal("0")
            lbuff.anz_ausgang =  to_decimal("0")
            lbuff.wert_eingang =  to_decimal("0")
            lbuff.wert_ausgang =  to_decimal("0")

        for l_opbuff in db_session.query(L_opbuff).filter(
                 (L_opbuff.artnr == curr_artnr) & (L_opbuff.datum >= from_date) & ((L_opbuff.op_art >= 2) & (L_opbuff.op_art <= 14)) & (L_opbuff.loeschflag <= 1)).order_by(L_opbuff._recid).all():
            l_opbuff.einzelpreis =  to_decimal(avrg_price)
            l_opbuff.warenwert =  to_decimal(avrg_price) * to_decimal(l_opbuff.anzahl)


        pass

        for l_opbuff in db_session.query(L_opbuff).filter(
                 (L_opbuff.artnr == curr_artnr) & (L_opbuff.datum >= start_date) & (L_opbuff.datum <= end_date) & ((L_opbuff.op_art >= 1) & (L_opbuff.op_art <= 4)) & (L_opbuff.loeschflag <= 1)).order_by(L_opbuff._recid).all():

            if l_opbuff.op_art <= 2:

                if lbuff:
                    lbuff.anz_eingang =  to_decimal(lbuff.anz_eingang) + to_decimal(l_opbuff.anzahl)
                    lbuff.wert_eingang =  to_decimal(lbuff.wert_eingang) + to_decimal(l_opbuff.warenwert)

                if l_bestand:

                    if l_opbuff.lager_nr == l_bestand.lager_nr:
                        l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(l_opbuff.anzahl)
                        l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(l_opbuff.warenwert)


            else:

                if lbuff:
                    lbuff.anz_ausgang =  to_decimal(lbuff.anz_ausgang) + to_decimal(l_opbuff.anzahl)
                    lbuff.wert_ausgang =  to_decimal(lbuff.wert_ausgang) + to_decimal(l_opbuff.warenwert)

                if l_bestand:

                    if l_opbuff.lager_nr == l_bestand.lager_nr:
                        l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(l_opbuff.anzahl)
                        l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(l_opbuff.warenwert)


        pass
        pass
        pass
        pass


    def update_ap():

        nonlocal docu_nr, msg_str, lvcarea, avrg_price, direct_issue, from_date, start_date, end_date, t_amount, tot_receiving, l_op, l_artikel, queasy, l_order, htparam, l_kredit, ap_journal, reslin_queasy, dml_artdep, dml_art, l_bestand, l_liefumsatz, l_pprice, bediener
        nonlocal pvilanguage, cancel_reason, str_list_l_recid, str_list_billdate, str_list_qty, bediener_nr, bediener_username, userinit
        nonlocal blop


        nonlocal blop

        flogic:bool = False
        billdate:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1016)]})
        flogic = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
        billdate = htparam.fdate

        if flogic:
            ap_journal = Ap_journal()
            db_session.add(ap_journal)

            ap_journal.lief_nr = l_op.lief_nr
            ap_journal.docu_nr = l_op.docu_nr
            ap_journal.lscheinnr = l_op.lscheinnr
            ap_journal.rgdatum = l_op.datum
            ap_journal.saldo =  to_decimal(t_amount)
            ap_journal.netto =  to_decimal(t_amount)
            ap_journal.userinit = userinit
            ap_journal.zeit = get_current_time_in_seconds()
            ap_journal.bemerk = "Cancel Receiving Inventory"

    # l_op = get_cache (L_op, {"_recid": [(eq, str_list_l_recid)]})
    l_op = db_session.query(L_op).with_for_update().filter(
             (L_op._recid == str_list_l_recid)).with_for_update().first()

    if l_op:
        pass
        direct_issue = l_op.flag
        l_op.loeschflag = 2
        l_op.stornogrund = bediener_username + ": " + to_string(get_current_date()) +\
                "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS") + ";Reason:" +\
                cancel_reason


        pass

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})
        from_date = str_list_billdate
        start_date = date_mdy(get_month(from_date) , 1, get_year(from_date))
        end_date = start_date + timedelta(days=35)
        end_date = date_mdy(get_month(end_date) , 1, get_year(end_date)) - timedelta(days=1)


        update_it()

        if not direct_issue:
            reorg_avrg_price(l_op.artnr, str_list_billdate)
        pass

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 328) & ((Queasy.char2 == ("Inv-Cek Reciving").lower()) | (Queasy.char2 == ("Inv-Cek Reorg").lower()) | (Queasy.char2 == ("Inv-Cek Journal").lower()))).order_by(Queasy._recid).with_for_update().all():
        db_session.delete(queasy)

    return generate_output()
