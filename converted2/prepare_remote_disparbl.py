#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Guest, Artikel

def prepare_remote_disparbl(guestno:int):

    prepare_cache ([Htparam, Guest, Artikel])

    long_digit = False
    day1 = 0
    day2 = 0
    day3 = 0
    price_decimal = 0
    from_art = 0
    to_art = 0
    htparam = guest = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, day1, day2, day3, price_decimal, from_art, to_art, htparam, guest, artikel
        nonlocal guestno

        return {"long_digit": long_digit, "day1": day1, "day2": day2, "day3": day3, "price_decimal": price_decimal, "from_art": from_art, "to_art": to_art}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 330)]})

    if htparam.finteger != 0:
        day1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 331)]})

    if htparam.finteger != 0:
        day2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 332)]})

    if htparam.finteger != 0:
        day3 = htparam.finteger
    day2 = day2 + day1
    day3 = day3 + day2

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    guest = get_cache (Guest, {"gastnr": [(eq, guestno)]})

    if guest and guest.zahlungsart != 0:
        from_art = guest.zahlungsart
        to_art = from_art


    else:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (Artikel.artart == 2) & (Artikel.activeflag)).order_by(Artikel._recid).all():

            if from_art > artikel.artnr:
                from_art = artikel.artnr

            if to_art < artikel.artnr:
                to_art = artikel.artnr

    return generate_output()