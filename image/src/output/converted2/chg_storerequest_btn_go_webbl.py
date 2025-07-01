#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Bediener, Gl_acct, Parameters, L_ophdr, Queasy

payload_list_list, Payload_list = create_model("Payload_list", {"s_recid":int, "user_init":string, "t_lschein":string, "release_flag":bool, "transfered":bool, "show_price":bool, "sr_remark":string})
op_list_list, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "anzahl0":Decimal, "fibu":string, "fibu10":string, "s_recid":int, "einheit":string})

def chg_storerequest_btn_go_webbl(payload_list_list:[Payload_list], op_list_list:[Op_list]):

    prepare_cache ([L_op, Bediener, Gl_acct, L_ophdr, Queasy])

    response_list_list = []
    s_recid:int = 0
    user_init:string = ""
    t_lschein:string = ""
    release_flag:bool = False
    transfered:bool = False
    show_price:bool = False
    sr_remark:string = ""
    changed:bool = False
    approved:bool = False
    flag:int = 0
    transfer_date:date = None
    l_op = bediener = gl_acct = parameters = l_ophdr = queasy = None

    op_list = payload_list = response_list = None

    response_list_list, Response_list = create_model("Response_list", {"s_recid":int, "changed":bool, "approved":bool, "flag":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal response_list_list, s_recid, user_init, t_lschein, release_flag, transfered, show_price, sr_remark, changed, approved, flag, transfer_date, l_op, bediener, gl_acct, parameters, l_ophdr, queasy


        nonlocal op_list, payload_list, response_list
        nonlocal response_list_list

        return {"response-list": response_list_list}

    payload_list = query(payload_list_list, first=True)

    if payload_list:
        s_recid = payload_list.s_recid
        user_init = payload_list.user_init
        t_lschein = payload_list.t_lschein
        release_flag = payload_list.release_flag
        transfered = payload_list.transfered
        show_price = payload_list.show_price
        sr_remark = payload_list.sr_remark

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if not transfered and show_price:

            op_list = query(op_list_list, first=True)
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

                op_list = query(op_list_list, next=True)

        elif not transfered and not show_price:

            op_list = query(op_list_list, first=True)
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

                op_list = query(op_list_list, next=True)

        for op_list in query(op_list_list, filters=(lambda op_list: op_list.anzahl != op_list.anzahl0 or op_list.fibu != op_list.fibu10)):

            l_op = get_cache (L_op, {"_recid": [(eq, op_list.s_recid)]})

            if l_op:
                pass
                l_op.anzahl =  to_decimal(op_list.anzahl)
                l_op.stornogrund = op_list.fibu
                l_op.warenwert =  to_decimal(op_list.warenwert)
                changed = True

                if bediener:
                    l_op.fuellflag = bediener.nr
                pass
                pass

        l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, t_lschein)]})

        if l_ophdr:
            transfer_date = l_ophdr.datum

        queasy = get_cache (Queasy, {"key": [(eq, 343)],"char1": [(eq, t_lschein)]})

        if queasy:
            pass
            queasy.char2 = sr_remark
            pass
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 343
            queasy.char1 = t_lschein
            queasy.char2 = sr_remark
            queasy.date1 = transfer_date

        if release_flag:

            l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "req")],"lscheinnr": [(eq, t_lschein)],"docu_nr": [(eq, t_lschein)]})

            if l_ophdr:

                if bediener:
                    l_ophdr.betriebsnr = bediener.nr
                pass
                pass
                approved = True
        response_list = Response_list()
        response_list_list.append(response_list)

        response_list.s_recid = s_recid
        response_list.changed = changed
        response_list.approved = approved
        response_list.flag = flag

    return generate_output()