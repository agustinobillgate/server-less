#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Mathis, Fa_artikel

def fa_artlist_m_list_assetbl(asset:string):

    prepare_cache ([Mathis, Fa_artikel])

    avail_asset = False
    mathis_name = ""
    mathis = fa_artikel = None

    mathis1 = None

    Mathis1 = create_buffer("Mathis1",Mathis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_asset, mathis_name, mathis, fa_artikel
        nonlocal asset
        nonlocal mathis1


        nonlocal mathis1

        return {"avail_asset": avail_asset, "mathis_name": mathis_name}


    mathis1 = get_cache (Mathis, {"asset": [(eq, asset)]})

    if mathis1:

        fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, mathis1.nr)]})

        if fa_artikel.loeschflag == 0:
            avail_asset = True
            mathis_name = mathis1.name

    return generate_output()