#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_artikel, L_order, Queasy, Htparam, L_kredit, Ap_journal, Reslin_queasy, Dml_artdep, Dml_art, L_bestand, L_liefumsatz, L_pprice, Bediener

def supply_inlist_update_it_all_by_lscheinnr_webbl(pvilanguage:int, cancel_reason:string, str_list_lscheinnr:string, str_list_billdate:date, bediener_nr:int, bediener_username:string, userinit:string):

    prepare_cache ([L_op, L_artikel, L_order, Htparam, Reslin_queasy, Dml_artdep, Dml_art, L_bestand, L_liefumsatz, Bediener])

    msg_str = ""
    lvcarea:string = "supply-inlist"
    avrg_price:Decimal = to_decimal("0.0")
    direct_issue:bool = False
    from_date:date = None
    start_date:date = None
    end_date:date = None
    t_amount:Decimal = to_decimal("0.0")
    time_cancel:string = ""
    l_op = l_artikel = l_order = queasy = htparam = l_kredit = ap_journal = reslin_queasy = dml_artdep = dml_art = l_bestand = l_liefumsatz = l_pprice = bediener = None

    buff_l_op = buff_l_artikel = blop = None

    Buff_l_op = create_buffer("Buff_l_op",L_op)
    Buff_l_artikel = create_buffer("Buff_l_artikel",L_artikel)
    Blop = create_buffer("Blop",L_op)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, avrg_price, direct_issue, from_date, start_date, end_date, t_amount, time_cancel, l_op, l_artikel, l_order, queasy, htparam, l_kredit, ap_journal, reslin_queasy, dml_artdep, dml_art, l_bestand, l_liefumsatz, l_pprice, bediener
        nonlocal pvilanguage, cancel_reason, str_list_lscheinnr, str_list_billdate, bediener_nr, bediener_username, userinit
        nonlocal buff_l_op, buff_l_artikel, blop


        nonlocal buff_l_op, buff_l_artikel, blop

        return {"msg_str": msg_str}

    def update_it():

        nonlocal msg_str, lvcarea, avrg_price, direct_issue, from_date, start_date, end_date, t_amount, time_cancel, l_op, l_artikel, l_order, queasy, htparam, l_kredit, ap_journal, reslin_queasy, dml_artdep, dml_art, l_bestand, l_liefumsatz, l_pprice, bediener
        nonlocal pvilanguage, cancel_reason, str_list_lscheinnr, str_list_billdate, bediener_nr, bediener_username, userinit
        nonlocal buff_l_op, buff_l_artikel, blop


        nonlocal buff_l_op, buff_l_artikel, blop

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
        tot_receiving:Decimal = to_decimal("0.0")
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

        l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, l_op.lief_nr)],"name": [(eq, l_op.docu_nr)],"lscheinnr": [(eq, l_op.lscheinnr)],"opart": [(le, 2)],"zahlkonto": [(eq, 0)]})

        if not l_kredit:

            l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, l_op.lief_nr)],"lscheinnr": [(eq, l_op.lscheinnr)],"rgdatum": [(eq, l_op.datum)],"opart": [(le, 2)],"zahlkonto": [(eq, 0)]})

        if l_kredit:
            pass
            db_session.delete(l_kredit)
            pass

            ap_journal = get_cache (Ap_journal, {"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.docu_nr)],"lscheinnr": [(eq, l_op.lscheinnr)]})

            if ap_journal:
                pass
                db_session.delete(ap_journal)
                pass

        if (substring(l_op.docu_nr, 0, 1) == ("P").lower()):

            l_order = get_cache (L_order, {"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.docu_nr)],"artnr": [(eq, l_op.artnr)],"einzelpreis": [(eq, l_op.einzelpreis)]})

            if not l_order:

                l_order = get_cache (L_order, {"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.docu_nr)],"artnr": [(eq, l_op.artnr)],"einzelpreis": [(eq, l_op.einzelpreis)],"geliefert": [(gt, l_op.anzahl)]})

                if not l_order:

                    l_order = get_cache (L_order, {"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.docu_nr)],"artnr": [(eq, l_op.artnr)]})

            if l_order:
                l_order.geliefert =  to_decimal(l_order.geliefert) - to_decimal(l_op.anzahl)
                l_order.rechnungswert =  to_decimal(l_order.rechnungswert) - to_decimal(l_op.warenwert)
                pass

                l_order1 = get_cache (L_order, {"docu_nr": [(eq, l_order.docu_nr)],"pos": [(eq, 0)]})
                l_order1.rechnungspreis =  to_decimal(l_order1.rechnungspreis) - to_decimal(l_op.warenwert)
                l_order1.rechnungswert =  to_decimal(l_order1.rechnungswert) - to_decimal(l_op.warenwert)
                pass
                pass
                pass

        elif substring(l_op.docu_nr, 0, 1) == ("D").lower() :
            dml_no = to_int(substring(l_op.docu_nr, 10, 2))
            dept_no = to_int(substring(l_op.docu_nr, 1, 2))

            if dml_no > 1:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("DML").lower()) & (to_int(entry(0, Reslin_queasy.char1, ";")) == l_op.artnr) & (Reslin_queasy.date1 == l_op.datum) & (to_int(entry(1, Reslin_queasy.char1, ";")) == dept_no) & (Reslin_queasy.number2 == dml_no)).first()

                if reslin_queasy:
                    reslin_queasy.deci3 =  to_decimal(reslin_queasy.deci3) - to_decimal(l_op.anzahl)


                    pass
                    pass
            else:

                dml_artdep = get_cache (Dml_artdep, {"artnr": [(eq, l_op.artnr)],"datum": [(eq, l_op.datum)],"departement": [(eq, dept_no)]})

                if dml_artdep:
                    dml_artdep.geliefert =  to_decimal(dml_artdep.geliefert) - to_decimal(l_op.anzahl)


                    pass
                    pass
                else:

                    dml_art = get_cache (Dml_art, {"artnr": [(eq, l_op.artnr)],"datum": [(eq, l_op.datum)]})

                    if dml_art:
                        dml_art.geliefert =  to_decimal(dml_art.geliefert) - to_decimal(l_op.anzahl)


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

                    buff_l_artikel = get_cache (L_artikel, {"_recid": [(eq, l_artikel._recid)]})

                    if buff_l_artikel:
                        pass
                        buff_l_artikel.vk_preis =  to_decimal(avrg_price)
                        pass
                        pass

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_artikel.artnr)]})

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op.anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)


                pass
                pass

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, l_op.lager_nr)],"artnr": [(eq, l_artikel.artnr)]})

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op.anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)


                pass
                pass

        elif direct_issue:

            l_op1 = get_cache (L_op, {"lscheinnr": [(eq, l_op.lscheinnr)],"artnr": [(eq, l_op.artnr)],"op_art": [(eq, 3)],"loeschflag": [(ne, 2)],"lief_nr": [(eq, l_op.lief_nr)],"herkunftflag": [(eq, 2)],"lager_nr": [(eq, l_op.lager_nr)]})

            if l_op1:

                l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_artikel.artnr)]})

                if l_bestand:
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op1.anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op1.warenwert)
                    l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(l_op1.anzahl)
                    l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(l_op1.warenwert)


                    pass
                    pass

                l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, l_op1.lager_nr)],"artnr": [(eq, l_artikel.artnr)]})

                if l_bestand:
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op1.anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op1.warenwert)
                    l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(l_op1.anzahl)
                    l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(l_op1.warenwert)


                    pass
                    pass
                pass
            else:

                l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_artikel.artnr)]})

                if l_bestand:
                    l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op.anzahl)
                    l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)


                    pass
                    pass

                l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, l_op.lager_nr)],"artnr": [(eq, l_artikel.artnr)]})

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
                pass

        l_liefumsatz = get_cache (L_liefumsatz, {"lief_nr": [(eq, l_op.lief_nr)],"datum": [(eq, str_list_billdate)]})

        if l_liefumsatz:
            l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) - to_decimal(l_op.warenwert)
            pass
            pass

        if substring(l_op.docu_nr, 0, 1) == ("D").lower()  or substring(l_op.docu_nr, 0, 1) == ("I").lower() :

            l_pprice = get_cache (L_pprice, {"artnr": [(eq, l_op.artnr)],"bestelldatum": [(eq, l_op.datum)],"anzahl": [(eq, l_op.anzahl)],"einzelpreis": [(eq, l_op.einzelpreis)],"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.lscheinnr)]})

            if l_pprice:
                pass
                db_session.delete(l_pprice)
                pass

        elif substring(l_op.docu_nr, 0, 1) == ("P").lower() :

            l_pprice = get_cache (L_pprice, {"artnr": [(eq, l_op.artnr)],"bestelldatum": [(eq, l_op.datum)],"anzahl": [(eq, l_op.anzahl)],"einzelpreis": [(eq, l_op.einzelpreis)],"lief_nr": [(eq, l_op.lief_nr)],"docu_nr": [(eq, l_op.docu_nr)]})

            if l_pprice:
                pass
                db_session.delete(l_pprice)
                pass

        for blop in db_session.query(Blop).filter(
                 (Blop.lscheinnr == l_op.lscheinnr) & (Blop.lief_nr > 0) & (Blop.loeschflag <= 1)).order_by(Blop._recid).all():
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


    def reorg_avrg_price(curr_artnr:int, from_date:date):

        nonlocal msg_str, lvcarea, avrg_price, direct_issue, start_date, end_date, t_amount, time_cancel, l_op, l_artikel, l_order, queasy, htparam, l_kredit, ap_journal, reslin_queasy, dml_artdep, dml_art, l_bestand, l_liefumsatz, l_pprice, bediener
        nonlocal pvilanguage, cancel_reason, str_list_lscheinnr, str_list_billdate, bediener_nr, bediener_username, userinit
        nonlocal buff_l_op, buff_l_artikel, blop


        nonlocal buff_l_op, buff_l_artikel, blop

        t_anz:Decimal = to_decimal("0.0")
        t_wert:Decimal = to_decimal("0.0")
        lbuff = None
        l_opbuff = None
        Lbuff =  create_buffer("Lbuff",L_bestand)
        L_opbuff =  create_buffer("L_opbuff",L_op)

        l_bestand = get_cache (L_bestand, {"anf_best_dat": [(ge, start_date),(le, end_date)],"artnr": [(eq, curr_artnr)],"lager_nr": [(eq, l_op.lager_nr)]})

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

        if l_opbuff:
            pass
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

        if lbuff:
            pass
            pass

        if l_bestand:
            pass
            pass


    def update_ap():

        nonlocal msg_str, lvcarea, avrg_price, direct_issue, from_date, start_date, end_date, t_amount, time_cancel, l_op, l_artikel, l_order, queasy, htparam, l_kredit, ap_journal, reslin_queasy, dml_artdep, dml_art, l_bestand, l_liefumsatz, l_pprice, bediener
        nonlocal pvilanguage, cancel_reason, str_list_lscheinnr, str_list_billdate, bediener_nr, bediener_username, userinit
        nonlocal buff_l_op, buff_l_artikel, blop


        nonlocal buff_l_op, buff_l_artikel, blop

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


    time_cancel = to_string(get_current_time_in_seconds(), "HH:MM:SS")
    from_date = str_list_billdate
    start_date = date_mdy(get_month(from_date) , 1, get_year(from_date))
    end_date = start_date + timedelta(days=35)
    end_date = date_mdy(get_month(end_date) , 1, get_year(end_date)) - timedelta(days=1)

    l_op_obj_list = {}
    l_op = L_op()
    l_artikel = L_artikel()
    for l_op.lief_nr, l_op.docu_nr, l_op.lscheinnr, l_op.datum, l_op.artnr, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.lager_nr, l_op.zeit, l_op._recid, l_op.flag, l_op.loeschflag, l_op.stornogrund, l_artikel.endkum, l_artikel.vk_preis, l_artikel._recid, l_artikel.artnr in db_session.query(L_op.lief_nr, L_op.docu_nr, L_op.lscheinnr, L_op.datum, L_op.artnr, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.lager_nr, L_op.zeit, L_op._recid, L_op.flag, L_op.loeschflag, L_op.stornogrund, L_artikel.endkum, L_artikel.vk_preis, L_artikel._recid, L_artikel.artnr).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
             (L_op.lief_nr > 0) & (L_op.lscheinnr == (str_list_lscheinnr).lower()) & (L_op.loeschflag <= 1) & (L_op.op_art == 1)).order_by(L_op._recid).all():
        if l_op_obj_list.get(l_op._recid):
            continue
        else:
            l_op_obj_list[l_op._recid] = True

        buff_l_op = get_cache (L_op, {"_recid": [(eq, l_op._recid)]})

        if buff_l_op:
            pass
            direct_issue = buff_l_op.flag
            buff_l_op.loeschflag = 2
            buff_l_op.stornogrund = bediener_username + ": " + to_string(get_current_date()) +\
                    "-" + time_cancel + ";Reason:" +\
                    cancel_reason


            pass
            pass
        update_it()

        if not direct_issue:
            reorg_avrg_price(l_op.artnr, str_list_billdate)

    l_op = get_cache (L_op, {"lscheinnr": [(eq, str_list_lscheinnr)]})

    if l_op:

        l_order = get_cache (L_order, {"docu_nr": [(eq, l_op.docu_nr)],"lief_nr": [(eq, l_op.lief_nr)],"pos": [(eq, 0)],"loeschflag": [(eq, 1)]})

        if l_order:
            msg_str = msg_str + chr_unicode(2) + "&Q" + translateExtended ("Purchase Order closed; re-open it?", lvcarea, "")

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 328) & ((Queasy.char2 == ("Inv-Cek Reciving").lower()) | (Queasy.char2 == ("Inv-Cek Reorg").lower()) | (Queasy.char2 == ("Inv-Cek Journal").lower()))).order_by(Queasy._recid).all():
        db_session.delete(queasy)

    return generate_output()