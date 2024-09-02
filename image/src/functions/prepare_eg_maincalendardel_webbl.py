from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from sqlalchemy import func
from models import Zimmer, Eg_maintain, Bediener, Htparam, Queasy, Eg_staff, Eg_location, Eg_property

def prepare_eg_maincalendardel_webbl(user_init:str, all_room:bool):
    groupid = 0
    engid = 0
    p_992 = False
    maintain_list = []
    tproperty_list = []
    troom_list = []
    tmaintask_list = []
    tpic_list = []
    tstatus_list = []
    dept_link_list = []
    tlocation_list = []
    tcategory_list = []
    t_eg_maintain_list = []
    t_zimmer_list = []
    ci_date:date = None
    zimmer = eg_maintain = bediener = htparam = queasy = eg_staff = eg_location = eg_property = None

    t_zimmer = maintain = tproperty = troom = tmaintask = tpic = tstatus = dept_link = tlocation = tcategory = t_eg_maintain = qbuff = qbuff1 = comcategory = comlocat = commain = comroom = ques = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer)
    maintain_list, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":str, "propertynr":int, "pic":int, "cancel_date":date, "cancel_time":int, "cancel_str":str, "cancel_by":str, "categnr":int})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pcateg_nr":int, "pcateg":str, "pmain_nr":int, "pmain":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "categ_nr":int, "categ_nm":str, "main_selected":bool})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool, "pic_dept":int})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":str, "stat_selected":bool})
    dept_link_list, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":str})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})
    t_eg_maintain_list, T_eg_maintain = create_model_like(Eg_maintain)

    Qbuff = Eg_maintain
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
        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list
        return {"groupid": groupid, "engid": engid, "p_992": p_992, "maintain": maintain_list, "tproperty": tproperty_list, "troom": troom_list, "tMaintask": tmaintask_list, "tpic": tpic_list, "tStatus": tstatus_list, "dept-link": dept_link_list, "tLocation": tlocation_list, "tcategory": tcategory_list, "t-eg-maintain": t_eg_maintain_list, "t-zimmer": t_zimmer_list}

    def define_group():

        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def define_engineering():

        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def create_related_dept():

        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list

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

        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list


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

        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list


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

        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list


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

        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list


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

        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list


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
                tMaintask.categ_nr = comcategory.categ_nr
                tMaintask.categ_nm = comcategory.categ_nm
                tmaintask.main_selected = True

    def create_room():

        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list

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

        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list


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

    def create_maintain():

        nonlocal groupid, engid, p_992, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list, t_zimmer_list, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, qbuff, qbuff1, comcategory, comlocat, commain, comroom, ques
        nonlocal t_zimmer_list, maintain_list, tproperty_list, troom_list, tmaintask_list, tpic_list, tstatus_list, dept_link_list, tlocation_list, tcategory_list, t_eg_maintain_list

        strdatetime:str = ""
        ex_finishstr:str = ""
        cancelstr:str = ""
        Qbuff = Eg_maintain
        maintain_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.delete_flag) &  (Qbuff.cancel_date == ci_date)).all():
            cancelstr = to_string(qbuff.cancel_date , "99/99/99") + " " + to_string(qbuff.cancel_time , "HH:MM")

            if qbuff.propertynr != 0:

                tproperty = query(tproperty_list, filters=(lambda tproperty :tproperty.prop_nr == qbuff.propertynr), first=True)

                if tproperty:
                    maintain = Maintain()
                    maintain_list.append(maintain)

                    maintain.maintainnr = qbuff.maintainnr
                    maintain.workdate = qbuff.workdate
                    maintain.estworkdate = qbuff.estworkdate
                    maintain.donedate = qbuff.donedate
                    maintain.TYPE = qbuff.TYPE
                    maintain.maintask = tproperty.pmain_nr
                    maintain.location = tproperty.ploc_nr
                    maintain.propertynr = qbuff.propertynr
                    maintain.pic = qbuff.pic
                    maintain.cancel_date = qbuff.cancel_date
                    maintain.cancel_time = qbuff.cancel_time
                    maintain.cancel_str = cancelstr
                    maintain.cancel_by = qbuff.cancel_by


                else:
                    pass
            else:
                maintain = Maintain()
                maintain_list.append(maintain)

                maintain.maintainnr = qbuff.maintainnr
                maintain.workdate = qbuff.workdate
                maintain.estworkdate = qbuff.estworkdate
                maintain.donedate = qbuff.donedate
                maintain.TYPE = qbuff.TYPE
                maintain.maintask = tproperty.pmain_nr
                maintain.location = qbuff.location
                maintain.zinr = qbuff.zinr
                maintain.propertynr = qbuff.propertynr
                maintain.pic = qbuff.pic
                maintain.cancel_date = qbuff.cancel_date
                maintain.cancel_time = qbuff.cancel_time
                maintain.cancel_str = cancelstr
                maintain.cancel_by = qbuff.cancel_by


    ci_date = get_output(htpdate(87))
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
    create_maintain()

    for eg_maintain in db_session.query(Eg_maintain).all():
        t_eg_maintain = T_eg_maintain()
        t_eg_maintain_list.append(t_eg_maintain)

        buffer_copy(eg_maintain, t_eg_maintain)

    for zimmer in db_session.query(Zimmer).all():
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)

    return generate_output()