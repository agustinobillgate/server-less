#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit, Ap_journal

def po_retour_update_apbl(docu_nr:string, t_amount:Decimal, lief_nr:int, billdate:date, lscheinnr:string, bediener_nr:int, bediener_userinit:string):

    prepare_cache ([Ap_journal])

    l_kredit = ap_journal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_kredit, ap_journal
        nonlocal docu_nr, t_amount, lief_nr, billdate, lscheinnr, bediener_nr, bediener_userinit

        return {}

    def update_ap():

        nonlocal l_kredit, ap_journal
        nonlocal docu_nr, t_amount, lief_nr, billdate, lscheinnr, bediener_nr, bediener_userinit

        l_kredit = get_cache (L_kredit, {"name": [(eq, docu_nr)],"saldo": [(eq, - t_amount)],"lief_nr": [(eq, lief_nr)],"rgdatum": [(eq, billdate)],"zahlkonto": [(eq, 0)]})

        if not l_kredit:
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
            l_kredit.bediener_nr = bediener_nr
            ap_journal = Ap_journal()
            db_session.add(ap_journal)

            ap_journal.lief_nr = lief_nr
            ap_journal.docu_nr = docu_nr
            ap_journal.lscheinnr = lscheinnr
            ap_journal.rgdatum = billdate
            ap_journal.saldo =  to_decimal(t_amount)
            ap_journal.netto =  to_decimal(t_amount)
            ap_journal.userinit = bediener_userinit
            ap_journal.zeit = get_current_time_in_seconds()
            ap_journal.bemerk = "Return"

            return

        if l_kredit.counter == 0:
            pass
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
            l_kredit.saldo =  to_decimal(t_amount)
            l_kredit.ziel = 0
            l_kredit.netto =  to_decimal(t_amount)
            l_kredit.bediener_nr = bediener_nr
        ap_journal = Ap_journal()
        db_session.add(ap_journal)

        ap_journal.lief_nr = lief_nr
        ap_journal.docu_nr = docu_nr
        ap_journal.lscheinnr = lscheinnr
        ap_journal.rgdatum = billdate
        ap_journal.saldo =  to_decimal(t_amount)
        ap_journal.netto =  to_decimal(t_amount)
        ap_journal.userinit = bediener_userinit
        ap_journal.zeit = get_current_time_in_seconds()
        ap_journal.bemerk = "Return"


    update_ap()

    return generate_output()