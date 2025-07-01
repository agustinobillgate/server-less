#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

c_list_list, C_list = create_model("C_list", {"artnr":int, "bezeich":string, "munit":string, "inhalt":string, "zwkum":string, "endkum":int, "qty":Decimal, "qty1":Decimal, "fibukonto":string, "avrg_price":Decimal, "cost_center":string}, {"fibukonto": "0000000000"})

def inv_adjustment_chk_fibubl(c_list_list:[C_list]):
    err_code = 0
    gl_acct = None

    c_list = c_list1 = None

    C_list1 = C_list
    c_list1_list = c_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, gl_acct
        nonlocal c_list1


        nonlocal c_list, c_list1

        return {"err_code": err_code}

    for c_list1 in query(c_list1_list, filters=(lambda c_list1: c_list1.qty != c_list1.qty1 and c_list1.fibukonto.lower()  != ("0000000000").lower())):

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list1.fibukonto)]})

        if not gl_acct:
            err_code = 1

            return generate_output()

    return generate_output()