#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, Bediener, Gl_acct, Parameters, L_ophdr

op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "anzahl0":Decimal, "fibu":string, "fibu10":string, "s_recid":int, "einheit":string})

def chg_storerequest_btn_gobl(op_list_data:[Op_list], s_recid:int, user_init:string, t_lschein:string, release_flag:bool, transfered:bool, show_price:bool):

    prepare_cache ([L_op, Bediener, Gl_acct, L_ophdr])

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

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if not transfered and show_price:

        op_list = query(op_list_data, first=True)
        while None != op_list:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, op_list.fibu)]})

            if not gl_acct:
                flag = 1

                return generate_output()

            if gl_acct:

                parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(gt, "")],"vstring": [(eq, gl_acct.fibukonto)]})

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

            op_list = query(op_list_data, next=True)

    elif not transfered and not show_price:

        op_list = query(op_list_data, first=True)
        while None != op_list:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, op_list.fibu)]})

            if not gl_acct:
                flag = 1

                return generate_output()

            if gl_acct:

                parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"varname": [(gt, "")],"vstring": [(eq, gl_acct.fibukonto)]})

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

            op_list = query(op_list_data, next=True)

    for op_list in query(op_list_data, filters=(lambda op_list: op_list.anzahl != op_list.anzahl0 or op_list.fibu != op_list.fibu10)):

        l_op = get_cache (L_op, {"_recid": [(eq, op_list.s_recid)]})

        if l_op:
            pass
            l_op.anzahl =  to_decimal(op_list.anzahl)
            l_op.stornogrund = op_list.fibu
            l_op.fuellflag = bediener.nr
            l_op.warenwert =  to_decimal(op_list.warenwert)
            changed = True


            pass
            pass

    if release_flag:

        l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "req")],"lscheinnr": [(eq, t_lschein)],"docu_nr": [(eq, t_lschein)]})

        if l_ophdr:
            l_ophdr.betriebsnr = bediener.nr


            pass
            pass
            approved = True

    return generate_output()