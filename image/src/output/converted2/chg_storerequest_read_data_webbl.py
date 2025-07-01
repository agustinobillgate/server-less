#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Bediener, Parameters, L_lager, L_artikel, L_bestand, Gl_acct, Queasy

payload_list_list, Payload_list = create_model("Payload_list", {"t_lschein":string, "t_datum":string, "t_amount":Decimal, "lscheinnr":string})

def chg_storerequest_read_data_webbl(payload_list_list:[Payload_list]):

    prepare_cache ([Bediener, Parameters, L_lager, L_artikel, L_bestand, Gl_acct, Queasy])

    t_lschein:string = ""
    t_datum:date = None
    t_amount:Decimal = to_decimal("0.0")
    lscheinnr:string = ""
    curr_lager:int = 0
    deptno:int = 0
    transfered:bool = False
    out_type:int = 0
    to_stock:int = 0
    deptname:string = ""
    lager_bezeich:string = ""
    lager_bez1:string = ""
    curr_pos:int = 0
    sr_remark:string = ""
    op_list_list = []
    response_list_list = []
    l_op = bediener = parameters = l_lager = l_artikel = l_bestand = gl_acct = queasy = None

    op_list = payload_list = response_list = sys_user = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "anzahl0":Decimal, "fibu":string, "fibu10":string, "s_recid":int, "einheit":string})
    response_list_list, Response_list = create_model("Response_list", {"t_amount":Decimal, "lscheinnr":string, "curr_lager":int, "deptno":int, "transfered":bool, "out_type":int, "to_stock":int, "deptname":string, "lager_bezeich":string, "lager_bez1":string, "curr_pos":int, "sr_remark":string})

    Sys_user = create_buffer("Sys_user",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_lschein, t_datum, t_amount, lscheinnr, curr_lager, deptno, transfered, out_type, to_stock, deptname, lager_bezeich, lager_bez1, curr_pos, sr_remark, op_list_list, response_list_list, l_op, bediener, parameters, l_lager, l_artikel, l_bestand, gl_acct, queasy
        nonlocal sys_user


        nonlocal op_list, payload_list, response_list, sys_user
        nonlocal op_list_list, response_list_list

        return {"op-list": op_list_list, "response-list": response_list_list}

    def read_data():

        nonlocal t_lschein, t_datum, t_amount, lscheinnr, curr_lager, deptno, transfered, out_type, to_stock, deptname, lager_bezeich, lager_bez1, curr_pos, sr_remark, op_list_list, response_list_list, l_op, bediener, parameters, l_lager, l_artikel, l_bestand, gl_acct, queasy
        nonlocal sys_user


        nonlocal op_list, payload_list, response_list, sys_user
        nonlocal op_list_list, response_list_list


        lscheinnr = t_lschein

        l_op = get_cache (L_op, {"datum": [(eq, t_datum)],"lscheinnr": [(eq, t_lschein)],"pos": [(gt, 0)]})

        if l_op:
            curr_lager = l_op.lager_nr
            deptno = l_op.reorgflag

            parameters = db_session.query(Parameters).filter(
                     (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == deptno)).first()

            if parameters:
                deptname = parameters.vstring

            if l_op.op_art == 14:
                transfered = True
                out_type = 1
                to_stock = l_op.pos


            else:
                out_type = 2

            l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_lager)]})

            if l_lager:
                lager_bezeich = l_lager.bezeich

            if to_stock != 0:

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, to_stock)]})

                if l_lager:
                    lager_bez1 = l_lager.bezeich

            for l_op in db_session.query(L_op).filter(
                     (L_op.datum == t_datum) & (L_op.lscheinnr == (t_lschein).lower()) & (L_op.pos > 0) & (L_op.loeschflag == 0)).order_by(L_op.pos).all():
                op_list = Op_list()
                op_list_list.append(op_list)

                buffer_copy(l_op, op_list)

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})

                if l_artikel:
                    op_list.bezeich = l_artikel.bezeich
                    op_list.einheit = l_artikel.masseinheit

                sys_user = get_cache (Bediener, {"nr": [(eq, l_op.fuellflag)]})

                if sys_user:
                    op_list.username = sys_user.username

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, curr_lager)]})
                op_list.s_recid = to_int(l_op._recid)
                op_list.anzahl0 =  to_decimal(l_op.anzahl)
                op_list.fibu = l_op.stornogrund
                op_list.fibu10 = l_op.stornogrund
                curr_pos = l_op.pos
                t_amount =  to_decimal(t_amount) + to_decimal(l_op.warenwert)

                if l_bestand:
                    op_list.onhand =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                if not gl_acct:

                    gl_acct = get_cache (Gl_acct, {"bezeich": [(eq, l_op.stornogrund)]})

                if gl_acct:
                    op_list.fibu = gl_acct.fibukonto
                    op_list.fibu10 = gl_acct.fibukonto
                    op_list.stornogrund = gl_acct.bezeich

            queasy = get_cache (Queasy, {"key": [(eq, 343)],"char1": [(eq, t_lschein)]})

            if queasy:
                sr_remark = queasy.char2


    payload_list = query(payload_list_list, first=True)

    if payload_list:
        t_lschein = payload_list.t_lschein
        t_amount =  to_decimal(payload_list.t_amount)
        lscheinnr = payload_list.lscheinnr


        t_datum = date_mdy(to_int(substring(payload_list.t_datum, 0, 2)) , to_int(substring(payload_list.t_datum, 3, 2)) , 2000 + timedelta(days=to_int(substring(payload_list.t_datum, 6, 2))))
        read_data()
        response_list = Response_list()
        response_list_list.append(response_list)

        response_list.t_amount =  to_decimal(t_amount)
        response_list.lscheinnr = lscheinnr
        response_list.curr_lager = curr_lager
        response_list.deptno = deptno
        response_list.transfered = transfered
        response_list.out_type = out_type
        response_list.to_stock = to_stock
        response_list.deptname = deptname
        response_list.lager_bezeich = lager_bezeich
        response_list.lager_bez1 = lager_bez1
        response_list.curr_pos = curr_pos
        response_list.sr_remark = sr_remark

    return generate_output()