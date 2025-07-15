#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr

def unrelease_pobl(docu_nr:string):

    prepare_cache ([L_orderhdr])

    flag = 0
    l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_orderhdr
        nonlocal docu_nr

        return {"flag": flag}


    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})

    if not l_orderhdr:
        flag = 1

        return generate_output()
    else:

        if l_orderhdr.gedruckt == None:
            flag = 2

            return generate_output()
        else:
            flag = 3

            return generate_output()

    return generate_output()