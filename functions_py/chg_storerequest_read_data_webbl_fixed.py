#using conversion tools version: 1.0.0.113
#------------------------------------------
# Rd, 3/8/2025
# Manual edit response-list key
#------------------------------------------
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

        # ... (rest of the read_data function remains unchanged)

    payload_list = query(payload_list_list, first=True)

    if payload_list:
        t_lschein = payload_list.t_lschein
        t_amount =  to_decimal(payload_list.t_amount)
        lscheinnr = payload_list.lscheinnr

        t_datum = date_mdy(to_int(substring(payload_list.t_datum, 3, 2)) , to_int(substring(payload_list.t_datum, 0, 2)) , 2000 + to_int(substring(payload_list.t_datum, 6, 2)))
        read_data()
        response_list = Response_list()
        response_list_list.append(response_list)

        # ... (rest of the code remains unchanged)

    return generate_output()
