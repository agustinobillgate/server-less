#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_lager, Bediener, Htparam, Parameters, Queasy, L_artikel, L_bestand

payload_list_data, Payload_list = create_model("Payload_list", {"user_init":string, "t_datum":string, "t_lschein":string})

def prepare_ins_storerequest_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([L_lager, Bediener, Htparam, Parameters, Queasy, L_artikel, L_bestand])

    user_init:string = ""
    t_datum:date = None
    t_lschein:string = ""
    deptname:string = ""
    curr_lager:int = 0
    deptno:int = 0
    show_price:bool = False
    req_flag:bool = False
    p_220:int = 0
    out_type:int = 1
    transfered:bool = False
    to_stock:int = 0
    lager_bezeich:string = ""
    lager_bez1:string = ""
    curr_pos:int = 0
    t_amount:Decimal = to_decimal("0.0")
    lscheinnr:string = ""
    sr_remark:string = ""
    op_list_data = []
    response_list_data = []
    l_op = l_lager = bediener = htparam = parameters = queasy = l_artikel = l_bestand = None

    op_list = t_l_lager = sys_user = payload_list = response_list = None

    op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "new_flag":bool}, {"new_flag": True})
    t_l_lager_data, T_l_lager = create_model_like(L_lager)
    response_list_data, Response_list = create_model("Response_list", {"deptname":string, "curr_lager":int, "deptno":int, "show_price":bool, "req_flag":bool, "p_220":int, "out_type":int, "transfered":bool, "to_stock":int, "lager_bezeich":string, "lager_bez1":string, "curr_pos":int, "t_amount":Decimal, "lscheinnr":string, "sr_remark":string}, {"out_type": 1})

    Sys_user = create_buffer("Sys_user",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_init, t_datum, t_lschein, deptname, curr_lager, deptno, show_price, req_flag, p_220, out_type, transfered, to_stock, lager_bezeich, lager_bez1, curr_pos, t_amount, lscheinnr, sr_remark, op_list_data, response_list_data, l_op, l_lager, bediener, htparam, parameters, queasy, l_artikel, l_bestand
        nonlocal sys_user


        nonlocal op_list, t_l_lager, sys_user, payload_list, response_list
        nonlocal op_list_data, t_l_lager_data, response_list_data

        return {"op-list": op_list_data, "response-list": response_list_data}

    def read_data():

        nonlocal user_init, t_datum, t_lschein, deptname, curr_lager, deptno, show_price, req_flag, p_220, out_type, transfered, to_stock, lager_bezeich, lager_bez1, curr_pos, t_amount, lscheinnr, sr_remark, op_list_data, response_list_data, l_op, l_lager, bediener, htparam, parameters, queasy, l_artikel, l_bestand
        nonlocal sys_user


        nonlocal op_list, t_l_lager, sys_user, payload_list, response_list
        nonlocal op_list_data, t_l_lager_data, response_list_data


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

            queasy = get_cache (Queasy, {"key": [(eq, 343)],"char1": [(eq, t_lschein)]})

            if queasy:
                sr_remark = queasy.char2

            for l_op in db_session.query(L_op).filter(
                     (L_op.datum == t_datum) & (L_op.lscheinnr == (t_lschein).lower()) & (L_op.pos > 0) & (L_op.loeschflag <= 1)).order_by(L_op.pos).all():
                op_list = Op_list()
                op_list_data.append(op_list)

                buffer_copy(l_op, op_list)

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})

                sys_user = get_cache (Bediener, {"nr": [(eq, l_op.fuellflag)]})

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, curr_lager)]})

                if sys_user:
                    op_list.username = sys_user.username

                if l_artikel:
                    op_list.bezeich = l_artikel.bezeich
                op_list.new_flag = False
                curr_pos = l_op.pos
                t_amount =  to_decimal(t_amount) + to_decimal(l_op.warenwert)

                if l_bestand:
                    op_list.onhand =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:

        if substring(bediener.permissions, 21, 1) != ("0").lower() :
            show_price = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})

    if htparam:
        show_price = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 475)]})

    if htparam:
        req_flag = not htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 220)]})

    if htparam:
        p_220 = htparam.finteger

    payload_list = query(payload_list_data, first=True)

    if payload_list:
        user_init = payload_list.user_init
        t_lschein = payload_list.t_lschein


        # t_datum = date_mdy(to_int(substring(payload_list.t_datum, 0, 2)) , to_int(substring(payload_list.t_datum, 3, 2)) , 2000 + timedelta(days=to_int(substring(payload_list.t_datum, 6, 2))))
        base_year = 2000
        month = to_int(substring(payload_list.t_datum, 0, 2))
        day = to_int(substring(payload_list.t_datum, 3, 2))
        year_offset = to_int(substring(payload_list.t_datum, 6, 2))

        final_date = date(base_year, 1, 1) + timedelta(days=year_offset)
        t_datum = date_mdy(month, day, final_date.year)
        
        read_data()
        response_list = Response_list()
        response_list_data.append(response_list)

        response_list.deptname = deptname
        response_list.curr_lager = curr_lager
        response_list.deptno = deptno
        response_list.show_price = show_price
        response_list.req_flag = req_flag
        response_list.p_220 = p_220
        response_list.out_type = out_type
        response_list.transfered = transfered
        response_list.to_stock = to_stock
        response_list.lager_bezeich = lager_bezeich
        response_list.lager_bez1 = lager_bez1
        response_list.curr_pos = curr_pos
        response_list.t_amount =  to_decimal(t_amount)
        response_list.lscheinnr = lscheinnr
        response_list.sr_remark = sr_remark

    return generate_output()