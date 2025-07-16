#using conversion tools version: 1.0.0.113

from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timedelta
from models import L_op, L_lager, Bediener, Htparam, Parameters, Queasy, L_artikel, L_bestand

payload_list_list, Payload_list = create_model("Payload_list", {"user_init":string, "t_datum":string, "t_lschein":string})

def prepare_ins_storerequest_webbl(payload_list_list:[Payload_list]):

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
    op_list_list = []
    response_list_list = []
    l_op = l_lager = bediener = htparam = parameters = queasy = l_artikel = l_bestand = None

    op_list = t_l_lager = sys_user = payload_list = response_list = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "new_flag":bool}, {"new_flag": True})
    t_l_lager_list, T_l_lager = create_model_like(L_lager)
    response_list_list, Response_list = create_model("Response_list", {"deptname":string, "curr_lager":int, "deptno":int, "show_price":bool, "req_flag":bool, "p_220":int, "out_type":int, "transfered":bool, "to_stock":int, "lager_bezeich":string, "lager_bez1":string, "curr_pos":int, "t_amount":Decimal, "lscheinnr":string, "sr_remark":string}, {"out_type": 1})

    Sys_user = create_buffer("Sys_user",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_init, t_datum, t_lschein, deptname, curr_lager, deptno, show_price, req_flag, p_220, out_type, transfered, to_stock, lager_bezeich, lager_bez1, curr_pos, t_amount, lscheinnr, sr_remark, op_list_list, response_list_list, l_op, l_lager, bediener, htparam, parameters, queasy, l_artikel, l_bestand
        nonlocal sys_user


        nonlocal op_list, t_l_lager, sys_user, payload_list, response_list
        nonlocal op_list_list, t_l_lager_list, response_list_list

        return {"op-list": op_list_list, "response-list": response_list_list}

    def read_data():

        # ... (rest of the read_data function remains unchanged)

    # ... (rest of the code before the problematic line remains unchanged)

    if payload_list:
        user_init = payload_list.user_init
        t_lschein = payload_list.t_lschein

        base_year = date(2000, 1, 1)  # Create a date object for the base year
        days_to_add = to_int(substring(payload_list.t_datum, 6, 2))
        t_datum = date_mdy(to_int(substring(payload_list.t_datum, 0, 2)), to_int(substring(payload_list.t_datum, 3, 2)), base_year + timedelta(days=days_to_add))
        read_data()
        response_list = Response_list()
        response_list_list.append(response_list)

        # ... (rest of the code remains unchanged)

    return generate_output()
