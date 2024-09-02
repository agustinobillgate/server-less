from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Debitor, Debthis

def mn_del_old_debtbl():
    i = 0
    ci_date:date = None
    htparam = debitor = debthis = None

    debt1 = debt = None

    Debt1 = Debitor
    Debt = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, debitor, debthis
        nonlocal debt1, debt


        nonlocal debt1, debt
        return {"i": i}

    def del_old_debt():

        nonlocal i, ci_date, htparam, debitor, debthis
        nonlocal debt1, debt


        nonlocal debt1, debt

        anz:int = 0
        curr_counter:int = 0
        Debt1 = Debitor

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 163)).first()
        anz = htparam.finteger

        if anz == 0:
            anz = 90

        debitor = db_session.query(Debitor).filter(
                (Debitor.opart == 2) &  (Debitor.zahlkonto > 0) &  ((Debitor.rgdatum + anz) < ci_date)).first()
        while None != debitor:

            debt1 = db_session.query(Debt1).filter(
                    (Debt1.counter == debitor.counter) &  (Debt1.zahlkonto > 0) &  (Debt1._recid != debitor._recid) &  ((Debt1.rgdatum + anz) >= ci_date)).first()

            if not debt1:
                i = i + 1
                curr_counter = debitor.counter

                for debt1 in db_session.query(Debt1).filter(
                        (Debt1.counter == curr_counter)).all():
                    create_debthis(debt1._recid)
                    db_session.delete(debt1)

        debitor = db_session.query(Debitor).filter(
                (Debitor.opart == 2) &  (Debitor.zahlkonto > 0) &  ((Debitor.rgdatum + anz) < ci_date)).first()

    def create_debthis(ar_recid:int):

        nonlocal i, ci_date, htparam, debitor, debthis
        nonlocal debt1, debt


        nonlocal debt1, debt


        Debt = Debitor

        debt = db_session.query(Debt).filter(
                    (Debt._recid == ar_recid)).first()
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
        debthis.saldo = debt.saldo
        debthis.vesrdep = debt.vesrdep
        debthis.vesrcod = debt.vesrcod
        debthis.verstat = debt.verstat
        debthis.bediener_nr = debt.bediener_nr

        debthis = db_session.query(Debthis).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    del_old_debt()

    return generate_output()