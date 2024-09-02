from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_kredit, Ap_journal

def po_retour_update_apbl(docu_nr:str, t_amount:decimal, lief_nr:int, billdate:date, lscheinnr:str, bediener_nr:int, bediener_userinit:str):
    l_kredit = ap_journal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_kredit, ap_journal


        return {}

    def update_ap():

        nonlocal l_kredit, ap_journal

        l_kredit = db_session.query(L_kredit).filter(
                (func.lower(L_kredit.name) == (docu_nr).lower()) &  (L_kredit.saldo == - t_amount) &  (L_kredit.lief_nr == lief_nr) &  (L_kredit.rgdatum == billdate) &  (L_kredit.zahlkonto == 0)).first()

        if not l_kredit:
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
            l_kredit.bediener_nr = bediener_nr
            ap_journal = Ap_journal()
            db_session.add(ap_journal)

            ap_journal.lief_nr = lief_nr
            ap_journal.docu_nr = docu_nr
            ap_journal.lscheinnr = lscheinnr
            ap_journal.rgdatum = billdate
            ap_journal.saldo = t_amount
            ap_journal.netto = t_amount
            ap_journal.userinit = bediener_userinit
            ap_journal.zeit = get_current_time_in_seconds()
            ap_journal.bemerk = "Return"

            return

        if l_kredit.counter == 0:

            l_kredit = db_session.query(L_kredit).first()
            db_session.delete(l_kredit)

            return
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
            l_kredit.bediener_nr = bediener_nr
        ap_journal = Ap_journal()
        db_session.add(ap_journal)

        ap_journal.lief_nr = lief_nr
        ap_journal.docu_nr = docu_nr
        ap_journal.lscheinnr = lscheinnr
        ap_journal.rgdatum = billdate
        ap_journal.saldo = t_amount
        ap_journal.netto = t_amount
        ap_journal.userinit = bediener_userinit
        ap_journal.zeit = get_current_time_in_seconds()
        ap_journal.bemerk = "Return"

    update_ap()

    return generate_output()