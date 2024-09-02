from functions.additional_functions import *
import decimal
from datetime import date
from functions.htplogic import htplogic
from sqlalchemy import func
from models import Eg_action, Bediener, Htparam, Queasy, Eg_location, Zimmer, Eg_property, Eg_staff, Eg_mdetail, Eg_maintain

def prepare_eg_maincalendar_webbl(user_init:str, all_room:bool, mm:int, yy:int):
    groupid = 0
    engid = 0
    p_992 = False
    troom_list = []
    tproperty_list = []
    tstatus_list = []
    tcategory_list = []
    smaintain_list = []
    tpic_list = []
    tlocation_list = []
    dept_link_list = []
    tmaintask_list = []
    action_list = []
    eg_action = bediener = htparam = queasy = eg_location = zimmer = eg_property = eg_staff = eg_mdetail = eg_maintain = None

    smaintain = action = maintain = tpic = tproperty = troom = tcategory = tlocation = dept_link = tstatus = tmaintask = qbuff = comcategory = qbuff1 = comlocat = commain = comroom = ques = buff_maintain = buff_mdetail = buff_action = comproperty = comstatus = compic = commaintask = comlocation = None

    smaintain_list, Smaintain = create_model("Smaintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "stat_nr":int, "stat_nm":str, "categ_nr":int, "categ_nm":str, "main_nr":int, "main_nm":str, "loc_nr":int, "loc_nm":str, "prop_nr":int, "prop_nm":str, "pzinr":str, "pic_nr":int, "pic_nm":str, "str":str, "rec":str, "task_nr":int, "task_nm":str})
    action_list, Action = create_model_like(Eg_action, {"maintainnr":int})
    maintain_list, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":str, "propertynr":int, "pic":int})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool, "pic_dept":int})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pcateg_nr":int, "pcateg":str, "pmain_nr":int, "pmain":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})
    dept_link_list, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":str})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":str, "stat_selected":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool})

    Qbuff = Eg_staff
    Comcategory = Tcategory
    comcategory_list = tcategory_list

    Qbuff1 = Bediener
    Comlocat = Tlocation
    comlocat_list = tlocation_list

    Commain = Tmaintask
    commain_list = tmaintask_list

    Comroom = Troom
    comroom_list = troom_list

    Ques = Queasy
    Buff_maintain = Maintain
    buff_maintain_list = maintain_list

    Buff_mdetail = Eg_mdetail
    Buff_action = Eg_action
    Comproperty = Tproperty
    comproperty_list = tproperty_list

    Comstatus = Tstatus
    comstatus_list = tstatus_list

    Compic = Tpic
    compic_list = tpic_list

    Commaintask = Tmaintask
    commaintask_list = tmaintask_list

    Comlocation = Tlocation
    comlocation_list = tlocation_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list
        return {"groupid": groupid, "engid": engid, "p_992": p_992, "troom": troom_list, "tproperty": tproperty_list, "tStatus": tstatus_list, "tcategory": tcategory_list, "smaintain": smaintain_list, "tpic": tpic_list, "tLocation": tlocation_list, "dept-link": dept_link_list, "tMaintask": tmaintask_list, "action": action_list}

    def define_group():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def define_engineering():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def create_related_dept():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

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

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list


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

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list


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

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list


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

    def create_location():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list


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

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

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

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list


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

                qbuff_obj_list = []
                for qbuff, commain, comroom in db_session.query(Qbuff, Commain, Comroom).join(Commain,(Commain.main_nr == Qbuff.maintask) &  (Commain.main_selected)).join(Comroom,(Comroom.room_nm == Qbuff.zinr) &  (Comroom.room_selected)).filter(
                        (Qbuff.location == comlocat.loc_nr)).all():
                    if qbuff._recid in qbuff_obj_list:
                        continue
                    else:
                        qbuff_obj_list.append(qbuff._recid)


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

                qbuff_obj_list = []
                for qbuff, commain in db_session.query(Qbuff, Commain).join(Commain,(Commain.main_nr == Qbuff.maintask) &  (Commain.main_selected)).filter(
                        (Qbuff.location == comlocat.loc_nr)).all():
                    if qbuff._recid in qbuff_obj_list:
                        continue
                    else:
                        qbuff_obj_list.append(qbuff._recid)


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

    def create_pic():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list


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

    def create_smaintain():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques, buff_maintain, buff_mdetail, buff_action, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list


        Buff_maintain = Maintain
        Buff_mdetail = Eg_mdetail
        Buff_action = Eg_action
        Comproperty = Tproperty
        Comstatus = Tstatus
        Compic = Tpic
        Commaintask = Tmaintask
        Comlocation = Tlocation
        Ques = Queasy
        smaintain_list.clear()

        eg_maintain_obj_list = []
        for eg_maintain, comstatus, eg_location, eg_property, eg_staff in db_session.query(Eg_maintain, Comstatus, Eg_location, Eg_property, Eg_staff).join(Comstatus,(Comstatus.stat_nr == Eg_maintain.TYPE)).join(Eg_location,(Eg_location.nr == Eg_maintain.location)).join(Eg_property,(Eg_property.nr == Eg_maintain.propertynr)).join(Eg_staff,(Eg_staff.nr == Eg_maintain.pic)).filter(
                (get_month(Eg_maintain.estworkdate) == mm) &  (get_year(Eg_maintain.estworkdate) == yy) &  (Eg_maintain.delete_flag == False)).all():
            if eg_maintain._recid in eg_maintain_obj_list:
                continue
            else:
                eg_maintain_obj_list.append(eg_maintain._recid)


            smaintain = Smaintain()
            smaintain_list.append(smaintain)


            eg_mdetail_obj_list = []
            for eg_mdetail, eg_action in db_session.query(Eg_mdetail, Eg_action).join(Eg_action,(Eg_action.actionnr == Eg_mdetail.nr)).filter(
                    (Eg_mdetail.KEY == 1) &  (Eg_mdetail.maintainnr == eg_maintain.maintainnr)).all():
                if eg_mdetail._recid in eg_mdetail_obj_list:
                    continue
                else:
                    eg_mdetail_obj_list.append(eg_mdetail._recid)


                smaintain.task_nr = eg_mdetail.nr
                smaintain.task_nm = smaintain.task_nm + eg_action.bezeich + ","


            smaintain.task_nm = substring(smaintain.task_nm, 0, len(smaintain.task_nm) - 1)
            smaintain.maintainnr = eg_maintain.maintainnr
            smaintain.workdate = eg_maintain.workdate
            smaintain.estworkdate = eg_maintain.estworkdate
            smaintain.stat_nr = eg_maintain.TYPE
            smaintain.stat_nm = comstatus.stat_nm
            smaintain.loc_nr = eg_location.nr
            smaintain.loc_nm = eg_location.bezeich
            smaintain.prop_nr = eg_property.nr
            smaintain.prop_nm = eg_property.bezeich
            smaintain.pzinr = eg_maintain.zinr
            smaintain.pic_nr = eg_staff.nr
            smaintain.pic_nm = eg_staff.name

            queasy = db_session.query(Queasy).filter(
                    (Queasy.KEY == 133) &  (Queasy.number1 == eg_property.maintask)).first()

            if queasy:
                smaintain.main_nm = queasy.char1
                smaintain.main_nr = queasy.number1

                ques = db_session.query(Ques).filter(
                        (Ques.key == 132) &  (Ques.number1 == queasy.number2)).first()

                if ques:
                    smaintain.categ_nm = ques.char1
                    smaintain.categ_nr = ques.number1


    p_992 = get_output(htplogic(992))
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
    create_smaintain()

    return generate_output()