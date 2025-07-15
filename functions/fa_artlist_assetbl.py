#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mathis

def fa_artlist_assetbl(m_list_asset:string, recid_mathis:int):

    prepare_cache ([Mathis])

    avail_mathis1 = False
    mathis1_name = ""
    mathis = None

    mathis1 = None

    Mathis1 = create_buffer("Mathis1",Mathis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_mathis1, mathis1_name, mathis
        nonlocal m_list_asset, recid_mathis
        nonlocal mathis1


        nonlocal mathis1

        return {"avail_mathis1": avail_mathis1, "mathis1_name": mathis1_name}


    mathis1 = get_cache (Mathis, {"asset": [(eq, m_list_asset)],"_recid": [(ne, recid_mathis)]})

    if mathis1:
        avail_mathis1 = True
        mathis1_name = mathis1.name

    return generate_output()