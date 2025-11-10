# using conversion tools version: 1.0.0.119
"""_yusufwijasena_06/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - only convert
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy


def leasing_update_queasybl(casetype: int, nr: int, gastnr: int, gastnrmember: int, amount: Decimal, arrival: date, departure: date):

    prepare_cache([Htparam])

    success_flag = False
    bill_date: date = None
    counter: int = 0
    htparam = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bill_date, counter, htparam, queasy
        nonlocal casetype, nr, gastnr, gastnrmember, amount, arrival, departure

        return {
            "success_flag": success_flag
        }

    htparam = get_cache(Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        bill_date = htparam.fdate

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 329)).order_by(Queasy.number3).all():
        counter = queasy.number3 + 1

        break

    if counter == 0:
        counter = 1

    if casetype == 1:
        queasy = Queasy()

        queasy.key = 329
        queasy.date1 = bill_date
        queasy.date2 = arrival
        queasy.date3 = departure
        queasy.number1 = gastnrmember
        queasy.number2 = gastnr
        queasy.number3 = counter
        queasy.deci1 = to_decimal(amount)

        db_session.add(queasy)

    elif casetype == 2:
        queasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number3": [(eq, nr)]})

        if not queasy:
            queasy = Queasy()

            queasy.key = 329
            queasy.date2 = arrival
            queasy.date3 = departure
            queasy.number1 = gastnrmember
            queasy.number2 = gastnr
            queasy.number3 = counter
            queasy.deci1 = to_decimal(amount)

            db_session.add(queasy)

        else:
            queasy.date2 = arrival
            queasy.date3 = departure
            queasy.number1 = gastnrmember
            queasy.number2 = gastnr
            queasy.deci1 = to_decimal(amount)

    elif casetype == 3:
        queasy = get_cache(
            Queasy, {"key": [(eq, 329)], "number3": [(eq, nr)]})

        if queasy:
            db_session.delete(queasy)

    return generate_output()
