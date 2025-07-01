#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

xls_list_list, Xls_list = create_model("Xls_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "flag":bool, "bezeich":string, "remark":string}, {"fibukonto": "000000000000"})
s_list_list, S_list = create_model("S_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "flag":bool, "bezeich":string, "remark":string}, {"fibukonto": "000000000000"})

def mk_ap_check_importxls_databl(xls_list_list:[Xls_list], s_list_list:[S_list]):

    prepare_cache ([Gl_acct])

    gl_notavail = False
    gl_fibu = ""
    gl_acct = None

    s_list = xls_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_notavail, gl_fibu, gl_acct


        nonlocal s_list, xls_list

        return {"gl_notavail": gl_notavail, "gl_fibu": gl_fibu, "s-list": s_list_list}


    for xls_list in query(xls_list_list):

        if xls_list.fibukonto.lower()  != ("000000000000").lower() :

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, xls_list.fibukonto)]})

            if not gl_acct:
                gl_notavail = True
                gl_fibu = xls_list.fibukonto

                return generate_output()
            xls_list.bezeich = gl_acct.bezeich
    s_list_list.clear()

    for xls_list in query(xls_list_list):
        s_list = S_list()
        s_list_list.append(s_list)

        buffer_copy(xls_list, s_list)

    return generate_output()