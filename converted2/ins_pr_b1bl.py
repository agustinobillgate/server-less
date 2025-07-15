#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_order

def ins_pr_b1bl(t_recid:int, quality:string, bez:string):

    prepare_cache ([L_order])

    l_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order
        nonlocal t_recid, quality, bez

        return {}


    l_order = get_cache (L_order, {"_recid": [(eq, t_recid)]})
    l_order.quality = to_string(substring(quality, 0, 11) , "x(11)") + bez
    pass

    return generate_output()