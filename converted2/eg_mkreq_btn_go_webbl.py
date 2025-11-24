#using conversion tools version: 1.0.0.117
#---------------------------------------------------
# Rd, 24/11/2025 , Update last counter dengan next_counter_for_update
#---------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_request, Htparam, Eg_queasy, Bediener, Eg_property, Counters, Eg_location, Res_line, History, Guest
from functions.next_counter_for_update import next_counter_for_update

request1_data, Request1 = create_model_like(Eg_request)

def eg_mkreq_btn_go_webbl(request1_data:[Request1], sguestflag:bool, sub_str:string, main_str:string, prop_bezeich:string):

    prepare_cache ([Htparam, Eg_queasy, Eg_property, Counters, Eg_location, Res_line, History])

    ci_date:date = None
    eg_request = htparam = eg_queasy = bediener = eg_property = counters = eg_location = res_line = history = guest = None

    request1 = None

    db_session = local_storage.db_session
    last_count:int = 0
    error_lock:string = ""
    sub_str = sub_str.strip()
    main_str = main_str.strip()
    prop_bezeich = prop_bezeich.strip()

    def generate_output():
        nonlocal ci_date, eg_request, htparam, eg_queasy, bediener, eg_property, counters, eg_location, res_line, history, guest
        nonlocal request1_data, sguestflag, sub_str, main_str, prop_bezeich


        nonlocal request1

        return {"request1": request1_data}

    def create_request():

        nonlocal ci_date, eg_request, htparam, eg_queasy, bediener, eg_property, counters, eg_location, res_line, history, guest
        nonlocal request1_data, sguestflag, sub_str, main_str, prop_bezeich


        nonlocal request1

        strmemo:string = ""
        nr:int = 0
        prop_nr:int = 0
        buff = None
        usr = None
        buff_property = None
        Buff =  create_buffer("Buff",Eg_queasy)
        Usr =  create_buffer("Usr",Bediener)
        Buff_property =  create_buffer("Buff_property",Eg_property)

        counters = get_cache (Counters, {"counter_no": [(eq, 34)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 34
            counters.counter_bez = "Counter for Engineering RequestNo"
            counters.counter = 1


            pass
        else:
            pass
            # counters.counter = counters.counter + 1
            last_count, error_lock = get_output(next_counter_for_update(34))

            pass
        # request1.reqnr = counters.counter
        request1.reqnr = last_count

        request1.opened_time = get_current_time_in_seconds()

        if request1.propertynr == 0:

            for buff_property in db_session.query(Buff_property).order_by(Buff_property.nr.desc()).yield_per(100):
                prop_nr = buff_property.nr
                break
            prop_nr = prop_nr + 1
            eg_property = Eg_property()
            db_session.add(eg_property)

            eg_property.nr = prop_nr
            eg_property.bezeich = prop_bezeich
            eg_property.maintask = request1.maintask
            eg_property.zinr = request1.zinr
            eg_property.datum = get_current_date()

            if sguestflag :

                eg_location = get_cache (Eg_location, {"guestflag": [(eq, True)]})

                if eg_location:
                    eg_property.location = eg_location.nr
            else:
                eg_property.location = request1.reserve_int
            request1.propertynr = prop_nr

        if sguestflag :

            eg_location = get_cache (Eg_location, {"guestflag": [(eq, True)]})

            if eg_location:
                request1.reserve_int = eg_location.nr

            if request1.zinr != "" or request1.zinr != None:
                get_guestname()
        request1.subtask_bezeich = sub_str


        eg_request = Eg_request()
        db_session.add(eg_request)

        buffer_copy(request1, eg_request)
        pass

        for buff in db_session.query(Buff).filter(
                     (Buff.key == 3) & (Buff.reqnr == request1.reqnr)).order_by(Buff._recid).all():

            if buff.hist_nr > nr:
                nr = buff.hist_nr
        eg_queasy = Eg_queasy()
        db_session.add(eg_queasy)

        eg_queasy.key = 3
        eg_queasy.reqnr = request1.reqnr
        eg_queasy.hist_nr = nr + 1
        eg_queasy.hist_time = get_current_time_in_seconds()
        eg_queasy.hist_fdate = get_current_date()

        if request1.assign_to != 0:
            eg_queasy.usr_nr = request1.assign_to
        pass


    def create_history():

        nonlocal ci_date, eg_request, htparam, eg_queasy, bediener, eg_property, counters, eg_location, res_line, history, guest
        nonlocal request1_data, sguestflag, sub_str, main_str, prop_bezeich


        nonlocal request1

        resline1 = None
        Resline1 =  create_buffer("Resline1",Res_line)

        resline1 = get_cache (Res_line, {"resnr": [(eq, request1.resnr)],"reslinnr": [(eq, request1.reslinnr)]})

        if resline1:
            history.ankunft = resline1.ankunft
            history.abreise = resline1.abreise
            history.zinr = resline1.zinr


        history = History()
        db_session.add(history)

        history.gastnr = request1.gastnr
        history.resnr = request1.resnr
        history.reslinnr = request1.reslinnr
        history.zi_wechsel = True
        history.bemerk = main_str + ", " + sub_str + ", " + request1.task_def


        pass


    def get_guestname():

        nonlocal ci_date, eg_request, htparam, eg_queasy, bediener, eg_property, counters, eg_location, res_line, history, guest
        nonlocal request1_data, sguestflag, sub_str, main_str, prop_bezeich


        nonlocal request1

        resline1 = None
        guest1 = None
        Resline1 =  create_buffer("Resline1",Res_line)
        Guest1 =  create_buffer("Guest1",Guest)

        resline1 = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, request1.zinr)],"resstatus": [(ne, 12)],"ankunft": [(le, ci_date)],"abreise": [(ge, ci_date)]})

        if resline1:

            guest1 = db_session.query(Guest1).filter(
                     (Guest1.gastnr == resline1.gastnrmember)).first()

            if guest1:
                request1.gastnr = resline1.gastnrmember
                request1.resnr = resline1.resnr
                request1.reslinnr = resline1.reslinnr


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    request1 = query(request1_data, first=True)
    create_request()
    create_history()

    return generate_output()