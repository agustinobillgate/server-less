from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.create_lartjob import create_lartjob
from models import Bediener, L_ophdr, Htparam, L_op, L_bestand, Gl_acct, L_kredit, Ap_journal

def cancel_dissuebl(lief_nr:int, docu_nr:str, user_init:str):
    wert:decimal = to_decimal("0.0")
    billdate:date = None
    closedate:date = None
    anzahl:decimal = to_decimal("0.0")
    t_amount:decimal = to_decimal("0.0")
    tot_anz:decimal = to_decimal("0.0")
    tot_wert:decimal = to_decimal("0.0")
    lscheinnr:str = ""
    bediener = l_ophdr = htparam = l_op = l_bestand = gl_acct = l_kredit = ap_journal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal wert, billdate, closedate, anzahl, t_amount, tot_anz, tot_wert, lscheinnr, bediener, l_ophdr, htparam, l_op, l_bestand, gl_acct, l_kredit, ap_journal
        nonlocal lief_nr, docu_nr, user_init


        return {}

    def update_ap():

        nonlocal wert, billdate, closedate, anzahl, t_amount, tot_anz, tot_wert, lscheinnr, bediener, l_ophdr, htparam, l_op, l_bestand, gl_acct, l_kredit, ap_journal
        nonlocal lief_nr, docu_nr, user_init

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
                 (func.lower(L_kredit.name) == (docu_nr).lower()) & (L_kredit.saldo == - t_amount) & (L_kredit.lief_nr == lief_nr) & (L_kredit.rgdatum == billdate)).first()

        if l_kredit:
            db_session.delete(l_kredit)
        else:
            l_kredit = L_kredit()
            db_session.add(l_kredit)

            l_kredit.name = docu_nr
            l_kredit.lief_nr = lief_nr
            l_kredit.lscheinnr = lscheinnr
            l_kredit.rgdatum = billdate
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
        ap_journal.bemerk = "Cancel Direct Issueing"

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()
    lscheinnr = docu_nr

    l_ophdr = db_session.query(L_ophdr).filter(
             (func.lower(L_ophdr.lscheinnr) == (lscheinnr).lower()) & (func.lower(L_ophdr.op_typ) == ("STT").lower())).first()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 224)).first()
    closedate = htparam.fdate

    for l_op in db_session.query(L_op).filter(
             (L_op.lief_nr == lief_nr) & (func.lower(L_op.lscheinnr) == (docu_nr).lower()) & ((L_op.op_art == 1) | (L_op.op_art == 3)) & (L_op.flag) & (L_op.loeschflag == 0) & (L_op.pos > 0)).order_by(L_op._recid).all():
        l_op.loeschflag = 2
        billdate = l_op.datum
        wert =  - to_decimal(l_op.warenwert)

        if l_op.op_art == 1:
            t_amount =  to_decimal(t_amount) + to_decimal(wert)

            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == l_op.lager_nr) & (L_bestand.artnr == l_op.artnr)).first()

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op.anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)
                l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(l_op.anzahl)
                l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(l_op.warenwert)

            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == 0) & (L_bestand.artnr == l_op.artnr)).first()

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op.anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)
                l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(l_op.anzahl)
                l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(l_op.warenwert)

        elif l_op.op_art == 3 and l_ophdr.betriebsnr != 0:
            get_output(create_lartjob(l_ophdr._recid, l_op.artnr, - l_op.anzahl, - l_op.warenwert, l_op.datum, False))
    update_ap()

    return generate_output()