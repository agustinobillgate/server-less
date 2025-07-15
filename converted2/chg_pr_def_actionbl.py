#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_order

def chg_pr_def_actionbl(s_recid:int, bez:string):

    prepare_cache ([L_order])

    l_order = None

    l_od = None

    L_od = create_buffer("L_od",L_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order
        nonlocal s_recid, bez
        nonlocal l_od


        nonlocal l_od

        return {}


    l_od = get_cache (L_order, {"_recid": [(eq, s_recid)]})
    l_od.quality = to_string(substring(l_od.quality, 0, 11) , "x(11)") + bez
    pass

    return generate_output()