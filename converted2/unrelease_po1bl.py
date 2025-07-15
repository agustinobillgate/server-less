#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr

def unrelease_po1bl(docu_nr:string):

    prepare_cache ([L_orderhdr])

    l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr
        nonlocal docu_nr

        return {}


    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})
    pass
    l_orderhdr.gedruckt = None


    pass

    return generate_output()