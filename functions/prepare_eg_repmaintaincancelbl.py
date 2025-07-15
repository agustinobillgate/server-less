#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener, Eg_staff, Queasy, Eg_location

def prepare_eg_repmaintaincancelbl(user_init:string):

    prepare_cache ([Htparam, Bediener, Queasy])

    engid = 0
    groupid = 0
    ci_date = None
    tstatus_data = []
    tcategory_data = []
    tmaintask_data = []
    tlocation_data = []
    troom_data = []
    tfrequency_data = []
    tpic_data = []
    htparam = bediener = eg_staff = queasy = eg_location = None

    tpic = tfrequency = troom = tlocation = tmaintask = tcategory = tstatus = comcategory = None

    tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool})
    tfrequency_data, Tfrequency = create_model("Tfrequency", {"freq_nr":int, "freq_nm":string})
    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
    tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    tstatus_data, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, ci_date, tstatus_data, tcategory_data, tmaintask_data, tlocation_data, troom_data, tfrequency_data, tpic_data, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal user_init


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, comcategory
        nonlocal tpic_data, tfrequency_data, troom_data, tlocation_data, tmaintask_data, tcategory_data, tstatus_data

        return {"engid": engid, "groupid": groupid, "ci_date": ci_date, "tStatus": tstatus_data, "tcategory": tcategory_data, "tMaintask": tmaintask_data, "tLocation": tlocation_data, "troom": troom_data, "tfrequency": tfrequency_data, "tpic": tpic_data}

    def define_engineering():

        nonlocal engid, groupid, ci_date, tstatus_data, tcategory_data, tmaintask_data, tlocation_data, troom_data, tfrequency_data, tpic_data, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal user_init


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, comcategory
        nonlocal tpic_data, tfrequency_data, troom_data, tlocation_data, tmaintask_data, tcategory_data, tstatus_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal engid, groupid, ci_date, tstatus_data, tcategory_data, tmaintask_data, tlocation_data, troom_data, tfrequency_data, tpic_data, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal user_init


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, comcategory
        nonlocal tpic_data, tfrequency_data, troom_data, tlocation_data, tmaintask_data, tcategory_data, tstatus_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def create_frequency():

        nonlocal engid, groupid, ci_date, tstatus_data, tcategory_data, tmaintask_data, tlocation_data, troom_data, tfrequency_data, tpic_data, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal user_init


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, comcategory
        nonlocal tpic_data, tfrequency_data, troom_data, tlocation_data, tmaintask_data, tcategory_data, tstatus_data


        tfrequency_data.clear()
        tfrequency = Tfrequency()
        tfrequency_data.append(tfrequency)

        tfrequency.freq_nr = 1
        tfrequency.freq_nm = "Weekly"


        tfrequency = Tfrequency()
        tfrequency_data.append(tfrequency)

        tfrequency.freq_nr = 2
        tfrequency.freq_nm = "Monthly"


        tfrequency = Tfrequency()
        tfrequency_data.append(tfrequency)

        tfrequency.freq_nr = 3
        tfrequency.freq_nm = "Quarter"


        tfrequency = Tfrequency()
        tfrequency_data.append(tfrequency)

        tfrequency.freq_nr = 4
        tfrequency.freq_nm = "Half Yearly"


        tfrequency = Tfrequency()
        tfrequency_data.append(tfrequency)

        tfrequency.freq_nr = 5
        tfrequency.freq_nm = "Year"


    def create_status():

        nonlocal engid, groupid, ci_date, tstatus_data, tcategory_data, tmaintask_data, tlocation_data, troom_data, tfrequency_data, tpic_data, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal user_init


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, comcategory
        nonlocal tpic_data, tfrequency_data, troom_data, tlocation_data, tmaintask_data, tcategory_data, tstatus_data


        tstatus_data.clear()
        tstatus = Tstatus()
        tstatus_data.append(tstatus)

        tstatus.stat_nr = 1
        tstatus.stat_nm = "Scheduled"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_data.append(tstatus)

        tstatus.stat_nr = 2
        tstatus.stat_nm = "Processed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_data.append(tstatus)

        tstatus.stat_nr = 3
        tstatus.stat_nm = "Done"
        tstatus.stat_selected = False


    def create_pic():

        nonlocal engid, groupid, ci_date, tstatus_data, tcategory_data, tmaintask_data, tlocation_data, troom_data, tfrequency_data, tpic_data, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal user_init


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, comcategory
        nonlocal tpic_data, tfrequency_data, troom_data, tlocation_data, tmaintask_data, tcategory_data, tstatus_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_staff)
        tpic_data.clear()
        tpic = Tpic()
        tpic_data.append(tpic)

        tpic.pic_nr = 0
        tpic.pic_nm = ""
        tpic.pic_selected = False

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.usergroup == engid) & (Qbuff.activeflag)).order_by(Qbuff.nr).all():
            tpic = Tpic()
            tpic_data.append(tpic)

            tpic.pic_nr = qbuff.nr
            tpic.pic_nm = qbuff.name
            tpic.pic_selected = False


    def create_category():

        nonlocal engid, groupid, ci_date, tstatus_data, tcategory_data, tmaintask_data, tlocation_data, troom_data, tfrequency_data, tpic_data, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal user_init


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, comcategory
        nonlocal tpic_data, tfrequency_data, troom_data, tlocation_data, tmaintask_data, tcategory_data, tstatus_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        tcategory_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 132)).order_by(Qbuff._recid).all():
            tcategory = Tcategory()
            tcategory_data.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.char1
            tcategory.categ_selected = False


    def create_location():

        nonlocal engid, groupid, ci_date, tstatus_data, tcategory_data, tmaintask_data, tlocation_data, troom_data, tfrequency_data, tpic_data, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal user_init


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, comcategory
        nonlocal tpic_data, tfrequency_data, troom_data, tlocation_data, tmaintask_data, tcategory_data, tstatus_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_location)
        tlocation_data.clear()
        tlocation = Tlocation()
        tlocation_data.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = True

        for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():

            if qbuff.guestflag :
                tlocation = Tlocation()
                tlocation_data.append(tlocation)

                tlocation.loc_nr = qbuff.nr
                tlocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = True


            else:
                tlocation = Tlocation()
                tlocation_data.append(tlocation)

                tlocation.loc_nr = qbuff.nr
                tlocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = False


    def create_maintask():

        nonlocal engid, groupid, ci_date, tstatus_data, tcategory_data, tmaintask_data, tlocation_data, troom_data, tfrequency_data, tpic_data, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal user_init


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, comcategory
        nonlocal tpic_data, tfrequency_data, troom_data, tlocation_data, tmaintask_data, tcategory_data, tstatus_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        Comcategory = Tcategory
        comcategory_data = tcategory_data
        tmaintask_data.clear()

        for comcategory in query(comcategory_data, filters=(lambda comcategory: comcategory.categ_selected)):

            for qbuff in db_session.query(Qbuff).filter(
                     (Qbuff.key == 133) & (Qbuff.number2 == comcategory.categ_nr)).order_by(Qbuff._recid).all():
                tmaintask = Tmaintask()
                tmaintask_data.append(tmaintask)

                tmaintask.main_nr = qbuff.number1
                tmaintask.main_nm = qbuff.char1
                tmaintask.main_selected = True

    define_group()
    define_engineering()
    create_frequency()
    create_status()
    create_pic()
    create_category()
    create_location()

    for tcategory in query(tcategory_data):
        tcategory.categ_selected = True


    create_maintask()

    for tlocation in query(tlocation_data):
        tlocation.loc_selected = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    return generate_output()