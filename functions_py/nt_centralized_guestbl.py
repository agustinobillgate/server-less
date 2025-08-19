#using conversion tools version: 1.0.0.118

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
# from functions.nt_shareguest_profileblho import nt_shareguest_profileblho # Oscar - skip because using HServer on Progress
from models import Guest, History, Htparam, Paramtext, Res_line, Res_history

def nt_centralized_guestbl():

    prepare_cache ([Htparam, Paramtext, Res_line, Res_history])

    cidate:date = None
    hoappparam:string = ""
    vhost:string = ""
    vservice:string = ""
    lreturn:bool = False
    min_repeater:int = 0
    hotel_name:string = ""
    guest = history = htparam = paramtext = res_line = res_history = None

    t_guest = t_history = None

    t_guest_data, T_guest = create_model_like(Guest)
    t_history_data, T_history = create_model_like(History)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cidate, hoappparam, vhost, vservice, lreturn, min_repeater, hotel_name, guest, history, htparam, paramtext, res_line, res_history


        nonlocal t_guest, t_history
        nonlocal t_guest_data, t_history_data

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        cidate = htparam.fdate - timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 458)]})

    if htparam:
        min_repeater = htparam.finteger

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

    if paramtext:
        hotel_name = paramtext.ptexte

    for res_line in db_session.query(Res_line).filter(
             (Res_line.abreise == cidate) & (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:

            t_guest = query(t_guest_data, filters=(lambda t_guest: t_guest.gastnr == guest.gastnr), first=True)

            if not t_guest:
                t_guest = T_guest()
                t_guest_data.append(t_guest)

                buffer_copy(guest, t_guest)

        for history in db_session.query(History).filter(
                 (History.gastnr == res_line.gastnrmember) & (History.abreise <= cidate) & (History.zi_wechsel == False) & (History.abreisezeit != "") & (matches((History.bemerk,("*C/O:*"))) | (History.bemerk == None))).order_by(History._recid).all():
            t_history = T_history()
            t_history_data.append(t_history)

            buffer_copy(history, t_history)
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = 0
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "SharingGuestProfile"
            res_history.aenderung = "History of guest number " + to_string(history.gastnr) + " sent to HO"


            pass
            pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1343)]})

    if htparam:

        if htparam.fchar != "" and htparam.fchar != None:

            if num_entries(htparam.fchar, ":") > 1:
                vhost = entry(0, htparam.fchar, ":")
                vservice = entry(1, htparam.fchar, ":")
                hoappparam = " -H " + vhost + " -S " + vservice + " -DirectConnect -sessionModel Session-free"

        else:
            return generate_output()
        
        # lreturn = hServerHO:CONNECT (hoappparam, None, None, None) # Oscar - skip because using HServer on Progress
        lreturn = False

        if lreturn == False:
            return generate_output()
        
        local_storage.combo_flag = True
        # get_output(nt_shareguest_profileblho(hotel_name, t_guest_data, t_history_data)) # Oscar - skip because using HServer on Progress
        local_storage.combo_flag = False

        # lreturn = hServerHO:DISCONNECT() # Oscar - skip because using HServer on Progress


    return generate_output()