from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Htparam, L_op, L_artikel, L_bestand, L_liefumsatz, Gl_acct, L_kredit, Ap_journal

def cancel_dpurchasebl(lief_nr:int, docu_nr:str, user_init:str):
    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    billdate = None
    fb_closedate = None
    m_closedate = None
    negative_oh:bool = False
    lscheinnr:str = ""
    curr_lager:int = 0
    anzahl:decimal = 0
    wert:decimal = 0
    t_amount:decimal = 0
    tot_anz:decimal = 0
    tot_wert:decimal = 0
    bediener = htparam = l_op = l_artikel = l_bestand = l_liefumsatz = gl_acct = l_kredit = ap_journal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, negative_oh, lscheinnr, curr_lager, anzahl, wert, t_amount, tot_anz, tot_wert, bediener, htparam, l_op, l_artikel, l_bestand, l_liefumsatz, gl_acct, l_kredit, ap_journal


        return {"f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "billdate": billdate, "fb_closedate": fb_closedate, "m_closedate": m_closedate}

    def check_onhand():

        nonlocal f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, negative_oh, lscheinnr, curr_lager, anzahl, wert, t_amount, tot_anz, tot_wert, bediener, htparam, l_op, l_artikel, l_bestand, l_liefumsatz, gl_acct, l_kredit, ap_journal


        billdate = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
        fb_closedate = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
        m_closedate = htparam.fdate

        for l_op in db_session.query(L_op).filter(
                (L_op.lief_nr == lief_nr) &  (func.lower(L_op.(docu_nr).lower()) == (docu_nr).lower()) &  (func.lower(L_op.lscheinnr) == (docu_nr).lower()) &  (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (L_op.pos > 0)).all():

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_op.artnr)).first()

            if (l_artikel.endkum <= 2 and l_op.datum <= fb_closedate) or (l_artikel.endkum > 2 and l_op.datum <= m_closedate):

                l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == l_op.artnr) &  (L_bestand.lager_nr == curr_lager)).first()

                if l_bestand and (l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang - l_op.anzahl) < 0:
                    negative_oh = True

                    return

    def update_ap():

        nonlocal f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, negative_oh, lscheinnr, curr_lager, anzahl, wert, t_amount, tot_anz, tot_wert, bediener, htparam, l_op, l_artikel, l_bestand, l_liefumsatz, gl_acct, l_kredit, ap_journal

        ap_license:bool = False
        ap_acct:str = ""
        do_it:bool = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1016)).first()

        if not htparam.flogical:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 986)).first()
        ap_acct = htparam.fchar

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (ap_acct).lower())).first()

        if not gl_acct:
            do_it = False

        if not do_it:

            return

        l_kredit = db_session.query(L_kredit).filter(
                (func.lower(L_kredit.name) == (docu_nr).lower()) &  (L_kredit.saldo == - t_amount) &  (L_kredit.lief_nr == lief_nr) &  (L_kredit.rgdatum == billdate)).first()

        if l_kredit:

            l_kredit = db_session.query(L_kredit).first()
            db_session.delete(l_kredit)
        else:
            l_kredit = L_kredit()
            db_session.add(l_kredit)

            l_kredit.name = docu_nr
            l_kredit.lief_nr = lief_nr
            l_kredit.lscheinnr = lscheinnr
            l_kredit.rgdatum = billdate
            l_kredit.datum = None
            l_kredit.saldo = t_amount
            l_kredit.ziel = 0
            l_kredit.netto = t_amount
            l_kredit.bediener_nr = bediener.nr
        ap_journal = Ap_journal()
        db_session.add(ap_journal)

        ap_journal.lief_nr = lief_nr
        ap_journal.docu_nr = docu_nr
        ap_journal.lscheinnr = docu_nr
        ap_journal.rgdatum = billdate
        ap_journal.saldo = t_amount
        ap_journal.netto = t_amount
        ap_journal.userinit = bediener.userinit
        ap_journal.zeit = get_current_time_in_seconds()
        ap_journal.bemerk = "Cancel Direct Purchase"


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

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
            (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    fb_closedate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 221)).first()
    m_closedate = htparam.fdate
    check_onhand()

    if negative_oh:

        return generate_output()

    for l_op in db_session.query(L_op).filter(
            (L_op.lief_nr == lief_nr) &  (func.lower(L_op.(docu_nr).lower()) == (docu_nr).lower()) &  (func.lower(L_op.lscheinnr) == (docu_nr).lower()) &  (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (L_op.pos > 0)).all():

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_op.artnr)).first()
        l_op.loeschflag = 2
        curr_lager = l_op.lager_nr
        billdate = l_op.datum
        anzahl = - l_op.anzahl
        wert = - l_op.warenwert
        t_amount = t_amount + wert

        if ((l_artikel.endkum == f_endkum or l_artikel.endkum == b_endkum) and not l_op.flag and billdate <= fb_closedate) or (l_artikel.endkum >= m_endkum and billdate <= m_closedate and not l_op.flag):

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0) &  (L_bestand.artnr == l_artikel.artnr)).first()
            l_bestand.anz_eingang = l_bestand.anz_eingang + anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang + wert
            tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
            tot_wert = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang

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

            if tot_anz != 0:

                l_artikel = db_session.query(L_artikel).first()
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
    update_ap()

    return generate_output()