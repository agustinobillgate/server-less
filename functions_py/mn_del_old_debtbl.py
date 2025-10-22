#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Debitor, Debthis

def mn_del_old_debtbl():

    prepare_cache ([Htparam, Debitor, Debthis])

    i = 0
    ci_date:date = None
    htparam = debitor = debthis = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, debitor, debthis

        return {"i": i}

    def del_old_debt():

        nonlocal i, ci_date, htparam, debitor, debthis

        debt1 = None
        anz:int = 0
        curr_counter:int = 0
        Debt1 =  create_buffer("Debt1",Debitor)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 163)]})
        anz = htparam.finteger

        if anz == 0:
            anz = 90

        debitor = db_session.query(Debitor).filter(
                 (Debitor.opart == 2) & (Debitor.zahlkonto > 0) & ((Debitor.rgdatum + anz) < ci_date)).first()
        while None != debitor:

            debt1 = db_session.query(Debt1).filter(
                     (Debt1.counter == debitor.counter) & (Debt1.zahlkonto > 0) & (Debt1._recid != debitor._recid) & ((Debt1.rgdatum + anz) >= ci_date)).first()

            if not debt1:
                i = i + 1
                curr_counter = debitor.counter

                for debt1 in db_session.query(Debt1).filter(
                         (Debt1.counter == curr_counter)).order_by(Debt1._recid).all():
                    create_debthis(debt1._recid)
                    db_session.delete(debt1)

            curr_recid = debitor._recid
            debitor = db_session.query(Debitor).filter(
                     (Debitor.opart == 2) & (Debitor.zahlkonto > 0) & ((Debitor.rgdatum + anz) < ci_date) & (Debitor._recid > curr_recid)).first()


    def create_debthis(ar_recid:int):

        nonlocal i, ci_date, htparam, debitor, debthis

        debt = None
        Debt =  create_buffer("Debt",Debitor)

        debt = get_cache (Debitor, {"_recid": [(eq, ar_recid)]})
        debthis = Debthis()
        db_session.add(debthis)

        debthis.artnr = debt.artnr
        debthis.rechnr = debt.rechnr
        debthis.rgdatum = debt.rgdatum
        debthis.counter = debt.counter
        debthis.zahlkonto = debt.zahlkonto
        debthis.gastnr = debt.gastnr
        debthis.gastnrmember = debt.gastnrmember
        debthis.name = debt.name
        debthis.zinr = debt.zinr
        debthis.saldo =  to_decimal(debt.saldo)
        debthis.vesrdep =  to_decimal(debt.vesrdep)
        debthis.vesrcod = debt.vesrcod
        debthis.verstat = debt.verstat
        debthis.bediener_nr = debt.bediener_nr


        pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    del_old_debt()

    return generate_output()