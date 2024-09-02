from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Eg_location, Eg_property, Eg_staff, Zimmer, Queasy, Eg_action, Eg_maintain, Res_line, Guest, Bediener, Htparam, Counters

def prepare_eg_mainschedule_webbl(user_init:str, dayplan:date, firstday:date, endday:date):
    groupid = 0
    engid = 0
    maintain_list = []
    action_list = []
    t_eg_location_list = []
    t_zimmer_list = []
    t_eg_property_list = []
    t_queasy_list = []
    t_eg_staff_list = []
    guestname:str = ""
    eg_location = eg_property = eg_staff = zimmer = queasy = eg_action = eg_maintain = res_line = guest = bediener = htparam = counters = None

    t_eg_location = t_eg_property = t_eg_staff = t_zimmer = t_queasy = action = staff = maintain = resline1 = guest1 = qbuff = None

    t_eg_location_list, T_eg_location = create_model_like(Eg_location)
    t_eg_property_list, T_eg_property = create_model_like(Eg_property)
    t_eg_staff_list, T_eg_staff = create_model_like(Eg_staff)
    t_zimmer_list, T_zimmer = create_model_like(Zimmer, {"gname_str":str})
    t_queasy_list, T_queasy = create_model_like(Queasy)
    action_list, Action = create_model_like(Eg_action, {"selected":bool})
    staff_list, Staff = create_model_like(Eg_staff, {"staff_selected":bool})
    maintain_list, Maintain = create_model_like(Eg_maintain)

    Resline1 = Res_line
    Guest1 = Guest
    Qbuff = Eg_staff

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, maintain_list, action_list, t_eg_location_list, t_zimmer_list, t_eg_property_list, t_queasy_list, t_eg_staff_list, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal resline1, guest1, qbuff


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1, qbuff
        nonlocal t_eg_location_list, t_eg_property_list, t_eg_staff_list, t_zimmer_list, t_queasy_list, action_list, staff_list, maintain_list
        return {"groupid": groupid, "engid": engid, "maintain": maintain_list, "action": action_list, "t-eg-location": t_eg_location_list, "t-zimmer": t_zimmer_list, "t-eg-property": t_eg_property_list, "t-queasy": t_queasy_list, "t-eg-staff": t_eg_staff_list}

    def define_group():

        nonlocal groupid, engid, maintain_list, action_list, t_eg_location_list, t_zimmer_list, t_eg_property_list, t_queasy_list, t_eg_staff_list, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal resline1, guest1, qbuff


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1, qbuff
        nonlocal t_eg_location_list, t_eg_property_list, t_eg_staff_list, t_zimmer_list, t_queasy_list, action_list, staff_list, maintain_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def define_engineering():

        nonlocal groupid, engid, maintain_list, action_list, t_eg_location_list, t_zimmer_list, t_eg_property_list, t_queasy_list, t_eg_staff_list, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal resline1, guest1, qbuff


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1, qbuff
        nonlocal t_eg_location_list, t_eg_property_list, t_eg_staff_list, t_zimmer_list, t_queasy_list, action_list, staff_list, maintain_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            pass

    def create_action():

        nonlocal groupid, engid, maintain_list, action_list, t_eg_location_list, t_zimmer_list, t_eg_property_list, t_queasy_list, t_eg_staff_list, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal resline1, guest1, qbuff


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1, qbuff
        nonlocal t_eg_location_list, t_eg_property_list, t_eg_staff_list, t_zimmer_list, t_queasy_list, action_list, staff_list, maintain_list


        Qbuff = Eg_action
        action_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.usefor != 2)).all():
            action = Action()
            action_list.append(action)

            action.actionnr = qbuff.actionnr
            action.bezeich = qbuff.bezeich
            action.maintask = qbuff.maintask
            action.SELECTED = False

    def create_staff():

        nonlocal groupid, engid, maintain_list, action_list, t_eg_location_list, t_zimmer_list, t_eg_property_list, t_queasy_list, t_eg_staff_list, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal resline1, guest1, qbuff


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1, qbuff
        nonlocal t_eg_location_list, t_eg_property_list, t_eg_staff_list, t_zimmer_list, t_queasy_list, action_list, staff_list, maintain_list


        Qbuff = Eg_staff
        staff_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.usergroup == engid) &  (Qbuff.activeflag)).all():
            staff = Staff()
            staff_list.append(staff)

            staff.nr = qbuff.nr
            staff.name = qbuff.name
            staff.staff_SELECTED = False

    def init_maintain():

        nonlocal groupid, engid, maintain_list, action_list, t_eg_location_list, t_zimmer_list, t_eg_property_list, t_queasy_list, t_eg_staff_list, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal resline1, guest1, qbuff


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1, qbuff
        nonlocal t_eg_location_list, t_eg_property_list, t_eg_staff_list, t_zimmer_list, t_queasy_list, action_list, staff_list, maintain_list

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 38)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 38
            counters.counter_bez = "Counter for maintenance in engineering"
            counters.counter = 0


        else:

            counters = db_session.query(Counters).first()
        maintain.maintainnr = counters.counter + 1
        maintain.workdate = None
        maintain.TYPE = 1
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

    def get_guestname(h_zinr:str):

        nonlocal groupid, engid, maintain_list, action_list, t_eg_location_list, t_zimmer_list, t_eg_property_list, t_queasy_list, t_eg_staff_list, guestname, eg_location, eg_property, eg_staff, zimmer, queasy, eg_action, eg_maintain, res_line, guest, bediener, htparam, counters
        nonlocal resline1, guest1, qbuff


        nonlocal t_eg_location, t_eg_property, t_eg_staff, t_zimmer, t_queasy, action, staff, maintain, resline1, guest1, qbuff
        nonlocal t_eg_location_list, t_eg_property_list, t_eg_staff_list, t_zimmer_list, t_queasy_list, action_list, staff_list, maintain_list

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

    maintain = Maintain()
    maintain_list.append(maintain)

    define_group()
    define_engineering()
    create_action()
    create_staff()
    init_maintain()

    for eg_location in db_session.query(Eg_location).all():
        t_eg_location = T_eg_location()
        t_eg_location_list.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    for zimmer in db_session.query(Zimmer).all():
        get_guestname(zimmer.zinr)
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)
        t_zimmer.gname_str = guestname

    for eg_property in db_session.query(Eg_property).all():
        t_eg_property = T_eg_property()
        t_eg_property_list.append(t_eg_property)

        buffer_copy(eg_property, t_eg_property)

    for queasy in db_session.query(Queasy).filter(
            (Queasy.KEY == 132) |  (Queasy.KEY == 133) |  (Queasy.KEY == 135)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    for eg_staff in db_session.query(Eg_staff).all():
        t_eg_staff = T_eg_staff()
        t_eg_staff_list.append(t_eg_staff)

        buffer_copy(eg_staff, t_eg_staff)

    return generate_output()