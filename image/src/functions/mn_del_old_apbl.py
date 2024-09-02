from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_kredit

def mn_del_old_apbl():
    i = 0
    ci_date:date = None
    htparam = l_kredit = None

    debt1 = None

    Debt1 = L_kredit

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, l_kredit
        nonlocal debt1


        nonlocal debt1
        return {"i": i}

    def del_old_ap():

        nonlocal i, ci_date, htparam, l_kredit
        nonlocal debt1


        nonlocal debt1

        i:int = 0
        anz:int = 0
        Debt1 = L_kredit

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1085)).first()
        anz = htparam.finteger

        if anz == 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 163)).first()
            anz = htparam.finteger

        if anz == 0:
            anz = 90

        l_kredit = db_session.query(L_kredit).filter(
                (L_kredit.opart == 2) &  (L_kredit.zahlkonto > 0) &  ((L_kredit.rgdatum + anz) < ci_date)).first()
        while None != l_kredit:

            debt1 = db_session.query(Debt1).filter(
                    (Debt1.counter == l_kredit.counter) &  (Debt1.zahlkonto > 0) &  (Debt1._recid != l_kredit._recid) &  ((Debt1.rgdatum + anz) >= ci_date)).first()

            if not debt1:
                i = i + 1

                for debt1 in db_session.query(Debt1).filter(
                        (Debt1.counter == l_kredit.counter)).all():
                    db_session.delete(debt1)

        l_kredit = db_session.query(L_kredit).filter(
                (L_kredit.opart == 2) &  (L_kredit.zahlkonto > 0) &  ((L_kredit.rgdatum + anz) < ci_date)).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    del_old_ap()

    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit.opart == 2) &  (L_kredit.zahlkonto == 0) &  ((L_kredit.rgdatum + anz) < ci_date)).first()
    while None != l_kredit:

        debt1 = db_session.query(Debt1).filter(
                (Debt1.counter == l_kredit.counter) &  (Debt1.zahlkonto > 0)).first()

        if not debt1:

            debt1 = db_session.query(Debt1).filter(
                    (Debt1._recid == l_kredit._recid)).first()
            db_session.delete(debt1)


        l_kredit = db_session.query(L_kredit).filter(
                (L_kredit.opart == 2) &  (L_kredit.zahlkonto == 0) &  ((L_kredit.rgdatum + anz) < ci_date)).first()

    return generate_output()