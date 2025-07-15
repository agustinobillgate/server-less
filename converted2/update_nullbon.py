from functions.additional_functions import *
import decimal
from datetime import date
from models import Umsatz, Kellner, Htparam, Hoteldpt, Kellne1

def update_nullbon():
    tot_balance:decimal = to_decimal("0.0")
    tot_balance1:decimal = to_decimal("0.0")
    datum:date = None
    bill_date:date = None
    umsatz = kellner = htparam = hoteldpt = kellne1 = None

    umsatz0 = umsatz1 = umsatz2 = umsatz3 = waiter = None

    Umsatz0 = create_buffer("Umsatz0",Umsatz)
    Umsatz1 = create_buffer("Umsatz1",Umsatz)
    Umsatz2 = create_buffer("Umsatz2",Umsatz)
    Umsatz3 = create_buffer("Umsatz3",Umsatz)
    Waiter = create_buffer("Waiter",Kellner)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_balance, tot_balance1, datum, bill_date, umsatz, kellner, htparam, hoteldpt, kellne1
        nonlocal umsatz0, umsatz1, umsatz2, umsatz3, waiter


        nonlocal umsatz0, umsatz1, umsatz2, umsatz3, waiter

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num >= 1)).order_by(Hoteldpt.num).all():

        for kellner in db_session.query(Kellner).filter(
                 (Kellner.departement == hoteldpt.num)).order_by(Kellner.kellnername).all():

            kellne1 = db_session.query(Kellne1).filter(
                     (Kellne1.kellner_nr == kellner.kellner_nr) & (Kellne1.departement == hoteldpt.num)).first()
            tot_balance =  to_decimal(kellner.saldo)

            if kellne1:
                tot_balance1 =  to_decimal(kellne1.saldo)
            for datum in date_range((bill_date - 9),bill_date) :

                umsatz = db_session.query(Umsatz).filter(
                         (Umsatz.artnr == kellner.kumsatz_nr) & (Umsatz.departement == kellner.departement) & (Umsatz.datum == datum)).first()

                umsatz1 = db_session.query(Umsatz1).filter(
                         (Umsatz1.artnr == kellner.kcredit_nr) & (Umsatz1.departement == 0) & (Umsatz1.datum == datum)).first()

                umsatz2 = db_session.query(Umsatz2).filter(
                         (Umsatz2.artnr == kellner.kzahl_nr) & (Umsatz2.departement == kellner.departement) & (Umsatz2.datum == datum)).first()

                if umsatz:
                    tot_balance =  to_decimal(tot_balance) + to_decimal(umsatz.betrag)

                if umsatz1:
                    tot_balance =  to_decimal(tot_balance) - to_decimal(umsatz1.betrag)

                if umsatz2:
                    tot_balance =  to_decimal(tot_balance) + to_decimal(umsatz2.betrag)

                if kellne1:

                    umsatz0 = db_session.query(Umsatz0).filter(
                             (Umsatz0.artnr == kellne1.kumsatz_nr) & (Umsatz0.departement == kellne1.departement) & (Umsatz0.datum == datum)).first()

                    umsatz3 = db_session.query(Umsatz3).filter(
                             (Umsatz3.artnr == kellne1.kzahl_nr) & (Umsatz3.departement == kellne1.departement) & (Umsatz3.datum == datum)).first()

                    if umsatz0:
                        tot_balance1 =  to_decimal(tot_balance1) + to_decimal(umsatz0.betrag)

                    if umsatz3:
                        tot_balance1 =  to_decimal(tot_balance1) + to_decimal(umsatz3.betrag)

            if (tot_balance != 0 or tot_balance1 != 0) and not kellner.nullbon:

                waiter = db_session.query(Waiter).filter(
                         (Waiter._recid == kellner._recid)).first()
                waiter.nullbon = True

    return generate_output()