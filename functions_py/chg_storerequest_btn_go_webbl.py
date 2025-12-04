#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Bediener, Gl_acct, Parameters, L_ophdr, Queasy

payload_list_data, Payload_list = create_model("Payload_list", {"s_recid":int, "user_init":string, "t_lschein":string, "release_flag":bool, "transfered":bool, "show_price":bool, "sr_remark":string})
op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "anzahl0":Decimal, "fibu":string, "fibu10":string, "s_recid":int, "einheit":string})

def chg_storerequest_btn_go_webbl(payload_list_data:[Payload_list], op_list_data:[Op_list]):

    prepare_cache ([L_op, Bediener, Gl_acct, L_ophdr, Queasy])

    response_list_data = []
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

    response_list_data, Response_list = create_model("Response_list", {"s_recid":int, "changed":bool, "approved":bool, "flag":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal response_list_data, s_recid, user_init, t_lschein, release_flag, transfered, show_price, sr_remark, changed, approved, flag, transfer_date, l_op, bediener, gl_acct, parameters, l_ophdr, queasy


        nonlocal op_list, payload_list, response_list
        nonlocal response_list_data

        return {"response-list": response_list_data}

    payload_list = query(payload_list_data, first=True)

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

            l_op = db_session.query(L_op).filter(L_op._recid == op_list.s_recid).first()

            if l_op:
                db_session.refresh(l_op, with_for_update=True)

                l_op.anzahl =  to_decimal(op_list.anzahl)
                l_op.stornogrund = op_list.fibu
                l_op.warenwert =  to_decimal(op_list.warenwert)
                changed = True

                if bediener:
                    l_op.fuellflag = bediener.nr

                db_session.flush()

        l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, t_lschein)]})

        if l_ophdr:
            transfer_date = l_ophdr.datum

        queasy = db_session.query(Queasy).filter(Queasy.key == 343, Queasy.char1 == t_lschein).first()

        if queasy:
            db_session.refresh(queasy, with_for_update=True)
            queasy.char2 = sr_remark
            db_session.flush()
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 343
            queasy.char1 = t_lschein
            queasy.char2 = sr_remark
            queasy.date1 = transfer_date

        if release_flag:

            l_ophdr = db_session.query(L_ophdr).filter(
                     (L_ophdr.op_typ == "req") & (L_ophdr.lscheinnr == t_lschein) & (L_ophdr.docu_nr == t_lschein)).with_for_update().first()

            if l_ophdr:

                if bediener:
                    l_ophdr.betriebsnr = bediener.nr

                approved = True

        response_list = Response_list()
        response_list_data.append(response_list)

        response_list.s_recid = s_recid
        response_list.changed = changed
        response_list.approved = approved
        response_list.flag = flag

    return generate_output()