#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_request, Eg_location, Queasy, Zimmer, Res_line, Guest, Htparam, Bediener, Counters

def prepare_eg_mkreq_webbl(pvilanguage:int, user_init:string):

    prepare_cache ([Res_line, Guest, Htparam, Bediener, Counters])

    engid = 0
    groupid = 0
    status_str = ""
    open_str = ""
    flag = 0
    dept_str = ""
    ci_date = None
    request1_list = []
    t_eg_location_list = []
    t_queasy_list = []
    t_zimmer_list = []
    lvcarea:string = "eg-mkreq"
    guestname:string = ""
    eg_request = eg_location = queasy = zimmer = res_line = guest = htparam = bediener = counters = None

    request1 = t_eg_location = t_queasy = t_zimmer = resline1 = guest1 = None

    request1_list, Request1 = create_model_like(Eg_request)
    t_eg_location_list, T_eg_location = create_model_like(Eg_location)
    t_queasy_list, T_queasy = create_model_like(Queasy)
    t_zimmer_list, T_zimmer = create_model_like(Zimmer, {"gname_str":string})

    Resline1 = create_buffer("Resline1",Res_line)
    Guest1 = create_buffer("Guest1",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, status_str, open_str, flag, dept_str, ci_date, request1_list, t_eg_location_list, t_queasy_list, t_zimmer_list, lvcarea, guestname, eg_request, eg_location, queasy, zimmer, res_line, guest, htparam, bediener, counters
        nonlocal pvilanguage, user_init
        nonlocal resline1, guest1


        nonlocal request1, t_eg_location, t_queasy, t_zimmer, resline1, guest1
        nonlocal request1_list, t_eg_location_list, t_queasy_list, t_zimmer_list

        return {"engid": engid, "groupid": groupid, "status_str": status_str, "open_str": open_str, "flag": flag, "dept_str": dept_str, "ci_date": ci_date, "request1": request1_list, "t-eg-location": t_eg_location_list, "t-queasy": t_queasy_list, "t-zimmer": t_zimmer_list}

    def define_engineering():

        nonlocal engid, groupid, status_str, open_str, flag, dept_str, ci_date, request1_list, t_eg_location_list, t_queasy_list, t_zimmer_list, lvcarea, guestname, eg_request, eg_location, queasy, zimmer, res_line, guest, htparam, bediener, counters
        nonlocal pvilanguage, user_init
        nonlocal resline1, guest1


        nonlocal request1, t_eg_location, t_queasy, t_zimmer, resline1, guest1
        nonlocal request1_list, t_eg_location_list, t_queasy_list, t_zimmer_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            pass


    def define_group():

        nonlocal engid, groupid, status_str, open_str, flag, dept_str, ci_date, request1_list, t_eg_location_list, t_queasy_list, t_zimmer_list, lvcarea, guestname, eg_request, eg_location, queasy, zimmer, res_line, guest, htparam, bediener, counters
        nonlocal pvilanguage, user_init
        nonlocal resline1, guest1


        nonlocal request1, t_eg_location, t_queasy, t_zimmer, resline1, guest1
        nonlocal request1_list, t_eg_location_list, t_queasy_list, t_zimmer_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def initiate_it():

        nonlocal engid, groupid, status_str, open_str, flag, dept_str, ci_date, request1_list, t_eg_location_list, t_queasy_list, t_zimmer_list, lvcarea, guestname, eg_request, eg_location, queasy, zimmer, res_line, guest, htparam, bediener, counters
        nonlocal pvilanguage, user_init
        nonlocal resline1, guest1


        nonlocal request1, t_eg_location, t_queasy, t_zimmer, resline1, guest1
        nonlocal request1_list, t_eg_location_list, t_queasy_list, t_zimmer_list

        queasy1 = None
        Queasy1 =  create_buffer("Queasy1",Queasy)

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
        request1.reqstatus = 1
        request1.opened_by = user_init
        request1.opened_date = get_current_date()
        request1.opened_time = get_current_time_in_seconds()
        request1.urgency = 1


        status_str = translateExtended ("New", lvcarea, "")
        open_str = to_string(request1.opened_time, "HH:MM:SS")
        request1.deptnum = int (engid)

        queasy1 = db_session.query(Queasy1).filter(
                 (Queasy1.key == 19) & (Queasy1.number1 == request1.deptnum)).first()

        if not queasy1:
            flag = 1
            request1.deptnum = 0


        else:
            flag = 2
            dept_str = queasy1.char3


    def get_guestname(h_zinr:string):

        nonlocal engid, groupid, status_str, open_str, flag, dept_str, ci_date, request1_list, t_eg_location_list, t_queasy_list, t_zimmer_list, lvcarea, guestname, eg_request, eg_location, queasy, zimmer, res_line, guest, htparam, bediener, counters
        nonlocal pvilanguage, user_init
        nonlocal resline1, guest1


        nonlocal request1, t_eg_location, t_queasy, t_zimmer, resline1, guest1
        nonlocal request1_list, t_eg_location_list, t_queasy_list, t_zimmer_list

        resline1 = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, h_zinr)],"resstatus": [(ne, 13)]})

        if resline1:

            guest1 = get_cache (Guest, {"gastnr": [(eq, resline1.gastnrmember)]})

            if guest1:
                guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
        else:

            resline1 = get_cache (Res_line, {"active_flag": [(eq, 0)],"zinr": [(eq, h_zinr)],"resstatus": [(ne, 13)]})

            if resline1:

                guest1 = get_cache (Guest, {"gastnr": [(eq, resline1.gastnrmember)]})

                if guest1:
                    guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
            else:
                guestname = ""


    request1 = Request1()
    request1_list.append(request1)

    define_group()
    define_engineering()
    initiate_it()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():
        t_eg_location = T_eg_location()
        t_eg_location_list.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 132) | (Queasy.key == 133) | (Queasy.key == 130) | (Queasy.key == 19) | (Queasy.key == 135)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        get_guestname(zimmer.zinr)
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)
        t_zimmer.gname_str = guestname

    return generate_output()