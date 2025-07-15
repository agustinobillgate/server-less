#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_grup

def fa_artlist_gnrbl(fa_art_gnr:string):

    prepare_cache ([Fa_grup])

    grp_bez = ""
    avail_fa_grup = False
    fa_grup = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal grp_bez, avail_fa_grup, fa_grup
        nonlocal fa_art_gnr

        return {"grp_bez": grp_bez, "avail_fa_grup": avail_fa_grup}


    fa_grup = get_cache (Fa_grup, {"gnr": [(eq, to_int(fa_art_gnr))],"flag": [(eq, 0)]})

    if fa_grup:
        avail_fa_grup = True
        grp_bez = fa_grup.bezeich

    return generate_output()