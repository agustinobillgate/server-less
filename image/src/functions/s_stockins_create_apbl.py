from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, L_lieferant, L_op, Htparam, Gl_acct, L_kredit, Ap_journal

def s_stockins_create_apbl(lief_nr:int, lscheinnr:str, billdate:date, t_amount:decimal, user_init:str):
    bediener = l_lieferant = l_op = htparam = gl_acct = l_kredit = ap_journal = None

    l_op1 = None

    L_op1 = L_op

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bediener, l_lieferant, l_op, htparam, gl_acct, l_kredit, ap_journal
        nonlocal l_op1


        nonlocal l_op1
        return {}

    def create_ap():

        nonlocal bediener, l_lieferant, l_op, htparam, gl_acct, l_kredit, ap_journal
        nonlocal l_op1


        nonlocal l_op1

        ap_license:bool = False
        ap_acct:str = ""
        do_it:bool = True
        L_op1 = L_op

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 986)).first()
        ap_acct = htparam.fchar

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (ap_acct).lower())).first()

        if gl_acct:

            if l_lieferant.z_code != "":

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == l_lieferant.z_code)).first()

                if gl_acct and (l_lieferant.z_code != ap_acct):
                    do_it = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1016)).first()
        ap_license = htparam.flogical

        if ap_license and do_it:

            l_kredit = db_session.query(L_kredit).filter(
                    (L_kredit.lief_nr == lief_nr) &  (func.lower(L_kredit.name) == (lscheinnr).lower()) &  (func.lower(L_kredit.(lscheinnr).lower()) == (lscheinnr).lower()) &  (L_kredit.rgdatum == billdate) &  (L_kredit.opart <= 2) &  (L_kredit.zahlkonto == 0)).first()

            if l_kredit:

                l_kredit = db_session.query(L_kredit).first()
                l_kredit.netto = l_kredit.netto + t_amount
                l_kredit.saldo = l_kredit.saldo + t_amount

                l_kredit = db_session.query(L_kredit).first()
            else:
                l_kredit = L_kredit()
                db_session.add(l_kredit)

                l_kredit.name = lscheinnr
                l_kredit.lief_nr = lief_nr
                l_kredit.lscheinnr = lscheinnr
                l_kredit.rgdatum = billdate
                l_kredit.datum = None
                l_kredit.saldo = t_amount
                l_kredit.ziel = 30
                l_kredit.netto = t_amount
                l_kredit.bediener_nr = bediener.nr

                l_kredit = db_session.query(L_kredit).first()
            ap_journal = Ap_journal()
            db_session.add(ap_journal)

            ap_journal.lief_nr = lief_nr
            ap_journal.docu_nr = lscheinnr
            ap_journal.lscheinnr = lscheinnr
            ap_journal.rgdatum = billdate
            ap_journal.saldo = t_amount
            ap_journal.netto = t_amount
            ap_journal.userinit = bediener.userinit
            ap_journal.zeit = get_current_time_in_seconds()


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()
    create_ap()

    return generate_output()