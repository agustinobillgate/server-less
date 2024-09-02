from functions.additional_functions import *
import decimal
from models import L_kredit, Htparam

def release_ap_def_actionbl(pay_list_s_recid:int):
    success_flag = False
    i_counter:int = 0
    it_exist:bool = False
    l_kredit = htparam = None

    debt = None

    Debt = L_kredit

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, i_counter, it_exist, l_kredit, htparam
        nonlocal debt


        nonlocal debt
        return {"success_flag": success_flag}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1118)).first()

    debt = db_session.query(Debt).filter(
            (Debt._recid == pay_list_s_recid)).first()

    if debt and debt.rgdatum <= htparam.fdate:

        return generate_output()

    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit.counter == debt.counter) &  (L_kredit.zahlkonto == 0)).first()

    if l_kredit:
        i_counter = l_kredit.counter

        debt = db_session.query(Debt).first()
        db_session.delete(debt)

        l_kredit = db_session.query(L_kredit).first()
        l_kredit.opart = 0

        l_kredit = db_session.query(L_kredit).first()
        success_flag = True

        debt = db_session.query(Debt).filter(
                (Debt.counter == i_counter) &  (Debt.zahlkonto > 0) &  (Debt.opart == 2)).first()

        if debt:

            for debt in db_session.query(Debt).filter(
                    (Debt.counter == i_counter) &  (Debt.zahlkonto > 0) &  (Debt.opart == 2)).all():
                debt.opart = 1
                it_exist = True
    else:

        for debt in db_session.query(Debt).filter(
                (Debt.counter == i_counter) &  (Debt.zahlkonto > 0) &  (Debt.opart == 1)).all():
            it_exist = True

    if not it_exist:

        l_kredit = db_session.query(L_kredit).first()
        l_kredit.counter = 0

        l_kredit = db_session.query(L_kredit).first()

    return generate_output()