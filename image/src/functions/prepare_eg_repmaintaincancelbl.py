from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bediener, Eg_staff, Queasy, Eg_location

def prepare_eg_repmaintaincancelbl(user_init:str):
    engid = 0
    groupid = 0
    ci_date = None
    tstatus_list = []
    tcategory_list = []
    tmaintask_list = []
    tlocation_list = []
    troom_list = []
    tfrequency_list = []
    tpic_list = []
    htparam = bediener = eg_staff = queasy = eg_location = None

    tpic = tfrequency = troom = tlocation = tmaintask = tcategory = tstatus = qbuff = comcategory = None

    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool})
    tfrequency_list, Tfrequency = create_model("Tfrequency", {"freq_nr":int, "freq_nm":str})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":str, "stat_selected":bool})

    Qbuff = Queasy
    Comcategory = Tcategory
    comcategory_list = tcategory_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, ci_date, tstatus_list, tcategory_list, tmaintask_list, tlocation_list, troom_list, tfrequency_list, tpic_list, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal qbuff, comcategory


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, qbuff, comcategory
        nonlocal tpic_list, tfrequency_list, troom_list, tlocation_list, tmaintask_list, tcategory_list, tstatus_list
        return {"engid": engid, "groupid": groupid, "ci_date": ci_date, "tStatus": tstatus_list, "tcategory": tcategory_list, "tMaintask": tmaintask_list, "tLocation": tlocation_list, "troom": troom_list, "tFrequency": tfrequency_list, "tpic": tpic_list}

    def define_engineering():

        nonlocal engid, groupid, ci_date, tstatus_list, tcategory_list, tmaintask_list, tlocation_list, troom_list, tfrequency_list, tpic_list, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal qbuff, comcategory


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, qbuff, comcategory
        nonlocal tpic_list, tfrequency_list, troom_list, tlocation_list, tmaintask_list, tcategory_list, tstatus_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal engid, groupid, ci_date, tstatus_list, tcategory_list, tmaintask_list, tlocation_list, troom_list, tfrequency_list, tpic_list, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal qbuff, comcategory


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, qbuff, comcategory
        nonlocal tpic_list, tfrequency_list, troom_list, tlocation_list, tmaintask_list, tcategory_list, tstatus_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def create_frequency():

        nonlocal engid, groupid, ci_date, tstatus_list, tcategory_list, tmaintask_list, tlocation_list, troom_list, tfrequency_list, tpic_list, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal qbuff, comcategory


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, qbuff, comcategory
        nonlocal tpic_list, tfrequency_list, troom_list, tlocation_list, tmaintask_list, tcategory_list, tstatus_list


        tFrequency_list.clear()
        tfrequency = Tfrequency()
        tfrequency_list.append(tfrequency)

        tFrequency.freq_nr = 1
        tFrequency.freq_nm = "Weekly"


        tfrequency = Tfrequency()
        tfrequency_list.append(tfrequency)

        tFrequency.freq_nr = 2
        tFrequency.freq_nm = "Monthly"


        tfrequency = Tfrequency()
        tfrequency_list.append(tfrequency)

        tFrequency.freq_nr = 3
        tFrequency.freq_nm = "Quarter"


        tfrequency = Tfrequency()
        tfrequency_list.append(tfrequency)

        tFrequency.freq_nr = 4
        tFrequency.freq_nm = "Half Yearly"


        tfrequency = Tfrequency()
        tfrequency_list.append(tfrequency)

        tFrequency.freq_nr = 5
        tFrequency.freq_nm = "Year"

    def create_status():

        nonlocal engid, groupid, ci_date, tstatus_list, tcategory_list, tmaintask_list, tlocation_list, troom_list, tfrequency_list, tpic_list, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal qbuff, comcategory


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, qbuff, comcategory
        nonlocal tpic_list, tfrequency_list, troom_list, tlocation_list, tmaintask_list, tcategory_list, tstatus_list


        tStatus_list.clear()
        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 1
        tStatus.stat_nm = "Scheduled"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 2
        tStatus.stat_nm = "Processed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 3
        tStatus.stat_nm = "Done"
        tstatus.stat_selected = False

    def create_pic():

        nonlocal engid, groupid, ci_date, tstatus_list, tcategory_list, tmaintask_list, tlocation_list, troom_list, tfrequency_list, tpic_list, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal qbuff, comcategory


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, qbuff, comcategory
        nonlocal tpic_list, tfrequency_list, troom_list, tlocation_list, tmaintask_list, tcategory_list, tstatus_list


        Qbuff = Eg_staff
        tpic_list.clear()
        tpic = Tpic()
        tpic_list.append(tpic)

        tpic.pic_nr = 0
        tpic.pic_nm = ""
        tpic.pic_selected = False

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.usergroup == engid) &  (Qbuff.activeflag)).all():
            tpic = Tpic()
            tpic_list.append(tpic)

            tpic.pic_nr = qbuff.nr
            tpic.pic_nm = qbuff.name
            tpic.pic_selected = False

    def create_category():

        nonlocal engid, groupid, ci_date, tstatus_list, tcategory_list, tmaintask_list, tlocation_list, troom_list, tfrequency_list, tpic_list, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal qbuff, comcategory


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, qbuff, comcategory
        nonlocal tpic_list, tfrequency_list, troom_list, tlocation_list, tmaintask_list, tcategory_list, tstatus_list


        Qbuff = Queasy
        tcategory_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 132)).all():
            tcategory = Tcategory()
            tcategory_list.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.char1
            tcategory.categ_selected = False

    def create_location():

        nonlocal engid, groupid, ci_date, tstatus_list, tcategory_list, tmaintask_list, tlocation_list, troom_list, tfrequency_list, tpic_list, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal qbuff, comcategory


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, qbuff, comcategory
        nonlocal tpic_list, tfrequency_list, troom_list, tlocation_list, tmaintask_list, tcategory_list, tstatus_list


        Qbuff = Eg_location
        tLocation_list.clear()
        tlocation = Tlocation()
        tlocation_list.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = True

        for qbuff in db_session.query(Qbuff).all():

            if qbuff.guestflag :
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tLocation.loc_nr = qbuff.nr
                tLocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = True


            else:
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tLocation.loc_nr = qbuff.nr
                tLocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = False

    def create_maintask():

        nonlocal engid, groupid, ci_date, tstatus_list, tcategory_list, tmaintask_list, tlocation_list, troom_list, tfrequency_list, tpic_list, htparam, bediener, eg_staff, queasy, eg_location
        nonlocal qbuff, comcategory


        nonlocal tpic, tfrequency, troom, tlocation, tmaintask, tcategory, tstatus, qbuff, comcategory
        nonlocal tpic_list, tfrequency_list, troom_list, tlocation_list, tmaintask_list, tcategory_list, tstatus_list


        Qbuff = Queasy
        Comcategory = Tcategory
        tMaintask_list.clear()

        for comcategory in query(comcategory_list, filters=(lambda comcategory :comCategory.categ_SELECTED)):

            for qbuff in db_session.query(Qbuff).filter(
                    (Qbuff.key == 133) &  (Qbuff.number2 == comcategory.categ_nr)).all():
                tmaintask = Tmaintask()
                tmaintask_list.append(tmaintask)

                tMaintask.Main_nr = qbuff.number1
                tMaintask.Main_nm = qbuff.char1
                tmaintask.main_selected = True


    define_group()
    define_engineering()
    create_frequency()
    create_status()
    create_pic()
    create_category()
    create_location()

    for tcategory in query(tcategory_list):
        tcategory.categ_selected = True


    create_maintask()

    for tlocation in query(tlocation_list):
        tlocation.loc_selected = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    return generate_output()