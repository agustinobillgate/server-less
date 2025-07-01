#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_kateg

def fa_artlist_depn_wertbl(fa_art_katnr:int):

    prepare_cache ([Fa_kateg])

    fa_kateg_nutzjahr = 0
    avail_fa_kateg = False
    fa_kateg = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_kateg_nutzjahr, avail_fa_kateg, fa_kateg
        nonlocal fa_art_katnr

        return {"fa_kateg_nutzjahr": fa_kateg_nutzjahr, "avail_fa_kateg": avail_fa_kateg}


    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_art_katnr)]})

    if fa_kateg and fa_kateg.methode == 0:
        avail_fa_kateg = True
        fa_kateg_nutzjahr = fa_kateg.nutzjahr

    return generate_output()