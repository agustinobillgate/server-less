#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Artikel

def prepare_ar_debtlistbl():

    prepare_cache ([Htparam, Artikel])

    from_date = None
    to_date = None
    from_art = 999999
    to_art = 0
    from_bez = ""
    to_bez = ""
    htparam = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, from_art, to_art, from_bez, to_bez, htparam, artikel

        return {"from_date": from_date, "to_date": to_date, "from_art": from_art, "to_art": to_art, "from_bez": from_bez, "to_bez": to_bez}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

    if htparam.finteger > 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        to_date = htparam.fdate
    else:
        to_date = get_current_date()
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7)) & (Artikel.activeflag)).order_by(Artikel._recid).all():

        if from_art > artikel.artnr:
            from_art = artikel.artnr
            from_bez = artikel.bezeich

        if to_art < artikel.artnr:
            to_art = artikel.artnr
            to_bez = artikel.bezeich

    return generate_output()