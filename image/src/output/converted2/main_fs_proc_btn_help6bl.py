#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Zwkum

def main_fs_proc_btn_help6bl(text_p2_1:string):

    prepare_cache ([Htparam, Zwkum])

    b_dept_finteger = 0
    zwkum_zknr = 0
    htparam = zwkum = None

    b_dept = None

    B_dept = create_buffer("B_dept",Htparam)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_dept_finteger, zwkum_zknr, htparam, zwkum
        nonlocal text_p2_1
        nonlocal b_dept


        nonlocal b_dept

        return {"b_dept_finteger": b_dept_finteger, "zwkum_zknr": zwkum_zknr}


    b_dept = get_cache (Htparam, {"paramnr": [(eq, 900)]})

    zwkum = get_cache (Zwkum, {"departement": [(eq, b_dept.finteger)],"bezeich": [(eq, text_p2_1)]})
    b_dept_finteger = b_dept.finteger
    zwkum_zknr = zwkum.zknr

    return generate_output()