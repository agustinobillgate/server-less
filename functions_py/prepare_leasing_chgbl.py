# using conversion tools version: 1.0.0.119
"""_yusufwijasena_06/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - only convert
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Guest

def prepare_leasing_chgbl(nr: int):

    prepare_cache([Queasy, Guest])

    gastnr = 0
    gastnrmember = 0
    amount = to_decimal("0.0")
    arrival = None
    departure = None
    rsvname = ""
    guestname = ""
    queasy = guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gastnr, gastnrmember, amount, arrival, departure, rsvname, guestname, queasy, guest
        nonlocal nr

        return {
            "gastnr": gastnr,
            "gastnrmember": gastnrmember,
            "amount": amount,
            "arrival": arrival,
            "departure": departure,
            "rsvname": rsvname,
            "guestname": guestname
        }

    queasy = get_cache(Queasy, {"key": [(eq, 329)], "number3": [(eq, nr)]})

    if queasy:
        arrival = queasy.date2
        departure = queasy.date3
        gastnrmember = queasy.number1
        gastnr = queasy.number2
        amount = to_decimal(queasy.deci1)

        guest = get_cache(
            Guest, {"gastnr": [(eq, queasy.number2)]})

        if guest:
            rsvname = guest.name + "," + guest.vorname1

        guest = get_cache(
            Guest, {"gastnr": [(eq, queasy.number1)]})

        if guest:
            guestname = guest.name + "," + guest.vorname1

    return generate_output()
