#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_kateg

def fa_artlist_katnrbl(fa_art_katnr:string):

    prepare_cache ([Fa_kateg])

    avail_fa_kateg = False
    fa_kateg_rate = to_decimal("0.0")
    fa_kateg = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_fa_kateg, fa_kateg_rate, fa_kateg
        nonlocal fa_art_katnr

        return {"avail_fa_kateg": avail_fa_kateg, "fa_kateg_rate": fa_kateg_rate}


    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, to_int(fa_art_katnr))]})

    if fa_kateg:
        avail_fa_kateg = True
        fa_kateg_rate =  to_decimal(fa_kateg.rate)

    return generate_output()