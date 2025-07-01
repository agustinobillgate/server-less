#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters, Gl_acct

def search_cost_center_webbl(account_no:string):

    prepare_cache ([Parameters, Gl_acct])

    vsuccess = False
    result_msg = ""
    out_list_list = []
    varcode:string = ""
    parameters = gl_acct = None

    out_list = None

    out_list_list, Out_list = create_model("Out_list", {"fibu":string, "fibu_desc":string, "costcenter_no":int, "costcenter_name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal vsuccess, result_msg, out_list_list, varcode, parameters, gl_acct
        nonlocal account_no


        nonlocal out_list
        nonlocal out_list_list

        return {"vsuccess": vsuccess, "result_msg": result_msg, "out-list": out_list_list}


    out_list_list.clear()

    parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(gt, "")],"vstring": [(eq, account_no)]})

    if not parameters:
        result_msg = "Account Number not found."

        return generate_output()
    varcode = parameters.varname
    out_list = Out_list()
    out_list_list.append(out_list)

    out_list.fibu = parameters.vstring

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, parameters.vstring)]})

    if gl_acct:
        out_list.fibu_desc = gl_acct.bezeich

    parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "name")],"varname": [(eq, varcode)]})

    if parameters:
        out_list.costcenter_no = to_int(parameters.varname)
        out_list.costcenter_name = parameters.vstring

    out_list = query(out_list_list, first=True)

    if out_list:
        result_msg = "Account found in Cost Center Code: " + to_string(out_list.costcenter_no) + chr_unicode(10) + out_list.fibu + " - " + out_list.fibu_desc
        vsuccess = True

    return generate_output()