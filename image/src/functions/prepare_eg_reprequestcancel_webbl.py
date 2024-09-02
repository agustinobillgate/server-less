from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bediener, Eg_location, Zimmer, Eg_property, Queasy, Eg_staff, Eg_subtask

def prepare_eg_reprequestcancel_webbl(all_maintask:bool, all_room:bool, user_init:str):
    engid = 0
    groupid = 0
    ci_date = None
    tsource_list = []
    tsubtask_list = []
    tpic_list = []
    tproperty_list = []
    tmaintask_list = []
    troom_list = []
    tstatus_list = []
    tlocation_list = []
    tcategory_list = []
    htparam = bediener = eg_location = zimmer = eg_property = queasy = eg_staff = eg_subtask = None

    tsource = tsubtask = tpic = tproperty = tmaintask = troom = tstatus = tlocation = tcategory = qbuff = qbuff1 = comlocat = commain = comroom = ques = comcategory = None

    tsource_list, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":str, "source_selected":bool})
    tsubtask_list, Tsubtask = create_model("Tsubtask", {"sub_nr":str, "sub_nm":str, "sub_selected":bool})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool, "pic_dept":int})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pmain_nr":int, "pmain":str, "pcateg_nr":int, "pcateg":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool, "categ_nr":int, "categ_nm":str})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":str, "stat_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool}, {"loc_selected": True})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})

    Qbuff = Queasy
    Qbuff1 = Bediener
    Comlocat = Tlocation
    comlocat_list = tlocation_list

    Commain = Tmaintask
    commain_list = tmaintask_list

    Comroom = Troom
    comroom_list = troom_list

    Ques = Queasy
    Comcategory = Tcategory
    comcategory_list = tcategory_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list
        return {"engid": engid, "groupid": groupid, "ci_date": ci_date, "tsource": tsource_list, "tsubtask": tsubtask_list, "tpic": tpic_list, "tproperty": tproperty_list, "tMaintask": tmaintask_list, "troom": troom_list, "tStatus": tstatus_list, "tLocation": tlocation_list, "tcategory": tcategory_list}

    def define_engineering():

        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def create_status():

        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list


        tStatus_list.clear()
        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 1
        tStatus.stat_nm = "New"
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


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 4
        tStatus.stat_nm = "Postponed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 5
        tStatus.stat_nm = "Closed"
        tstatus.stat_selected = False

    def create_location():

        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list


        Qbuff = Eg_location
        tLocation_list.clear()
        tlocation = Tlocation()
        tlocation_list.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = False

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

    def create_room():

        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list

        i:int = 0
        Qbuff = Zimmer
        Qbuff1 = Tlocation
        troom_list.clear()

        qbuff1 = query(qbuff1_list, filters=(lambda qbuff1 :qbuff1.loc_selected  and qbuff1.loc_guest), first=True)

        if qbuff1:

            for qbuff in db_session.query(Qbuff).all():
                troom = Troom()
                troom_list.append(troom)

                troom.room_nm = qbuff.zinr
                troom.room_SELECTED = False


        else:
            pass

    def create_property():

        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list


        Qbuff = Eg_property
        Comlocat = Tlocation
        Commain = Tmaintask
        Comroom = Troom
        Ques = Queasy
        tproperty_list.clear()

        if all_room:

            for troom in query(troom_list):
                troom.room_selected = True

        tproperty = Tproperty()
        tproperty_list.append(tproperty)

        tproperty.prop_nr = 0
        tproperty.prop_nm = "Undefine"

        for comlocat in query(comlocat_list, filters=(lambda comlocat :comlocat.loc_selected)):

            if comlocat.loc_guest :

                for qbuff in db_session.query(Qbuff).filter(
                        (Qbuff.location == comlocat.loc_nr)).all():
                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich + "(" + to_string(qbuff.nr) + ")"
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.KEY == 133) &  (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = db_session.query(Ques).filter(
                                (Ques.key == 132) &  (Ques.number1 == queasy.number2)).first()

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = db_session.query(Eg_location).filter(
                            (Eg_location.nr == qbuff.location)).first()

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


            else:

                for qbuff in db_session.query(Qbuff).filter(
                        (Qbuff.location == comlocat.loc_nr)).all():
                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich + "(" + to_string(qbuff.nr) + ")"
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.KEY == 133) &  (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = db_session.query(Ques).filter(
                                (Ques.key == 132) &  (Ques.number1 == queasy.number2)).first()

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = db_session.query(Eg_location).filter(
                            (Eg_location.nr == qbuff.location)).first()

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""

    def create_pic():

        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list


        Qbuff = Eg_staff
        Qbuff1 = Bediener
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
            tpic.pic_dept = qbuff.usergroup
            tpic.pic_selected = False

    def create_subtask():

        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list


        Qbuff = Eg_subtask
        tsubtask_list.clear()
        tsubtask = Tsubtask()
        tsubtask_list.append(tsubtask)

        tsubtask.sub_nr = "0"
        tsubtask.sub_nm = ""
        tsubtask.sub_selected = False

        if all_maintask:

            for qbuff in db_session.query(Qbuff).all():
                tsubtask = Tsubtask()
                tsubtask_list.append(tsubtask)

                tsubtask.sub_nr = qbuff.sub_code
                tsubtask.sub_nm = qbuff.bezeich
                tsubtask.sub_selected = False


        else:

            for tmaintask in query(tmaintask_list, filters=(lambda tmaintask :tmaintask.main_selected)):

                for qbuff in db_session.query(Qbuff).filter(
                        (Qbuff.main_nr == tmaintask.main_nr)).all():
                    tsubtask = Tsubtask()
                    tsubtask_list.append(tsubtask)

                    tsubtask.sub_nr = qbuff.sub_code
                    tsubtask.sub_nm = qbuff.bezeich
                    tsubtask.sub_selected = False

    def create_source():

        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list


        Qbuff = Queasy
        tsource_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.KEY == 130)).all():
            tsource = Tsource()
            tsource_list.append(tsource)

            tsource.source_nr = qbuff.number1
            tsource.source_nm = qbuff.char1
            tsource.source_selected = False

    def create_category():

        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list


        Qbuff = Queasy
        tcategory_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 132)).all():
            tcategory = Tcategory()
            tcategory_list.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.char1
            tcategory.categ_selected = False

    def create_maintask():

        nonlocal engid, groupid, ci_date, tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list, htparam, bediener, eg_location, zimmer, eg_property, queasy, eg_staff, eg_subtask
        nonlocal qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, qbuff, qbuff1, comlocat, commain, comroom, ques, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tstatus_list, tlocation_list, tcategory_list


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


                tMaintask.categ_nr = comcategory.categ_nr
                tMaintask.categ_nm = comcategory.categ_nm


    define_group()
    define_engineering()
    create_status()
    create_location()
    create_room()
    create_property()
    create_pic()
    create_subtask()
    create_source()
    create_category()

    for tcategory in query(tcategory_list):
        tcategory.categ_selected = True


    create_maintask()

    for tlocation in query(tlocation_list):
        tlocation.loc_selected = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    return generate_output()