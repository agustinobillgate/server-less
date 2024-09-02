from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.create_lartjob import create_lartjob
from models import Gl_acct, L_op, L_ophdr

def stock_outlist_btn_chgbl(str_list:[Str_list], cost_acct:str, op_recid:int):
    fl_code = 0
    t_fibu = ""
    t_s = ""
    gl_acct = l_op = l_ophdr = None

    str_list = None

    str_list_list, Str_list = create_model("Str_list", {"billdate":date, "fibu":str, "other_fibu":bool, "op_recid":int, "lscheinnr":str, "s":str, "id":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, t_fibu, t_s, gl_acct, l_op, l_ophdr


        nonlocal str_list
        nonlocal str_list_list
        return {"fl_code": fl_code, "t_fibu": t_fibu, "t_s": t_s}

    str_list = query(str_list_list, filters=(lambda str_list :str_list.op_recid == op_recid), first=True)

    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

    if gl_acct and gl_acct.fibukonto != str_list.fibu:

        if str_list.other_fibu:

            l_op = db_session.query(L_op).filter(
                    (L_op._recid == str_list.op_recid)).first()
            l_op.stornogrund = gl_acct.fibukonto

            l_op = db_session.query(L_op).first()
            t_fibu = cost_acct
            t_s = substring(str_list.s, 0, 8) + to_string(gl_acct.bezeich, "x(30)") + substring(str_list.s, 38, len(str_list.s))
            fl_code = 1
    else:

        l_ophdr = db_session.query(L_ophdr).filter(
                (L_ophdr.lscheinnr == str_list.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT")).first()

        if l_ophdr:

            for str_list in query(str_list_list, filters=(lambda str_list :str_list.lscheinnr == l_ophdr.lscheinnr)):

                if not str_list.other_fibu:
                    str_list.s = substring(str_list.s, 0, 8) + to_string(gl_acct.bezeich, "x(30)") + substring(str_list.s, 38, len(str_list.s))
                str_list.fibu = cost_acct

                if l_ophdr.betriebsnr != 0:

                    l_op = db_session.query(L_op).filter(
                            (L_op._recid == str_list.op_recid)).first()

                    if l_op:
                        get_output(create_lartjob(l_ophdr._recid, l_op.artnr, - l_op.anzahl, - l_op.warenwert, l_op.datum, False))
            l_ophdr.fibukonto = gl_acct.fibukonto

            if l_ophdr.betriebsnr != 0:

                for str_list in query(str_list_list, filters=(lambda str_list :str_list.lscheinnr == l_ophdr.lscheinnr)):

                    l_op = db_session.query(L_op).filter(
                            (L_op._recid == str_list.op_recid)).first()

                    if l_op:
                        get_output(create_lartjob(l_ophdr._recid, l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.datum, False))

            l_ophdr = db_session.query(L_ophdr).first()

    return generate_output()