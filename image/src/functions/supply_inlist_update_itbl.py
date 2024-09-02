from functions.additional_functions import *
import decimal
from datetime import date
from models import L_op, L_artikel, L_order, Htparam, L_kredit, L_bestand, L_liefumsatz, L_pprice, Dml_art, Dml_artdep, Ap_journal

def supply_inlist_update_itbl(pvilanguage:int, cancel_reason:str, str_list_l_recid:int, str_list_billdate:date, str_list_qty:decimal, bediener_nr:int, bediener_username:str, userinit:str):
    docu_nr = 0
    msg_str = ""
    lvcarea:str = "supply_inlist"
    avrg_price:decimal = None
    direct_issue:bool = False
    from_date:date = None
    start_date:date = None
    end_date:date = None
    t_amount:decimal = 0
    l_op = l_artikel = l_order = htparam = l_kredit = l_bestand = l_liefumsatz = l_pprice = dml_art = dml_artdep = ap_journal = None

    l_order1 = l_op1 = l_opbuff = lbuff = None

    L_order1 = L_order
    L_op1 = L_op
    L_opbuff = L_op
    Lbuff = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal docu_nr, msg_str, lvcarea, avrg_price, direct_issue, from_date, start_date, end_date, t_amount, l_op, l_artikel, l_order, htparam, l_kredit, l_bestand, l_liefumsatz, l_pprice, dml_art, dml_artdep, ap_journal
        nonlocal l_order1, l_op1, l_opbuff, lbuff


        nonlocal l_order1, l_op1, l_opbuff, lbuff
        return {"docu_nr": docu_nr, "msg_str": msg_str}

    def update_it():

        nonlocal docu_nr, msg_str, lvcarea, avrg_price, direct_issue, from_date, start_date, end_date, t_amount, l_op, l_artikel, l_order, htparam, l_kredit, l_bestand, l_liefumsatz, l_pprice, dml_art, dml_artdep, ap_journal
        nonlocal l_order1, l_op1, l_opbuff, lbuff


        nonlocal l_order1, l_op1, l_opbuff, lbuff

        f_endkum:int = 0
        b_endkum:int = 0
        m_endkum:int = 0
        billdate:date = None
        fb_closedate:date = None
        m_closedate:date = None
        tot_anz:decimal = 0
        tot_wert:decimal = 0
        curr_pos:int = 0
        answer:bool = True
        L_order1 = L_order
        L_op1 = L_op
        L_opbuff = L_op

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 257)).first()
        f_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 258)).first()
        b_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 268)).first()
        m_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
        fb_closedate = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
        m_closedate = htparam.fdate

        l_kredit = db_session.query(L_kredit).filter(
                (L_kredit.lief_nr == l_op.lief_nr) &  (L_kredit.name == l_op.docu_nr) &  (L_kredit.lscheinnr == l_op.lscheinnr) &  (L_kredit.opart <= 2) &  (L_kredit.zahlkonto == 0)).first()

        if not l_kredit:

            l_kredit = db_session.query(L_kredit).filter(
                    (L_kredit.lief_nr == l_op.lief_nr) &  (L_kredit.lscheinnr == l_op.lscheinnr) &  (L_kredit.rgdatum == l_op.datum) &  (L_kredit.opart <= 2) &  (L_kredit.zahlkonto == 0)).first()

        if l_kredit:

            l_kredit = db_session.query(L_kredit).first()

            if l_kredit.saldo == l_op.warenwert:
                db_session.delete(l_kredit)

            else:
                l_kredit.saldo = l_kredit.saldo - l_op.warenwert
                l_kredit.netto = l_kredit.netto - l_op.warenwert

                l_kredit = db_session.query(L_kredit).first()

            t_amount = t_amount - l_op.warenwert


            update_ap()

        if (substring(l_op.docu_nr, 0, 1) == "P"):

            l_order = db_session.query(L_order).filter(
                    (L_order.lief_nr == l_op.lief_nr) &  (L_order.docu_nr == l_op.docu_nr) &  (L_order.artnr == l_op.artnr) &  (L_order.einzelpreis == l_op.einzelpreis)).first()

            if not l_order:

                if str_list_qty > 0:

                    l_order = db_session.query(L_order).filter(
                            (L_order.lief_nr == l_op.lief_nr) &  (L_order.docu_nr == l_op.docu_nr) &  (L_order.artnr == l_op.artnr) &  (L_order.einzelpreis == l_op.einzelpreis) &  (L_order.geliefert > (str_list_qty / L_order.txtnr))).first()
                else:

                    l_order = db_session.query(L_order).filter(
                            (L_order.lief_nr == l_op.lief_nr) &  (L_order.docu_nr == l_op.docu_nr) &  (L_order.artnr == l_op.artnr) &  (L_order.einzelpreis == l_op.einzelpreis) &  (L_order.geliefert > (str_list_qty / L_order.txtnr))).first()

                if not l_order:

                    l_order = db_session.query(L_order).filter(
                            (L_order.lief_nr == l_op.lief_nr) &  (L_order.docu_nr == l_op.docu_nr) &  (L_order.artnr == l_op.artnr)).first()

            if l_order:
                l_order.geliefert = l_order.geliefert - str_list_qty / l_order.txtnr
                l_order.rechnungswert = l_order.rechnungswert - l_op.warenwert

                l_order = db_session.query(L_order).first()

                l_order1 = db_session.query(L_order1).filter(
                        (L_order1.docu_nr == l_order.docu_nr) &  (L_order1.pos == 0)).first()
                l_order1.rechnungspreis = l_order1.rechnungspreis - l_op.warenwert
                l_order1.rechnungswert = l_order1.rechnungswert - l_op.warenwert

                l_order1 = db_session.query(L_order1).first()

        if not direct_issue:

            if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and (str_list_billdate <= fb_closedate)) or ((l_artikel.endkum >= m_endkum) and (str_list_billdate <= m_closedate)):

                l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == l_op.artnr) &  (L_bestand.lager_nr == 0)).first()

                if l_bestand:
                    tot_anz = l_bestand.anz_anf_best
                    tot_wert = l_bestand.val_anf_best

                for l_opbuff in db_session.query(L_opbuff).filter(
                        (L_opbuff.artnr == l_op.artnr) &  (L_opbuff.op_art == 1) &  (L_opbuff.datum <= end_date) &  (L_opbuff.loeschflag <= 1)).all():
                    tot_anz = tot_anz + l_opbuff.anzahl
                    tot_wert = tot_wert + l_opbuff.warenwert

                if tot_anz != 0:
                    avrg_price = tot_wert / tot_anz
                else:

                    if l_bestand and l_bestand.anz_anf_best != 0:
                        avrg_price = l_bestand.val_anf_best / l_bestand.anz_anf_best
                    else:
                        avrg_price = l_artikel.vk_preis

                if avrg_price != l_artikel.vk_preis:

                    l_artikel = db_session.query(L_artikel).first()
                    l_artikel.vk_preis = avrg_price

                    l_artikel = db_session.query(L_artikel).first()

        elif direct_issue:

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0) &  (L_bestand.artnr == l_artikel.artnr)).first()

            if l_bestand:
                l_bestand.anz_eingang = l_bestand.anz_eingang - str_list_qty
                l_bestand.wert_eingang = l_bestand.wert_eingang - l_op.warenwert
                l_bestand.anz_ausgang = l_bestand.anz_ausgang - str_list_qty
                l_bestand.wert_ausgang = l_bestand.wert_ausgang - l_op.warenwert

                l_bestand = db_session.query(L_bestand).first()

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == l_op.lager_nr) &  (L_bestand.artnr == l_artikel.artnr)).first()

            if l_bestand:
                l_bestand.anz_eingang = l_bestand.anz_eingang - str_list_qty
                l_bestand.wert_eingang = l_bestand.wert_eingang - l_op.warenwert
                l_bestand.anz_ausgang = l_bestand.anz_ausgang - str_list_qty
                l_bestand.wert_ausgang = l_bestand.wert_ausgang - l_op.warenwert

                l_bestand = db_session.query(L_bestand).first()

            l_op1 = db_session.query(L_op1).filter(
                    (L_op1.artnr == l_op.artnr) &  (L_op1.op_art == 3) &  (L_op1.lief_nr == l_op.lief_nr) &  (L_op1.lscheinnr == l_op.lscheinnr) &  (L_op1.herkunftflag == 2) &  (L_op1.lager_nr == l_op.lager_nr)).first()

            if l_op1:
                l_op1.loeschflag = 2
                l_op1.betriebsnr = bediener_nr

                l_op1 = db_session.query(L_op1).first()

        l_liefumsatz = db_session.query(L_liefumsatz).filter(
                (L_liefumsatz.lief_nr == l_op.lief_nr) &  (L_liefumsatz.datum == str_list_billdate)).first()

        if l_liefumsatz:
            l_liefumsatz.gesamtumsatz = l_liefumsatz.gesamtumsatz - l_op.warenwert

        l_order = db_session.query(L_order).filter(
                (L_order.docu_nr == l_op.docu_nr) &  (L_order.lief_nr == l_op.lief_nr) &  (L_order.pos == 0) &  (L_order.loeschflag == 1)).first()

        if l_order:
            docu_nr = recid (l_op)
            msg_str = msg_str + chr(2) + "&Q" + translateExtended ("Purchase Order closed; re_open it?", lvcarea, "")

        l_pprice = db_session.query(L_pprice).filter(
                (L_pprice.artnr == l_op.artnr) &  (L_pprice.bestelldatum == l_op.datum) &  (L_pprice.anzahl == l_op.anzahl) &  (L_pprice.einzelpreis == l_op.einzelpreis) &  (L_pprice.lief_nr == l_op.lief_nr) &  (L_pprice.docu_nr == l_op.docu_nr)).first()

        if l_pprice:
            db_session.delete(l_pprice)


        if l_op.loeschflag == 2:

            dml_art = db_session.query(Dml_art).filter(
                    (Dml_art.artnr == l_op.artnr) &  (Dml_art.datum == l_op.datum) &  (Dml_art.anzahl > 0)).first()

            if dml_art:
                dml_art.geliefert = 0

                dml_art = db_session.query(Dml_art).first()

            elif not dml_art:

                dml_artdep = db_session.query(Dml_artdep).filter(
                        (Dml_artdep.artnr == l_op.artnr) &  (Dml_artdep.datum == l_op.datum) &  (Dml_artdep.anzahl > 0)).first()

                if dml_artdep:
                    dml_artdep.geliefert = 0

                    dml_artdep = db_session.query(Dml_artdep).first()

    def reorg_avrg_price(curr_artnr:int, from_date:date):

        nonlocal docu_nr, msg_str, lvcarea, avrg_price, direct_issue, start_date, end_date, t_amount, l_op, l_artikel, l_order, htparam, l_kredit, l_bestand, l_liefumsatz, l_pprice, dml_art, dml_artdep, ap_journal
        nonlocal l_order1, l_op1, l_opbuff, lbuff


        nonlocal l_order1, l_op1, l_opbuff, lbuff

        t_anz:decimal = 0
        t_wert:decimal = 0
        Lbuff = L_bestand
        L_opbuff = L_op

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.anf_best_dat >= start_date) &  (L_bestand.anf_best_dat <= end_date) &  (L_bestand.artnr == curr_artnr) &  (L_bestand.lager_nr == l_op.lager_nr)).first()

        if l_bestand:
            l_bestand.anz_eingang = 0
            l_bestand.anz_ausgang = 0
            l_bestand.wert_eingang = 0
            l_bestand.wert_ausgang = 0

        lbuff = db_session.query(Lbuff).filter(
                (Lbuff.anf_best_dat >= start_date) &  (Lbuff.anf_best_dat <= end_date) &  (Lbuff.artnr == curr_artnr) &  (Lbuff.lager_nr == 0)).first()

        if lbuff:
            lbuff.anz_eingang = 0
            lbuff.anz_ausgang = 0
            lbuff.wert_eingang = 0
            lbuff.wert_ausgang = 0

        for l_opbuff in db_session.query(L_opbuff).filter(
                (L_opbuff.artnr == curr_artnr) &  (L_opbuff.datum >= from_date) &  ((L_opbuff.op_art >= 2) &  (L_opbuff.op_art <= 14)) &  (L_opbuff.loeschflag <= 1)).all():
            l_opbuff.einzelpreis = avrg_price
            l_opbuff.warenwert = avrg_price * l_opbuff.anzahl

        for l_opbuff in db_session.query(L_opbuff).filter(
                (L_opbuff.artnr == curr_artnr) &  (L_opbuff.datum >= start_date) &  (L_opbuff.datum <= end_date) &  ((L_opbuff.op_art >= 1) &  (L_opbuff.op_art <= 4)) &  (L_opbuff.loeschflag <= 1)).all():

            if l_opbuff.op_art <= 2:

                if lbuff:
                    lbuff.anz_eingang = lbuff.anz_eingang + l_opbuff.anzahl
                    lbuff.wert_eingang = lbuff.wert_eingang + l_opbuff.warenwert

                if l_bestand:

                    if l_opbuff.lager_nr == l_bestand.lager_nr:
                        l_bestand.anz_eingang = l_bestand.anz_eingang + l_opbuff.anzahl
                        l_bestand.wert_eingang = l_bestand.wert_eingang + l_opbuff.warenwert


            else:

                if lbuff:
                    lbuff.anz_ausgang = lbuff.anz_ausgang + l_opbuff.anzahl
                    lbuff.wert_ausgang = lbuff.wert_ausgang + l_opbuff.warenwert

                if l_bestand:

                    if l_opbuff.lager_nr == l_bestand.lager_nr:
                        l_bestand.anz_ausgang = l_bestand.anz_ausgang + l_opbuff.anzahl
                        l_bestand.wert_ausgang = l_bestand.wert_ausgang + l_opbuff.warenwert

        lbuff = db_session.query(Lbuff).first()

        l_bestand = db_session.query(L_bestand).first()

    def update_ap():

        nonlocal docu_nr, msg_str, lvcarea, avrg_price, direct_issue, from_date, start_date, end_date, t_amount, l_op, l_artikel, l_order, htparam, l_kredit, l_bestand, l_liefumsatz, l_pprice, dml_art, dml_artdep, ap_journal
        nonlocal l_order1, l_op1, l_opbuff, lbuff


        nonlocal l_order1, l_op1, l_opbuff, lbuff

        flogic:bool = False
        billdate:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1016)).first()
        flogic = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 474)).first()
        billdate = htparam.fdate

        if flogic:
            ap_journal = Ap_journal()
            db_session.add(ap_journal)

            ap_journal.lief_nr = l_op.lief_nr
            ap_journal.docu_nr = l_op.docu_nr
            ap_journal.lscheinnr = l_op.lscheinnr
            ap_journal.rgdatum = l_op.datum
            ap_journal.saldo = t_amount
            ap_journal.netto = t_amount
            ap_journal.userinit = userinit
            ap_journal.zeit = get_current_time_in_seconds()
            ap_journal.bemerk = "Cancel Receiving Inventory"


    l_op = db_session.query(L_op).filter(
            (L_op._recid == str_list_l_recid)).first()

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == l_op.artnr)).first()
    direct_issue = l_op.flag
    l_op.loeschflag = 2
    l_op.stornogrund = bediener_username + ": " + to_string(get_current_date()) +\
            "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS") + ";Reason:" +\
            cancel_reason

    l_op = db_session.query(L_op).first()
    from_date = str_list_billdate
    start_date = date_mdy(get_month(from_date) , 1, get_year(from_date))
    end_date = start_date + 35
    end_date = date_mdy(get_month(end_date) , 1, get_year(end_date)) - 1


    update_it()

    if not direct_issue:
        reorg_avrg_price(l_op.artnr, str_list_billdate)

    return generate_output()