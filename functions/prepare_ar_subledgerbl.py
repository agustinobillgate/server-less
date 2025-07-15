#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Artikel, Htparam

def prepare_ar_subledgerbl(artno:int):

    prepare_cache ([Htparam])

    long_digit = False
    to_date = None
    double_currency = False
    t_artikel_data = []
    artikel = htparam = None

    t_artikel = None

    t_artikel_data, T_artikel = create_model_like(Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, to_date, double_currency, t_artikel_data, artikel, htparam
        nonlocal artno


        nonlocal t_artikel
        nonlocal t_artikel_data

        return {"long_digit": long_digit, "to_date": to_date, "double_currency": double_currency, "t-artikel": t_artikel_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    to_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    if artno > 0:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (Artikel.artnr == artno)).order_by(Artikel._recid).all():
            t_artikel = T_artikel()
            t_artikel_data.append(t_artikel)

            buffer_copy(artikel, t_artikel)

    else:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7)) & (Artikel.activeflag)).order_by(Artikel.artnr).all():
            t_artikel = T_artikel()
            t_artikel_data.append(t_artikel)

            buffer_copy(artikel, t_artikel)


    return generate_output()