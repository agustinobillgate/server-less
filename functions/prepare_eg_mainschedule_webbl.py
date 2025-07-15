#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_location, Eg_property, Eg_staff, Zimmer, Queasy, Eg_action, Eg_maintain, Res_line, Guest, Bediener, Htparam, Counters

def prepare_eg_mainschedule_webbl(user_init:string, dayplan:date, firstday:date, endday:date):

    prepare_cache ([Res_line, Guest, Bediener, Htparam, Counters])

    groupid = 0
    engid = 0
    maintain_data = []
    action_data = []
    t_eg_location_data = []
    t_zimmer_data = []
    t_eg_property_data = []
    t_queasy_data = []
    t_eg_staff_data = []
    guestname:string = ""
    eg_location = eg_property = eg_staff = zimmer = queasy = eg_action = eg_maintain = res_line = guest = bediener = htparam = counters = None

    t_eg_location = t_eg_property = t_eg_staff = t_zimmer = t_queasy = action = staff = maintain = resline1 = guest1 = None

    t_eg_location_data, T_eg_location = create_model_like(Eg_location)
    t_eg_property_data, T_eg_property = create_model_like(Eg_property)
    t_eg_staff_data, T_eg_staff = create_model_like(Eg_staff)
    t_zimmer_data, T_zimmer = create_model_like(Zimmer, {"gname_str":string})
    t_queasy_data, T_queasy = create_model_like(Queasy)
    action_data, Action = create_model_like(Eg_action, {"selected":bool})
    staff_data, Staff = create_model_like(Eg_staff, {"staff_selected":bool})
    maintain_data, Maintain = create_model_like(Eg_maintain)

    Resline1 = create_buffer("Resline1",Res_line)
    Guest1 = create_buffer("Guest1",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, maintain_data, action_data, t_eg_location_data, t_zimmer_data, t_eg_property_data, t_queasy_data, t_eg_staff_data, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal user_init, dayplan, firstday, endday
        nonlocal resline1, guest1


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1
        nonlocal t_eg_location_data, t_eg_property_data, t_eg_staff_data, t_zimmer_data, t_queasy_data, action_data, staff_data, maintain_data

        return {"groupid": groupid, "engid": engid, "maintain": maintain_data, "action": action_data, "t-eg-location": t_eg_location_data, "t-zimmer": t_zimmer_data, "t-eg-property": t_eg_property_data, "t-queasy": t_queasy_data, "t-eg-staff": t_eg_staff_data}

    def define_group():

        nonlocal groupid, engid, maintain_data, action_data, t_eg_location_data, t_zimmer_data, t_eg_property_data, t_queasy_data, t_eg_staff_data, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal user_init, dayplan, firstday, endday
        nonlocal resline1, guest1


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1
        nonlocal t_eg_location_data, t_eg_property_data, t_eg_staff_data, t_zimmer_data, t_queasy_data, action_data, staff_data, maintain_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal groupid, engid, maintain_data, action_data, t_eg_location_data, t_zimmer_data, t_eg_property_data, t_queasy_data, t_eg_staff_data, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal user_init, dayplan, firstday, endday
        nonlocal resline1, guest1


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1
        nonlocal t_eg_location_data, t_eg_property_data, t_eg_staff_data, t_zimmer_data, t_queasy_data, action_data, staff_data, maintain_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            pass


    def create_action():

        nonlocal groupid, engid, maintain_data, action_data, t_eg_location_data, t_zimmer_data, t_eg_property_data, t_queasy_data, t_eg_staff_data, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal user_init, dayplan, firstday, endday
        nonlocal resline1, guest1


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1
        nonlocal t_eg_location_data, t_eg_property_data, t_eg_staff_data, t_zimmer_data, t_queasy_data, action_data, staff_data, maintain_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_action)
        action_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.usefor != 2)).order_by(Qbuff._recid).all():
            action = Action()
            action_data.append(action)

            action.actionnr = qbuff.actionnr
            action.bezeich = qbuff.bezeich
            action.maintask = qbuff.maintask
            action.selected = False


    def create_staff():

        nonlocal groupid, engid, maintain_data, action_data, t_eg_location_data, t_zimmer_data, t_eg_property_data, t_queasy_data, t_eg_staff_data, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal user_init, dayplan, firstday, endday
        nonlocal resline1, guest1


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1
        nonlocal t_eg_location_data, t_eg_property_data, t_eg_staff_data, t_zimmer_data, t_queasy_data, action_data, staff_data, maintain_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_staff)
        staff_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.usergroup == engid) & (Qbuff.activeflag)).order_by(Qbuff._recid).all():
            staff = Staff()
            staff_data.append(staff)

            staff.nr = qbuff.nr
            staff.name = qbuff.name
            staff.staff_selected = False


    def init_maintain():

        nonlocal groupid, engid, maintain_data, action_data, t_eg_location_data, t_zimmer_data, t_eg_property_data, t_queasy_data, t_eg_staff_data, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal user_init, dayplan, firstday, endday
        nonlocal resline1, guest1


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1
        nonlocal t_eg_location_data, t_eg_property_data, t_eg_staff_data, t_zimmer_data, t_queasy_data, action_data, staff_data, maintain_data

        counters = get_cache (Counters, {"counter_no": [(eq, 38)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 38
            counters.counter_bez = "Counter for maintenance in engineering"
            counters.counter = 0


        else:
            pass
        maintain.maintainnr = counters.counter + 1
        maintain.workdate = None
        maintain.type = 1
        maintain.category = 0
        maintain.maintask = 0
        maintain.propertynr = 0
        maintain.comments = ""
        maintain.typework = 1
        maintain.pic = 0

        if dayplan != None:
            maintain.estworkdate = dayplan


        else:

            if firstday > get_current_date():
                maintain.estworkdate = firstday


            else:

                if endday > get_current_date():
                    maintain.estworkdate = get_current_date()


                else:
                    maintain.estworkdate = get_current_date()


    def get_guestname(h_zinr:string):

        nonlocal groupid, engid, maintain_data, action_data, t_eg_location_data, t_zimmer_data, t_eg_property_data, t_queasy_data, t_eg_staff_data, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal user_init, dayplan, firstday, endday
        nonlocal resline1, guest1


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1
        nonlocal t_eg_location_data, t_eg_property_data, t_eg_staff_data, t_zimmer_data, t_queasy_data, action_data, staff_data, maintain_data

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


    maintain = Maintain()
    maintain_data.append(maintain)

    define_group()
    define_engineering()
    create_action()
    create_staff()
    init_maintain()

    for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():
        t_eg_location = T_eg_location()
        t_eg_location_data.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        get_guestname(zimmer.zinr)
        t_zimmer = T_zimmer()
        t_zimmer_data.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)
        t_zimmer.gname_str = guestname

    for eg_property in db_session.query(Eg_property).order_by(Eg_property._recid).all():
        t_eg_property = T_eg_property()
        t_eg_property_data.append(t_eg_property)

        buffer_copy(eg_property, t_eg_property)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 132) | (Queasy.key == 133) | (Queasy.key == 135)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    for eg_staff in db_session.query(Eg_staff).order_by(Eg_staff._recid).all():
        t_eg_staff = T_eg_staff()
        t_eg_staff_data.append(t_eg_staff)

        buffer_copy(eg_staff, t_eg_staff)

    return generate_output()