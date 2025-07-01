#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def s_storerequest_entry_lscheinnrbl(recid_l_ophdr:int, lscheinnr:string):

    prepare_cache ([L_ophdr])

    l_ophdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_ophdr
        nonlocal recid_l_ophdr, lscheinnr

        return {}


    l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, recid_l_ophdr)]})
    pass
    l_ophdr.docu_nr = lscheinnr
    l_ophdr.lscheinnr = lscheinnr
    pass

    return generate_output()