#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit, Htparam

def release_ap_def_actionbl(pay_list_s_recid:int):

    prepare_cache ([Htparam])

    success_flag = False
    i_counter:int = 0
    it_exist:bool = False
    l_kredit = htparam = None

    debt = None

    Debt = create_buffer("Debt",L_kredit)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, i_counter, it_exist, l_kredit, htparam
        nonlocal pay_list_s_recid
        nonlocal debt


        nonlocal debt

        return {"success_flag": success_flag}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1118)]})

    debt = db_session.query(Debt).filter(
             (Debt._recid == pay_list_s_recid)).first()

    if not debt:

        return generate_output()

    if debt and debt.rgdatum <= htparam.fdate:

        return generate_output()

    l_kredit = get_cache (L_kredit, {"counter": [(eq, debt.counter)],"zahlkonto": [(eq, 0)]})

    if l_kredit:
        i_counter = l_kredit.counter
        pass
        db_session.delete(debt)
        pass
        pass
        l_kredit.opart = 0
        success_flag = True

        debt = db_session.query(Debt).filter(
                 (Debt.counter == i_counter) & (Debt.zahlkonto > 0) & (Debt.opart == 2)).first()

        if debt:

            for debt in db_session.query(Debt).filter(
                     (Debt.counter == i_counter) & (Debt.zahlkonto > 0) & (Debt.opart == 2)).order_by(Debt._recid).all():
                debt.opart = 1
                it_exist = True
        else:

            for debt in db_session.query(Debt).filter(
                     (Debt.counter == i_counter) & (Debt.zahlkonto > 0) & (Debt.opart == 1)).order_by(Debt._recid).all():
                it_exist = True

        if not it_exist:
            l_kredit.counter = 0
        pass

    return generate_output()