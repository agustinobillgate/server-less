#using conversion tools version: 1.0.0.61

from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_op, Bediener, Gl_acct, Parameters, L_ophdr

op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str, "onhand":decimal, "anzahl0":decimal, "fibu":str, "fibu10":str, "s_recid":int, "einheit":str})

def chg_storerequest_btn_gobl (1)(op_list_list:[Op_list], s_recid:int, user_init:str, t_lschein:str, release_flag:bool, transfered:bool, show_price:bool):
    changed = False
    approved = False
    flag = 0
    l_op = bediener = gl_acct = parameters = l_ophdr = None

    op_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal changed, approved, flag, l_op, bediener, gl_acct, parameters, l_ophdr
        nonlocal s_recid, user_init, t_lschein, release_flag, transfered, show_price


        nonlocal op_list

        return {"s_recid": s_recid, "changed": changed, "approved": approved, "flag": flag}

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if not transfered and show_price:

        op_list = query(op_list_list, first=True)
        while None != op_list:

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == op_list.fibu)).first()

            if not gl_acct:
                flag = 1

                return generate_output()

            if gl_acct:

                parameters = db_session.query(Parameters).filter(
                         (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("Alloc").lower()) & (Parameters.varname > "") & (Parameters.vstring == gl_acct.fibukonto)).first()

                if not parameters:
                    flag = 2

                    return generate_output()

            if s_recid == 0:
                s_recid = op_list._recid
            else:

                if op_list._recid == s_recid:
                    break
                else:
                    s_recid = op_list._recid

            op_list = query(op_list_list, next=True)

    elif not transfered and not show_price:

        op_list = query(op_list_list, first=True)
        while None != op_list:

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == op_list.fibu)).first()

            if not gl_acct:
                flag = 1

                return generate_output()

            if gl_acct:

                parameters = db_session.query(Parameters).filter(
                         (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("Alloc").lower()) & (Parameters.varname > "") & (Parameters.vstring == gl_acct.fibukonto)).first()

                if not parameters:
                    flag = 2

                    return generate_output()

            if s_recid == 0:
                s_recid = op_list._recid
            else:

                if op_list._recid == s_recid:
                    break
                else:
                    s_recid = op_list._recid

            op_list = query(op_list_list, next=True)

    for op_list in query(op_list_list, filters=(lambda op_list: op_list.anzahl != op_list.anzahl0 or op_list.fibu != op_list.fibu10)):

        l_op = db_session.query(L_op).filter(
                 (L_op._recid == op_list.s_recid)).first()

        if l_op:
            l_op.anzahl =  to_decimal(op_list.anzahl)
            l_op.stornogrund = op_list.fibu
            l_op.fuellflag = bediener.nr
            l_op.warenwert =  to_decimal(op_list.warenwert)
            changed = True


            pass
            pass

    if release_flag:

        l_ophdr = db_session.query(L_ophdr).filter(
                 (func.lower(L_ophdr.op_typ) == ("REQ").lower()) & (func.lower(L_ophdr.lscheinnr) == (t_lschein).lower()) & (func.lower(L_ophdr.docu_nr) == (t_lschein).lower())).first()

        if l_ophdr:
            l_ophdr.betriebsnr = bediener.nr


            pass
            pass
            approved = True

    return generate_output()