#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_order

def mk_pr_defaction_b1bl(rec_id:int, bez:string):

    prepare_cache ([L_order])

    l_order = None

    l_od = None

    L_od = create_buffer("L_od",L_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order
        nonlocal rec_id, bez
        nonlocal l_od


        nonlocal l_od

        return {}


    l_order = get_cache (L_order, {"_recid": [(eq, rec_id)]})

    l_od = get_cache (L_order, {"_recid": [(eq, l_order._recid)]})
    l_od.quality = substring(l_od.quality, 0, 11) + bez
    pass

    return generate_output()