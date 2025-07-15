#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Fa_artikel, Mathis

def prepare_fa_salebl(nr:int):

    prepare_cache ([Htparam, Fa_artikel, Mathis])

    last_close = None
    datum = None
    qty = 0
    amt = to_decimal("0.0")
    mathis_name = ""
    mathis_asset = ""
    fa_artikel_anzahl = 0
    htparam = fa_artikel = mathis = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal last_close, datum, qty, amt, mathis_name, mathis_asset, fa_artikel_anzahl, htparam, fa_artikel, mathis
        nonlocal nr

        return {"last_close": last_close, "datum": datum, "qty": qty, "amt": amt, "mathis_name": mathis_name, "mathis_asset": mathis_asset, "fa_artikel_anzahl": fa_artikel_anzahl}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})

    if htparam:
        last_close = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 372)]})

    if htparam:
        datum = htparam.fdate

    fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, nr)]})

    if fa_artikel:
        qty = fa_artikel.anzahl
        amt =  to_decimal(fa_artikel.book_wert)
        fa_artikel_anzahl = fa_artikel.anzahl

        mathis = get_cache (Mathis, {"nr": [(eq, fa_artikel.nr)]})

        if mathis:
            mathis_name = mathis.name
            mathis_asset = mathis.asset

    return generate_output()