from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Htparam, Queasy, Eg_staff, Eg_location, Zimmer, Eg_property

def eg_maincalendar_btn_gobl(user_init:str, all_room:bool):
    groupid = 0
    engid = 0
    troom_list = []
    tproperty_list = []
    bediener = htparam = queasy = eg_staff = eg_location = zimmer = eg_property = None

    tmaintask = tpic = tstatus = dept_link = tproperty = troom = tlocation = tcategory = qbuff = qbuff1 = comcategory = comlocat = commain = comroom = ques = None

    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool, "pic_dept":int})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":str, "stat_selected":bool})
    dept_link_list, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":str})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pcateg_nr":int, "pcateg":str, "pmain_nr":int, "pmain":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})

    Qbuff = Eg_property
    Qbuff1 = Tlocation
    qbuff1_list = tlocation_list

    Comcategory = Tcategory
    comcategory_list = tcategory_list

    Comlocat = Tlocation
    comlocat_list = tlocation_list

    Commain = Tmaintask
    commain_list = tmaintask_list

    Comroom = Troom
    comroom_list = troom_list

    Ques = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list
        return {"groupid": groupid, "engid": engid, "troom": troom_list, "tproperty": tproperty_list}

    def define_group():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def define_engineering():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def create_related_dept():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

        i:int = 0
        c:int = 0
        Qbuff = Queasy
        dept_link_list.clear()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 19) &  (Queasy.number1 == engid)).first()

        if queasy:
            dept_link = Dept_link()
            dept_link_list.append(dept_link)

            dept_link.dept_nr = engid
            dept_link.dept_nm = queasy.char3


            for i in range(1,num_entries(queasy.char2, ";")  + 1) :
                c = to_int(entry(i - 1, queasy.char2, ";"))

                qbuff = db_session.query(Qbuff).filter(
                        (Qbuff.key == 19) &  (Qbuff.number1 == to_int(entry(i - 1, queasy.char2, ";")))).first()

                if qbuff:
                    dept_link = Dept_link()
                    dept_link_list.append(dept_link)

                    dept_link.dept_nr = c
                    dept_link.dept_nm = qbuff.char3

    def create_status():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list


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

    def create_category():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list


        Qbuff = Queasy
        tcategory_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 132)).all():
            tcategory = Tcategory()
            tcategory_list.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.char1
            tcategory.categ_selected = False

    def create_pic():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list


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

    def create_location():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list


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

    def create_maintask():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list


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

    def create_room():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

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

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list


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
            qbuff = db_session.query(Qbuff).filter((Qbuff.location == comlocat.loc_nr)).first()
            if not qbuff:
                continue


            if comlocat.loc_guest :

                commain = query(commain_list, filters=(lambda commain :commain.main_nr == qbuff.maintask and commain.main_selected), first=True)

                if commain:

                    comroom = query(comroom_list, filters=(lambda comroom :comroom.room_nm == qbuff.zinr and comroom.room_selected), first=True)

                    if comroom:
                        tproperty = Tproperty()
                        tproperty_list.append(tproperty)

                        tproperty.prop_nr = qbuff.nr
                        tproperty.prop_nm = qbuff.bezeich + "(" + trim (to_string(qbuff.nr , ">>>>>>9")) + ")"
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

                commain = query(commain_list, filters=(lambda commain :commain.main_nr == qbuff.maintask and commain.main_selected), first=True)

                if commain:
                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich
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

    define_engineering()
    define_group()
    create_related_dept()
    create_status()
    create_category()
    create_pic()
    create_location()

    for tcategory in query(tcategory_list):
        tcategory.categ_selected = True


    create_maintask()

    for tlocation in query(tlocation_list):
        tlocation.loc_selected = True


    create_room()
    create_property()

    return generate_output()