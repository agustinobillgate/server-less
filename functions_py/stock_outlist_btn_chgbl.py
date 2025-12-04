#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, L_op, L_ophdr

str_list_data, Str_list = create_model("Str_list", {"billdate":date, "fibu":string, "other_fibu":bool, "op_recid":int, "lscheinnr":string, "s":string, "id":string})

def stock_outlist_btn_chgbl(str_list_data:[Str_list], cost_acct:string, op_recid:int):

    prepare_cache ([Gl_acct, L_op, L_ophdr])

    fl_code = 0
    t_fibu = ""
    t_s = ""
    gl_acct = l_op = l_ophdr = None

    str_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, t_fibu, t_s, gl_acct, l_op, l_ophdr
        nonlocal cost_acct, op_recid


        nonlocal str_list

        return {"str-list": str_list_data, "fl_code": fl_code, "t_fibu": t_fibu, "t_s": t_s}

    str_list = query(str_list_data, filters=(lambda str_list: str_list.op_recid == op_recid), first=True)

    if str_list:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, cost_acct)]})

        if gl_acct and gl_acct.fibukonto != str_list.fibu:

            if str_list.other_fibu:

                l_op = db_session.query(L_op).filter(L_op._recid == str_list.op_recid).first()

                if l_op:
                    db_session.refresh(l_op, with_for_update=True)
                    l_op.stornogrund = gl_acct.fibukonto

                    db_session.flush()

                t_fibu = cost_acct
                t_s = substring(str_list.s, 0, 8) + to_string(gl_acct.bezeich, "x(30)") + substring(str_list.s, 38, length(str_list.s))
                fl_code = 1
            else:

                l_ophdr = db_session.query(L_ophdr).filter((L_ophdr.lscheinnr == str_list.lscheinnr) & (L_ophdr.op_typ == "stt")).with_for_update().first()

                if l_ophdr:

                    for str_list in query(str_list_data, filters=(lambda str_list: str_list.lscheinnr == l_ophdr.lscheinnr)):

                        if not str_list.other_fibu:
                            str_list.s = substring(str_list.s, 0, 8) + to_string(gl_acct.bezeich, "x(30)") + substring(str_list.s, 38, length(str_list.s))

                        str_list.fibu = cost_acct
                        
                    l_ophdr.fibukonto = gl_acct.fibukonto
                    db_session.flush()

    return generate_output()