from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Eg_request, Eg_location, Eg_property, Queasy, Eg_subtask, Eg_staff, Zimmer, Res_line, Guest, Htparam, Bediener, Counters

def prepare_eg_mkreq_webbl(pvilanguage:int, user_init:str):
    engid = 0
    groupid = 0
    status_str = ""
    open_str = ""
    flag = 0
    dept_str = ""
    ci_date = None
    request1_list = []
    t_eg_location_list = []
    t_eg_property_list = []
    t_queasy_list = []
    t_eg_subtask_list = []
    t_zimmer_list = []
    t_eg_staff_list = []
    lvcarea:str = "eg_mkreq"
    guestname:str = ""
    eg_request = eg_location = eg_property = queasy = eg_subtask = eg_staff = zimmer = res_line = guest = htparam = bediener = counters = None

    request1 = t_eg_location = t_eg_property = t_queasy = t_eg_subtask = t_eg_staff = t_zimmer = resline1 = guest1 = queasy1 = None

    request1_list, Request1 = create_model_like(Eg_request)
    t_eg_location_list, T_eg_location = create_model_like(Eg_location)
    t_eg_property_list, T_eg_property = create_model_like(Eg_property)
    t_queasy_list, T_queasy = create_model_like(Queasy)
    t_eg_subtask_list, T_eg_subtask = create_model_like(Eg_subtask)
    t_eg_staff_list, T_eg_staff = create_model_like(Eg_staff)
    t_zimmer_list, T_zimmer = create_model_like(Zimmer, {"gname_str":str})

    Resline1 = Res_line
    Guest1 = Guest
    Queasy1 = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, status_str, open_str, flag, dept_str, ci_date, request1_list, t_eg_location_list, t_eg_property_list, t_queasy_list, t_eg_subtask_list, t_zimmer_list, t_eg_staff_list, lvcarea, guestname, eg_request, eg_location, eg_property, queasy, eg_subtask, eg_staff, zimmer, res_line, guest, htparam, bediener, counters
        nonlocal resline1, guest1, queasy1


        nonlocal request1, t_eg_location, t_eg_property, t_queasy, t_eg_subtask, t_eg_staff, t_zimmer, resline1, guest1, queasy1
        nonlocal request1_list, t_eg_location_list, t_eg_property_list, t_queasy_list, t_eg_subtask_list, t_eg_staff_list, t_zimmer_list
        return {"engid": engid, "groupid": groupid, "status_str": status_str, "open_str": open_str, "flag": flag, "dept_str": dept_str, "ci_date": ci_date, "request1": request1_list, "t-eg-location": t_eg_location_list, "t-eg-property": t_eg_property_list, "t-queasy": t_queasy_list, "t-eg-subtask": t_eg_subtask_list, "t-zimmer": t_zimmer_list, "t-eg-staff": t_eg_staff_list}

    def define_engineering():

        nonlocal engid, groupid, status_str, open_str, flag, dept_str, ci_date, request1_list, t_eg_location_list, t_eg_property_list, t_queasy_list, t_eg_subtask_list, t_zimmer_list, t_eg_staff_list, lvcarea, guestname, eg_request, eg_location, eg_property, queasy, eg_subtask, eg_staff, zimmer, res_line, guest, htparam, bediener, counters
        nonlocal resline1, guest1, queasy1


        nonlocal request1, t_eg_location, t_eg_property, t_queasy, t_eg_subtask, t_eg_staff, t_zimmer, resline1, guest1, queasy1
        nonlocal request1_list, t_eg_location_list, t_eg_property_list, t_queasy_list, t_eg_subtask_list, t_eg_staff_list, t_zimmer_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            pass

    def define_group():

        nonlocal engid, groupid, status_str, open_str, flag, dept_str, ci_date, request1_list, t_eg_location_list, t_eg_property_list, t_queasy_list, t_eg_subtask_list, t_zimmer_list, t_eg_staff_list, lvcarea, guestname, eg_request, eg_location, eg_property, queasy, eg_subtask, eg_staff, zimmer, res_line, guest, htparam, bediener, counters
        nonlocal resline1, guest1, queasy1


        nonlocal request1, t_eg_location, t_eg_property, t_queasy, t_eg_subtask, t_eg_staff, t_zimmer, resline1, guest1, queasy1
        nonlocal request1_list, t_eg_location_list, t_eg_property_list, t_queasy_list, t_eg_subtask_list, t_eg_staff_list, t_zimmer_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def initiate_it():

        nonlocal engid, groupid, status_str, open_str, flag, dept_str, ci_date, request1_list, t_eg_location_list, t_eg_property_list, t_queasy_list, t_eg_subtask_list, t_zimmer_list, t_eg_staff_list, lvcarea, guestname, eg_request, eg_location, eg_property, queasy, eg_subtask, eg_staff, zimmer, res_line, guest, htparam, bediener, counters
        nonlocal resline1, guest1, queasy1


        nonlocal request1, t_eg_location, t_eg_property, t_queasy, t_eg_subtask, t_eg_staff, t_zimmer, resline1, guest1, queasy1
        nonlocal request1_list, t_eg_location_list, t_eg_property_list, t_queasy_list, t_eg_subtask_list, t_eg_staff_list, t_zimmer_list


        Queasy1 = Queasy

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 34)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 34
            counters.counter_bez = "Counter for Engineering RequestNo"
            counters.counter = 1

            counters = db_session.query(Counters).first()
        else:

            counters = db_session.query(Counters).first()
        request1.reqstatus = 1
        request1.opened_by = user_init
        request1.opened_date = get_current_date()
        request1.opened_time = get_current_time_in_seconds()
        request1.urgency = 1


        status_str = translateExtended ("New", lvcarea, "")
        open_str = to_string(request1.opened_time, "HH:MM:SS")
        request1.deptnum = int (engid)

        queasy1 = db_session.query(Queasy1).filter(
                (Queasy1.key == 19) &  (Queasy1.number1 == request1.deptnum)).first()

        if not queasy1:
            flag = 1
            request1.deptnum = 0


        else:
            flag = 2
            dept_str = queasy1.char3

    def get_guestname(h_zinr:str):

        nonlocal engid, groupid, status_str, open_str, flag, dept_str, ci_date, request1_list, t_eg_location_list, t_eg_property_list, t_queasy_list, t_eg_subtask_list, t_zimmer_list, t_eg_staff_list, lvcarea, guestname, eg_request, eg_location, eg_property, queasy, eg_subtask, eg_staff, zimmer, res_line, guest, htparam, bediener, counters
        nonlocal resline1, guest1, queasy1


        nonlocal request1, t_eg_location, t_eg_property, t_queasy, t_eg_subtask, t_eg_staff, t_zimmer, resline1, guest1, queasy1
        nonlocal request1_list, t_eg_location_list, t_eg_property_list, t_queasy_list, t_eg_subtask_list, t_eg_staff_list, t_zimmer_list

        resline1 = db_session.query(Resline1).filter(
                (Resline1.active_flag == 1) &  (func.lower(Resline1.zinr) == (h_zinr).lower()) &  (Resline1.resstatus != 13)).first()

        if resline1:

            guest1 = db_session.query(Guest1).filter(
                    (Guest1.gastnr == resline1.gastnrmember)).first()

            if guest1:
                guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
        else:

            resline1 = db_session.query(Resline1).filter(
                    (Resline1.active_flag == 0) &  (func.lower(Resline1.zinr) == (h_zinr).lower()) &  (Resline1.resstatus != 13)).first()

            if resline1:

                guest1 = db_session.query(Guest1).filter(
                        (Guest1.gastnr == resline1.gastnrmember)).first()

                if guest1:
                    guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
            else:
                guestname = ""


    request1 = Request1()
    request1_list.append(request1)

    define_group()
    define_engineering()
    initiate_it()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    for eg_location in db_session.query(Eg_location).all():
        t_eg_location = T_eg_location()
        t_eg_location_list.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    for eg_property in db_session.query(Eg_property).all():
        t_eg_property = T_eg_property()
        t_eg_property_list.append(t_eg_property)

        buffer_copy(eg_property, t_eg_property)

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 132) |  (Queasy.key == 133) |  (Queasy.key == 130) |  (Queasy.key == 19) |  (Queasy.key == 135)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    for eg_subtask in db_session.query(Eg_subtask).all():
        t_eg_subtask = T_eg_subtask()
        t_eg_subtask_list.append(t_eg_subtask)

        buffer_copy(eg_subtask, t_eg_subtask)

    for zimmer in db_session.query(Zimmer).all():
        get_guestname(zimmer.zinr)
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)
        t_zimmer.gname_str = guestname

    for eg_staff in db_session.query(Eg_staff).all():
        t_eg_staff = T_eg_staff()
        t_eg_staff_list.append(t_eg_staff)

        buffer_copy(eg_staff, t_eg_staff)

    return generate_output()