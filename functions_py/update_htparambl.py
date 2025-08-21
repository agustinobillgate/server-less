#using conversion tools version: 1.0.0.117

#------------------------------------------------
# Rulita, 19/08/2025
# New Compile program Update htparam hit from IF
# ticket: 6C8C53
#------------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def update_htparambl(htparamnum:int, case_type:int, param_int:int, param_deci:Decimal, param_char:string, param_logi:bool):

    prepare_cache ([Htparam])

    htpfint = 0
    htpfdeci = to_decimal("0.0")
    htpfchar = ""
    htpflogical = False
    htparam = None

    b_htpar = None

    B_htpar = create_buffer("B_htpar",Htparam)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpfint, htpfdeci, htpfchar, htpflogical, htparam
        nonlocal htparamnum, case_type, param_int, param_deci, param_char, param_logi
        nonlocal b_htpar


        nonlocal b_htpar

        return {"htpfint": htpfint, "htpfdeci": htpfdeci, "htpfchar": htpfchar, "htpflogical": htpflogical}

    htpfint = 0
    htpfdeci =  to_decimal("0")
    htpfchar = ""
    htpflogical = False

    if case_type == 1:

        htparam = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

        if htparam:
            pass
            htparam.finteger = param_int


            pass
            pass

        b_htpar = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

        if b_htpar:
            htpfint = b_htpar.fint

    elif case_type == 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

        if htparam:
            pass
            htparam.fdecimal =  to_decimal(param_deci)


            pass
            pass

        b_htpar = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

        if b_htpar:
            htpfdeci =  to_decimal(b_htpar.fdeci)

    elif case_type == 3:

        htparam = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

        if htparam:
            pass
            htparam.fchar = param_char


            pass
            pass

        b_htpar = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

        if b_htpar:
            htpfchar = b_htpar.fchar

    elif case_type == 4:

        htparam = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

        if htparam:
            pass
            htparam.flogical = param_logi


            pass
            pass

        b_htpar = get_cache (Htparam, {"paramnr": [(eq, htparamnum)]})

        if b_htpar:
            htpflogical = htparam.flogical

    return generate_output()