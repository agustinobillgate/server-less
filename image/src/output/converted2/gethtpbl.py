#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def gethtpbl(casetype:int, inp_param:int):

    prepare_cache ([Htparam])

    flogical = False
    fdate = None
    fchar = ""
    fint = 0
    fdec = to_decimal("0.0")
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flogical, fdate, fchar, fint, fdec, htparam
        nonlocal casetype, inp_param

        return {"flogical": flogical, "fdate": fdate, "fchar": fchar, "fint": fint, "fdec": fdec}


    if casetype == 1:
        flogical = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, inp_param)]})

        if htparam:
            flogical = htparam.flogical
    elif casetype == 2:
        fdate = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, inp_param)]})

        if htparam:
            fdate = htparam.fdate
    elif casetype == 3:
        fchar = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, inp_param)]})

        if htparam:
            fchar = htparam.fchar
    elif casetype == 4:
        fint = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, inp_param)]})

        if htparam:
            fint = htparam.finteger
    elif casetype == 5:
        fdec =  to_decimal(None)

        htparam = get_cache (Htparam, {"paramnr": [(eq, inp_param)]})

        if htparam:
            fdec =  to_decimal(htparam.fdecimal)

    return generate_output()