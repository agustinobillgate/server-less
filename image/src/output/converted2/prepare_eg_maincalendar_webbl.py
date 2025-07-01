#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from models import Eg_action, Bediener, Htparam, Queasy, Eg_location, Zimmer, Eg_property, Eg_staff, Eg_mdetail, Eg_maintain

def prepare_eg_maincalendar_webbl(user_init:string, all_room:bool, mm:int, yy:int):

    prepare_cache ([Eg_action, Bediener, Htparam, Queasy, Eg_location, Eg_property, Eg_staff, Eg_mdetail, Eg_maintain])

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

    smaintain = action = maintain = tpic = tproperty = troom = tcategory = tlocation = dept_link = tstatus = tmaintask = comcategory = qbuff1 = comlocat = commain = comroom = buff_maintain = comproperty = comstatus = compic = commaintask = comlocation = None

    smaintain_list, Smaintain = create_model("Smaintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "stat_nr":int, "stat_nm":string, "categ_nr":int, "categ_nm":string, "main_nr":int, "main_nm":string, "loc_nr":int, "loc_nm":string, "prop_nr":int, "prop_nm":string, "pzinr":string, "pic_nr":int, "pic_nm":string, "str":string, "rec":string, "task_nr":int, "task_nm":string})
    action_list, Action = create_model_like(Eg_action, {"maintainnr":int})
    maintain_list, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":string, "propertynr":int, "pic":int})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    troom_list, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    dept_link_list, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":string})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        return {"groupid": groupid, "engid": engid, "p_992": p_992, "troom": troom_list, "tproperty": tproperty_list, "tStatus": tstatus_list, "tcategory": tcategory_list, "smaintain": smaintain_list, "tpic": tpic_list, "tLocation": tlocation_list, "dept-link": dept_link_list, "tMaintask": tmaintask_list, "action": action_list}

    def define_group():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def create_related_dept():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        i:int = 0
        c:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        dept_link_list.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, engid)]})

        if queasy:
            dept_link = Dept_link()
            dept_link_list.append(dept_link)

            dept_link.dept_nr = engid
            dept_link.dept_nm = queasy.char3


            for i in range(1,num_entries(queasy.char2, ";")  + 1) :
                c = to_int(entry(i - 1, queasy.char2, ";"))

                qbuff = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, to_int(entry(i - 1, queasy.char2, ";")))]})

                if qbuff:
                    dept_link = Dept_link()
                    dept_link_list.append(dept_link)

                    dept_link.dept_nr = c
                    dept_link.dept_nm = qbuff.char3


    def create_status():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list


        tstatus_list.clear()
        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 1
        tstatus.stat_nm = "Scheduled"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 2
        tstatus.stat_nm = "Processed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 3
        tstatus.stat_nm = "Done"
        tstatus.stat_selected = False


    def create_category():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        tcategory_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 132)).order_by(Qbuff._recid).all():
            tcategory = Tcategory()
            tcategory_list.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.char1
            tcategory.categ_selected = False


    def create_maintask():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        Comcategory = Tcategory
        comcategory_list = tcategory_list
        tmaintask_list.clear()

        for comcategory in query(comcategory_list, filters=(lambda comcategory: comcategory.categ_selected)):

            for qbuff in db_session.query(Qbuff).filter(
                     (Qbuff.key == 133) & (Qbuff.number2 == comcategory.categ_nr)).order_by(Qbuff._recid).all():
                tmaintask = Tmaintask()
                tmaintask_list.append(tmaintask)

                tmaintask.main_nr = qbuff.number1
                tmaintask.main_nm = qbuff.char1
                tmaintask.main_selected = True


    def create_location():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_location)
        tlocation_list.clear()
        tlocation = Tlocation()
        tlocation_list.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = False

        for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():

            if qbuff.guestflag :
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tlocation.loc_nr = qbuff.nr
                tlocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = True


            else:
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tlocation.loc_nr = qbuff.nr
                tlocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = False


    def create_room():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        i:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Zimmer)
        Qbuff1 = Tlocation
        qbuff1_list = tlocation_list
        troom_list.clear()

        qbuff1 = query(qbuff1_list, filters=(lambda qbuff1: qbuff1.loc_selected  and qbuff1.loc_guest), first=True)

        if qbuff1:

            for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
                troom = Troom()
                troom_list.append(troom)

                troom.room_nm = qbuff.zinr
                troom.room_selected = False


        else:
            pass


    def create_property():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        qbuff = None
        ques = None
        Qbuff =  create_buffer("Qbuff",Eg_property)
        Comlocat = Tlocation
        comlocat_list = tlocation_list
        Commain = Tmaintask
        commain_list = tmaintask_list
        Comroom = Troom
        comroom_list = troom_list
        Ques =  create_buffer("Ques",Queasy)
        tproperty_list.clear()

        if all_room:

            for troom in query(troom_list):
                troom.room_selected = True

        tproperty = Tproperty()
        tproperty_list.append(tproperty)

        tproperty.prop_nr = 0
        tproperty.prop_nm = "Undefine"

        for comlocat in query(comlocat_list, filters=(lambda comlocat: comlocat.loc_selected)):

            if comlocat.loc_guest :

                qbuff_obj_list = {}
                for qbuff in db_session.query(Qbuff).filter(
                         (Qbuff.location == comlocat.loc_nr)).order_by(Qbuff._recid).all():
                    commain = query(commain_list, (lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    comroom = query(comroom_list, (lambda comroom: comroom.room_nm == qbuff.zinr and comroom.room_selected), first=True)
                    if not comroom:
                        continue

                    if qbuff_obj_list.get(qbuff._recid):
                        continue
                    else:
                        qbuff_obj_list[qbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich + "(" + trim (to_string(qbuff.nr , ">>>>>>9")) + ")"
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, queasy.number2)]})

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = get_cache (Eg_location, {"nr": [(eq, qbuff.location)]})

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


            else:

                qbuff_obj_list = {}
                for qbuff in db_session.query(Qbuff).filter(
                         (Qbuff.location == comlocat.loc_nr)).order_by(Qbuff._recid).all():
                    commain = query(commain_list, (lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    if qbuff_obj_list.get(qbuff._recid):
                        continue
                    else:
                        qbuff_obj_list[qbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, queasy.number2)]})

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = get_cache (Eg_location, {"nr": [(eq, qbuff.location)]})

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


    def create_pic():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        qbuff = None
        qbuff1 = None
        Qbuff =  create_buffer("Qbuff",Eg_staff)
        Qbuff1 =  create_buffer("Qbuff1",Bediener)
        tpic_list.clear()
        tpic = Tpic()
        tpic_list.append(tpic)

        tpic.pic_nr = 0
        tpic.pic_nm = ""
        tpic.pic_selected = False

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.usergroup == engid) & (Qbuff.activeflag)).order_by(Qbuff.nr).all():
            tpic = Tpic()
            tpic_list.append(tpic)

            tpic.pic_nr = qbuff.nr
            tpic.pic_nm = qbuff.name
            tpic.pic_dept = qbuff.usergroup
            tpic.pic_selected = False


    def create_smaintain():

        nonlocal groupid, engid, p_992, troom_list, tproperty_list, tstatus_list, tcategory_list, smaintain_list, tpic_list, tlocation_list, dept_link_list, tmaintask_list, action_list, eg_action, bediener, htparam, queasy, eg_location, zimmer, eg_property, eg_staff, eg_mdetail, eg_maintain
        nonlocal user_init, all_room, mm, yy


        nonlocal smaintain, action, maintain, tpic, tproperty, troom, tcategory, tlocation, dept_link, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom, buff_maintain, comproperty, comstatus, compic, commaintask, comlocation
        nonlocal smaintain_list, action_list, maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, dept_link_list, tstatus_list, tmaintask_list

        buff_mdetail = None
        buff_action = None
        ques = None
        Buff_maintain = Maintain
        buff_maintain_list = maintain_list
        Buff_mdetail =  create_buffer("Buff_mdetail",Eg_mdetail)
        Buff_action =  create_buffer("Buff_action",Eg_action)
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
        Ques =  create_buffer("Ques",Queasy)
        smaintain_list.clear()

        eg_maintain_obj_list = {}
        for eg_maintain, eg_location, eg_property, eg_staff in db_session.query(Eg_maintain, Eg_location, Eg_property, Eg_staff).join(Eg_location,(Eg_location.nr == Eg_maintain.location)).join(Eg_property,(Eg_property.nr == Eg_maintain.propertynr)).join(Eg_staff,(Eg_staff.nr == Eg_maintain.pic)).filter(
                 (get_month(Eg_maintain.estworkdate) == mm) & (get_year(Eg_maintain.estworkdate) == yy) & (Eg_maintain.delete_flag == False)).order_by(Eg_maintain._recid).all():
            comstatus = query(comstatus_list, (lambda comstatus: comstatus.stat_nr == eg_maintain.type), first=True)
            if not comstatus:
                continue

            if eg_maintain_obj_list.get(eg_maintain._recid):
                continue
            else:
                eg_maintain_obj_list[eg_maintain._recid] = True


            smaintain = Smaintain()
            smaintain_list.append(smaintain)


            eg_mdetail_obj_list = {}
            eg_mdetail = Eg_mdetail()
            eg_action = Eg_action()
            for eg_mdetail.nr, eg_mdetail._recid, eg_action.bezeich, eg_action._recid in db_session.query(Eg_mdetail.nr, Eg_mdetail._recid, Eg_action.bezeich, Eg_action._recid).join(Eg_action,(Eg_action.actionnr == Eg_mdetail.nr)).filter(
                     (Eg_mdetail.key == 1) & (Eg_mdetail.maintainnr == eg_maintain.maintainnr)).order_by(Eg_mdetail._recid).all():
                if eg_mdetail_obj_list.get(eg_mdetail._recid):
                    continue
                else:
                    eg_mdetail_obj_list[eg_mdetail._recid] = True


                smaintain.task_nr = eg_mdetail.nr
                smaintain.task_nm = smaintain.task_nm + eg_action.bezeich + ","


            smaintain.task_nm = substring(smaintain.task_nm, 0, length(smaintain.task_nm) - 1)
            smaintain.maintainnr = eg_maintain.maintainnr
            smaintain.workdate = eg_maintain.workdate
            smaintain.estworkdate = eg_maintain.estworkdate
            smaintain.stat_nr = eg_maintain.type
            smaintain.stat_nm = comstatus.stat_nm
            smaintain.loc_nr = eg_location.nr
            smaintain.loc_nm = eg_location.bezeich
            smaintain.prop_nr = eg_property.nr
            smaintain.prop_nm = eg_property.bezeich
            smaintain.pzinr = eg_maintain.zinr
            smaintain.pic_nr = eg_staff.nr
            smaintain.pic_nm = eg_staff.name

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 133) & (Queasy.number1 == eg_property.maintask)).first()

            if queasy:
                smaintain.main_nm = queasy.char1
                smaintain.main_nr = queasy.number1

                ques = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, queasy.number2)]})

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