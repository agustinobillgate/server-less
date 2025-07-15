#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Gl_acct

c_list_data, C_list = create_model("C_list", {"artnr":int, "bezeich":string, "munit":string, "inhalt":string, "zwkum":string, "endkum":int, "qty":Decimal, "qty1":Decimal, "fibukonto":string, "avrg_price":Decimal, "cost_center":string}, {"fibukonto": "0000000000"})

def inv_check_fibukontobl(c_list_data:[C_list]):

    prepare_cache ([Htparam, Gl_acct])

    found_it = False
    p_272:string = ""
    p_275:string = ""
    htparam = gl_acct = None

    c_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal found_it, p_272, p_275, htparam, gl_acct


        nonlocal c_list

        return {"found_it": found_it}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 272)]})

    if htparam:
        p_272 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 275)]})

    if htparam:
        p_275 = htparam.fchar

    for c_list in query(c_list_data, filters=(lambda c_list: c_list.fibukonto.lower()  != ("0000000000").lower())):

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)],"acc_type": [(eq, 2)]})

        if gl_acct:

            if gl_acct.fibukonto.lower()  != (p_272).lower()  and gl_acct.fibukonto.lower()  != (p_275).lower() :
                found_it = True


                break

    return generate_output()