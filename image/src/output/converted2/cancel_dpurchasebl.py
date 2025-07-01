#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Htparam, L_op, L_artikel, L_bestand, L_liefumsatz, Gl_acct, L_kredit, Ap_journal

def cancel_dpurchasebl(lief_nr:int, docu_nr:string, user_init:string):

    prepare_cache ([Bediener, Htparam, L_op, L_artikel, L_bestand, L_liefumsatz, Ap_journal])

    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    billdate = None
    fb_closedate = None
    m_closedate = None
    negative_oh:bool = False
    lscheinnr:string = ""
    curr_lager:int = 0
    anzahl:Decimal = to_decimal("0.0")
    wert:Decimal = to_decimal("0.0")
    t_amount:Decimal = to_decimal("0.0")
    tot_anz:Decimal = to_decimal("0.0")
    tot_wert:Decimal = to_decimal("0.0")
    bediener = htparam = l_op = l_artikel = l_bestand = l_liefumsatz = gl_acct = l_kredit = ap_journal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, negative_oh, lscheinnr, curr_lager, anzahl, wert, t_amount, tot_anz, tot_wert, bediener, htparam, l_op, l_artikel, l_bestand, l_liefumsatz, gl_acct, l_kredit, ap_journal
        nonlocal lief_nr, docu_nr, user_init

        return {"f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "billdate": billdate, "fb_closedate": fb_closedate, "m_closedate": m_closedate}

    def check_onhand():

        nonlocal f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, negative_oh, lscheinnr, curr_lager, anzahl, wert, t_amount, tot_anz, tot_wert, bediener, htparam, l_op, l_artikel, l_bestand, l_liefumsatz, gl_acct, l_kredit, ap_journal
        nonlocal lief_nr, docu_nr, user_init


        billdate = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
        fb_closedate = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
        m_closedate = htparam.fdate

        for l_op in db_session.query(L_op).filter(
                 (L_op.lief_nr == lief_nr) & (L_op.docu_nr == (docu_nr).lower()) & (L_op.lscheinnr == (docu_nr).lower()) & (L_op.op_art == 1) & (L_op.loeschflag <= 1) & (L_op.pos > 0)).order_by(L_op._recid).all():

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})

            if (l_artikel.endkum <= 2 and l_op.datum <= fb_closedate) or (l_artikel.endkum > 2 and l_op.datum <= m_closedate):

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, curr_lager)]})

                if l_bestand and (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang - l_op.anzahl) < 0:
                    negative_oh = True

                    return


    def update_ap():

        nonlocal f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, negative_oh, lscheinnr, curr_lager, anzahl, wert, t_amount, tot_anz, tot_wert, bediener, htparam, l_op, l_artikel, l_bestand, l_liefumsatz, gl_acct, l_kredit, ap_journal
        nonlocal lief_nr, docu_nr, user_init

        ap_license:bool = False
        ap_acct:string = ""
        do_it:bool = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1016)]})

        if not htparam.flogical:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 986)]})
        ap_acct = htparam.fchar

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, ap_acct)]})

        if not gl_acct:
            do_it = False

        if not do_it:

            return

        l_kredit = get_cache (L_kredit, {"name": [(eq, docu_nr)],"saldo": [(eq, - t_amount)],"lief_nr": [(eq, lief_nr)],"rgdatum": [(eq, billdate)]})

        if l_kredit:
            pass
            db_session.delete(l_kredit)
        else:
            l_kredit = L_kredit()
            db_session.add(l_kredit)

            l_kredit.name = docu_nr
            l_kredit.lief_nr = lief_nr
            l_kredit.lscheinnr = lscheinnr
            l_kredit.rgdatum = billdate
            l_kredit.datum = None
            l_kredit.saldo =  to_decimal(t_amount)
            l_kredit.ziel = 0
            l_kredit.netto =  to_decimal(t_amount)
            l_kredit.bediener_nr = bediener.nr
        ap_journal = Ap_journal()
        db_session.add(ap_journal)

        ap_journal.lief_nr = lief_nr
        ap_journal.docu_nr = docu_nr
        ap_journal.lscheinnr = docu_nr
        ap_journal.rgdatum = billdate
        ap_journal.saldo =  to_decimal(t_amount)
        ap_journal.netto =  to_decimal(t_amount)
        ap_journal.userinit = bediener.userinit
        ap_journal.zeit = get_current_time_in_seconds()
        ap_journal.bemerk = "Cancel Direct Purchase"

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    f_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    b_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
    m_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    fb_closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    m_closedate = htparam.fdate
    check_onhand()

    if negative_oh:

        return generate_output()

    for l_op in db_session.query(L_op).filter(
             (L_op.lief_nr == lief_nr) & (L_op.docu_nr == (docu_nr).lower()) & (L_op.lscheinnr == (docu_nr).lower()) & (L_op.op_art == 1) & (L_op.loeschflag <= 1) & (L_op.pos > 0)).order_by(L_op._recid).all():

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})
        l_op.loeschflag = 2
        curr_lager = l_op.lager_nr
        billdate = l_op.datum
        anzahl =  - to_decimal(l_op.anzahl)
        wert =  - to_decimal(l_op.warenwert)
        t_amount =  to_decimal(t_amount) + to_decimal(wert)

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and not l_op.flag and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate and not l_op.flag):

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_artikel.artnr)]})
            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)
            tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
            tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
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

            if tot_anz != 0:
                pass
                l_artikel.vk_preis =  to_decimal(tot_wert) / to_decimal(tot_anz)
                pass

        l_liefumsatz = get_cache (L_liefumsatz, {"lief_nr": [(eq, lief_nr)],"datum": [(eq, billdate)]})

        if not l_liefumsatz:
            l_liefumsatz = L_liefumsatz()
            db_session.add(l_liefumsatz)

            l_liefumsatz.datum = billdate
            l_liefumsatz.lief_nr = lief_nr
        l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) + to_decimal(wert)
    update_ap()

    return generate_output()