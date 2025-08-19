#using conversion tools version: 1.0.0.118

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.gcf_history_4blho import gcf_history_4blho # Oscar - skip because using HServer on Progress
from models import History, Htparam

def prepare_gcf_history_centralizedbl(gastnr:int, fdate:date, tdate:date, guest_phone:string, guest_name:string, guest_email:string):

    prepare_cache ([Htparam])

    ghistory_data = []
    summ_list_data = []
    vhost:string = ""
    vservice:string = ""
    hoappparam:string = ""
    lreturn:bool = False
    history = htparam = None

    ghistory = summ_list = None

    ghistory_data, Ghistory = create_model_like(History, {"hname":string, "gname":string, "address":string, "s_recid":int, "vcrnr":string, "mblnr":string, "email":string})
    summ_list_data, Summ_list = create_model_like(History)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ghistory_data, summ_list_data, vhost, vservice, hoappparam, lreturn, history, htparam
        nonlocal gastnr, fdate, tdate, guest_phone, guest_name, guest_email


        nonlocal ghistory, summ_list
        nonlocal ghistory_data, summ_list_data

        return {"ghistory": ghistory_data, "summ-list": summ_list_data}

    def connect_ho():

        nonlocal ghistory_data, summ_list_data, vhost, vservice, hoappparam, lreturn, history, htparam
        nonlocal gastnr, fdate, tdate, guest_phone, guest_name, guest_email


        nonlocal ghistory, summ_list
        nonlocal ghistory_data, summ_list_data

        def generate_inner_output():
            return (ghistory_data, summ_list_data)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 1343)]})

        if htparam:

            if htparam.fchar != "" and htparam.fchar != None:

                if num_entries(htparam.fchar, ":") > 1:
                    vhost = entry(0, htparam.fchar, ":")
                    vservice = entry(1, htparam.fchar, ":")
                    hoappparam = " -H " + vhost + " -S " + vservice + " -DirectConnect -sessionModel Session-free"


        # lreturn = hServerHO:CONNECT (hoappparam, None, None, None) # Oscar - skip because using HServer on Progress
        lreturn = False

        if not lreturn:
            return generate_inner_output()
        
        local_storage.combo_flag = True
        # ghistory_data, summ_list_data = get_output(gcf_history_4blho(gastnr, guest_phone, guest_name, guest_email, fdate, tdate)) # Oscar - skip because using HServer on Progress
        local_storage.combo_flag = False

        # lreturn = hServerHO:DISCONNECT() # Oscar - skip because using HServer on Progress
        lreturn = False


        return generate_inner_output()


    ghistory_data, summ_list_data = connect_ho()

    return generate_output()