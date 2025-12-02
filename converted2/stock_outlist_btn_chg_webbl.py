#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, L_op, Gl_department, L_ophdr

str_list_data, Str_list = create_model("Str_list", {"billdate":date, "fibu":string, "other_fibu":bool, "op_recid":int, "lscheinnr":string, "s":string, "id":string, "gl_dept":string})

def stock_outlist_btn_chg_webbl(str_list_data:[Str_list], cost_acct:string, op_recid:int):

    prepare_cache ([Gl_acct, L_op, Gl_department, L_ophdr])

    fl_code = 0
    t_fibu = ""
    t_s = ""
    gl_acct = l_op = gl_department = l_ophdr = None

    str_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, t_fibu, t_s, gl_acct, l_op, gl_department, l_ophdr
        nonlocal cost_acct, op_recid


        nonlocal str_list

        return {"str-list": str_list_data, "fl_code": fl_code, "t_fibu": t_fibu, "t_s": t_s}

    str_list = query(str_list_data, filters=(lambda str_list: str_list.op_recid == op_recid), first=True)

    if str_list:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

        if gl_acct and gl_acct.fibukonto != str_list.fibu:

            if str_list.other_fibu:

                l_op = get_cache (L_op, {"_recid": [(eq, str_list.op_recid)]})

                if l_op:
                    pass
                    l_op.stornogrund = gl_acct.fibukonto

                    gl_department = get_cache (Gl_department, {"nr": [(eq, gl_acct.deptnr)]})

                    if gl_department:
                        str_list.gl_dept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                    pass
                    pass
                t_fibu = cost_acct
                t_s = substring(str_list.s, 0, 8) + to_string(gl_acct.bezeich, "x(30)") + substring(str_list.s, 38, length(str_list.s))
                fl_code = 1
            else:

                l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, str_list.lscheinnr)],"op_typ": [(eq, "stt")]})

                if l_ophdr:

                    for str_list in query(str_list_data, filters=(lambda str_list: str_list.lscheinnr == l_ophdr.lscheinnr)):

                        if not str_list.other_fibu:
                            str_list.s = substring(str_list.s, 0, 8) + to_string(gl_acct.bezeich, "x(30)") + substring(str_list.s, 38, length(str_list.s))

                        gl_department = get_cache (Gl_department, {"nr": [(eq, gl_acct.deptnr)]})

                        if gl_department:
                            str_list.gl_dept = to_string(gl_department.nr) + " - " + gl_department.bezeich
                        t_fibu = cost_acct
                        str_list.fibu = cost_acct
                    pass
                    l_ophdr.fibukonto = gl_acct.fibukonto
                    pass
                    pass

    return generate_output()