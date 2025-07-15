#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Htparam, L_ophdr, Bediener, Res_history

payload_list_data, Payload_list = create_model("Payload_list", {"user_init":string, "reason":string, "lscheinnr":string})

def storereq_list_unapprove_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([L_op, Htparam, L_ophdr, Bediener, Res_history])

    response_list_data = []
    user_init:string = ""
    reason:string = ""
    lscheinnr:string = ""
    success_status:bool = True
    msg_str:string = ""
    log_msg:string = ""
    l_op = htparam = l_ophdr = bediener = res_history = None

    payload_list = response_list = None

    response_list_data, Response_list = create_model("Response_list", {"success_status":bool, "msg_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal response_list_data, user_init, reason, lscheinnr, success_status, msg_str, log_msg, l_op, htparam, l_ophdr, bediener, res_history


        nonlocal payload_list, response_list
        nonlocal response_list_data

        return {"response-list": response_list_data}

    def unapprove_sr():

        nonlocal response_list_data, user_init, reason, lscheinnr, success_status, msg_str, log_msg, l_op, htparam, l_ophdr, bediener, res_history


        nonlocal payload_list, response_list
        nonlocal response_list_data

        close_date:date = None
        close_date2:date = None
        b_l_op = None
        B_l_op =  create_buffer("B_l_op",L_op)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})

        if htparam:
            close_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})

        if htparam:
            close_date2 = htparam.fdate

        if close_date < close_date2:
            close_date = close_date2
        close_date = date_mdy(get_month(close_date) , 1, get_year(close_date)) - timedelta(days=1)

        l_op = get_cache (L_op, {"lscheinnr": [(eq, lscheinnr)],"op_art": [(ge, 13),(le, 14)]})

        if l_op:

            b_l_op = get_cache (L_op, {"lscheinnr": [(eq, lscheinnr)],"op_art": [(ge, 3),(le, 4)],"herkunftflag": [(le, 2)]})

            if l_op.datum <= close_date:
                success_status = False
                msg_str = "Failed to unapprove SR because SR created before close inventory date. Last close inventory: " + to_string(close_date)

            elif l_op.loeschflag == 2:
                success_status = False
                msg_str = "Failed to unapprove SR because SR was deleted"

            elif b_l_op or l_op.herkunftflag == 2:
                success_status = False
                msg_str = "Failed to unapprove SR because SR already marked as outgoing"
            else:

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "req")],"lscheinnr": [(eq, l_op.lscheinnr)],"docu_nr": [(eq, l_op.lscheinnr)]})

                if l_ophdr:
                    l_ophdr.betriebsnr = 0
                    pass
                    pass
                log_msg = "SR with Request Code: " + to_string(lscheinnr) + " is unapproved. reason: " + reason

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Unapprove SR"
                    res_history.aenderung = log_msg

    payload_list = query(payload_list_data, first=True)

    if payload_list:
        user_init = payload_list.user_init
        reason = payload_list.reason
        lscheinnr = payload_list.lscheinnr


        unapprove_sr()
        response_list = Response_list()
        response_list_data.append(response_list)

        response_list.success_status = success_status
        response_list.msg_str = msg_str

    return generate_output()