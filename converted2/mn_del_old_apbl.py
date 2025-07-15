#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_kredit

def mn_del_old_apbl():

    prepare_cache ([Htparam])

    i = 0
    ci_date:date = None
    htparam = l_kredit = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, l_kredit

        return {"i": i}

    def del_old_ap():

        nonlocal ci_date, htparam, l_kredit

        i:int = 0
        debt1 = None
        debt2 = None
        anz:int = 0
        total_saldo:Decimal = to_decimal("0.0")
        Debt1 =  create_buffer("Debt1",L_kredit)
        Debt2 =  create_buffer("Debt2",L_kredit)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1085)]})
        anz = htparam.finteger

        if anz == 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 163)]})
            anz = htparam.finteger

        if anz == 0:
            anz = 90

        l_kredit = db_session.query(L_kredit).filter(
                 (L_kredit.opart == 2) & (L_kredit.zahlkonto > 0) & ((L_kredit.rgdatum + anz) <= (ci_date + timedelta(days=1)))).first()
        while None != l_kredit:
            i = i + 1
            total_saldo =  to_decimal("0")

            for debt1 in db_session.query(Debt1).filter(
                     (Debt1.counter == l_kredit.counter) & (Debt1.lscheinnr == l_kredit.lscheinnr)).order_by(Debt1._recid).all():
                total_saldo =  to_decimal(total_saldo) + to_decimal(debt1.saldo)

            if total_saldo == 0:

                for debt2 in db_session.query(Debt2).filter(
                         (Debt2.counter == l_kredit.counter) & (Debt2.lscheinnr == l_kredit.lscheinnr)).order_by(Debt2._recid).all():
                    db_session.delete(debt2)

            curr_recid = l_kredit._recid
            l_kredit = db_session.query(L_kredit).filter(
                     (L_kredit.opart == 2) & (L_kredit.zahlkonto > 0) & ((L_kredit.rgdatum + anz) <= (ci_date + timedelta(days=1))) & (L_kredit._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    del_old_ap()

    return generate_output()