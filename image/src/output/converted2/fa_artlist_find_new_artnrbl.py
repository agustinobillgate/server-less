#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_artikel, Mathis

def fa_artlist_find_new_artnrbl(endkum:int, zwkum:int):

    prepare_cache ([Fa_artikel, Mathis])

    new_artnr = 0
    l_end:int = 0
    l_zw:int = 0
    fa_artikel = mathis = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_artnr, l_end, l_zw, fa_artikel, mathis
        nonlocal endkum, zwkum

        return {"new_artnr": new_artnr}

    l_end = length(to_string(endkum))
    l_zw = length(to_string(zwkum))

    for fa_artikel in db_session.query(Fa_artikel).filter(
             (Fa_artikel.subgrp == zwkum) & (Fa_artikel.gnr == endkum)).order_by(Fa_artikel._recid).all():

        mathis = get_cache (Mathis, {"nr": [(eq, fa_artikel.nr)]})

        if mathis:

            if to_int(substring(mathis.asset, 0, l_end)) == endkum and to_int(substring(mathis.asset, 3, l_zw)) == zwkum:
                new_artnr = to_int(mathis.asset) + 1

                return generate_output()

    if l_end == 1 and l_zw == 1:
        new_artnr = endkum * 10000000 + zwkum * 10000 + 1

    elif l_end == 1 and l_zw == 2:
        new_artnr = endkum * 10000000 + zwkum * 1000 + 1

    elif l_end == 1 and l_zw == 3:
        new_artnr = endkum * 10000000 + zwkum * 100 + 1

    elif l_end == 2 and l_zw == 1:
        new_artnr = endkum * 1000000 + zwkum * 10000 + 1

    elif l_end == 2 and l_zw == 2:
        new_artnr = endkum * 1000000 + zwkum * 1000 + 1

    elif l_end == 2 and l_zw == 3:
        new_artnr = endkum * 1000000 + zwkum * 100 + 1

    elif l_end == 3 and l_zw == 1:
        new_artnr = endkum * 100000 + zwkum * 10000 + 1

    elif l_end == 3 and l_zw == 2:
        new_artnr = endkum * 100000 + zwkum * 1000 + 1

    elif l_end == 3 and l_zw == 3:
        new_artnr = endkum * 100000 + zwkum * 100 + 1

    return generate_output()