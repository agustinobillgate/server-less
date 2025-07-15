#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from models import Zimmer, Eg_maintain, Bediener, Htparam, Queasy, Eg_staff, Eg_location, Eg_property

def prepare_eg_maincalendardel_webbl(user_init:string, all_room:bool):

    prepare_cache ([Eg_maintain, Bediener, Htparam, Queasy, Eg_location])

    groupid = 0
    engid = 0
    p_992 = False
    maintain_data = []
    tproperty_data = []
    troom_data = []
    tmaintask_data = []
    tpic_data = []
    tstatus_data = []
    dept_link_data = []
    tlocation_data = []
    tcategory_data = []
    t_eg_maintain_data = []
    t_zimmer_data = []
    ci_date:date = None
    zimmer = eg_maintain = bediener = htparam = queasy = eg_staff = eg_location = eg_property = None

    t_zimmer = maintain = tproperty = troom = tmaintask = tpic = tstatus = dept_link = tlocation = tcategory = t_eg_maintain = comcategory = qbuff1 = comlocat = commain = comroom = None

    t_zimmer_data, T_zimmer = create_model_like(Zimmer)
    maintain_data, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":string, "propertynr":int, "pic":int, "cancel_date":date, "cancel_time":int, "cancel_str":string, "cancel_by":string, "categnr":int})
    tproperty_data, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "categ_nr":int, "categ_nm":string, "main_selected":bool})
    tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tstatus_data, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
    dept_link_data, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":string})
    tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    t_eg_maintain_data, T_eg_maintain = create_model_like(Eg_maintain)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        return {"groupid": groupid, "engid": engid, "p_992": p_992, "maintain": maintain_data, "tproperty": tproperty_data, "troom": troom_data, "tMaintask": tmaintask_data, "tpic": tpic_data, "tStatus": tstatus_data, "dept-link": dept_link_data, "tLocation": tlocation_data, "tcategory": tcategory_data, "t-eg-maintain": t_eg_maintain_data, "t-zimmer": t_zimmer_data}

    def define_group():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def create_related_dept():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        i:int = 0
        c:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        dept_link_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, engid)]})

        if queasy:
            dept_link = Dept_link()
            dept_link_data.append(dept_link)

            dept_link.dept_nr = engid
            dept_link.dept_nm = queasy.char3


            for i in range(1,num_entries(queasy.char2, ";")  + 1) :
                c = to_int(entry(i - 1, queasy.char2, ";"))

                qbuff = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, to_int(entry(i - 1, queasy.char2, ";")))]})

                if qbuff:
                    dept_link = Dept_link()
                    dept_link_data.append(dept_link)

                    dept_link.dept_nr = c
                    dept_link.dept_nm = qbuff.char3


    def create_status():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data


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


    def create_category():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

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


    def create_pic():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        qbuff = None
        qbuff1 = None
        Qbuff =  create_buffer("Qbuff",Eg_staff)
        Qbuff1 =  create_buffer("Qbuff1",Bediener)
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
            tpic.pic_dept = qbuff.usergroup
            tpic.pic_selected = False


    def create_location():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_location)
        tlocation_data.clear()
        tlocation = Tlocation()
        tlocation_data.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = False

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

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

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
                tmaintask.categ_nr = comcategory.categ_nr
                tmaintask.categ_nm = comcategory.categ_nm
                tmaintask.main_selected = True


    def create_room():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        i:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Zimmer)
        Qbuff1 = Tlocation
        qbuff1_data = tlocation_data
        troom_data.clear()

        qbuff1 = query(qbuff1_data, filters=(lambda qbuff1: qbuff1.loc_selected  and qbuff1.loc_guest), first=True)

        if qbuff1:

            for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
                troom = Troom()
                troom_data.append(troom)

                troom.room_nm = qbuff.zinr
                troom.room_selected = False


        else:
            pass


    def create_property():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        qbuff = None
        ques = None
        Qbuff =  create_buffer("Qbuff",Eg_property)
        Comlocat = Tlocation
        comlocat_data = tlocation_data
        Commain = Tmaintask
        commain_data = tmaintask_data
        Comroom = Troom
        comroom_data = troom_data
        Ques =  create_buffer("Ques",Queasy)
        tproperty_data.clear()

        if all_room:

            for troom in query(troom_data):
                troom.room_selected = True

        tproperty = Tproperty()
        tproperty_data.append(tproperty)

        tproperty.prop_nr = 0
        tproperty.prop_nm = "Undefine"

        for comlocat in query(comlocat_data, filters=(lambda comlocat: comlocat.loc_selected)):

            if comlocat.loc_guest :

                qbuff_obj_list = {}
                for qbuff in db_session.query(Qbuff).filter(
                         (Qbuff.location == comlocat.loc_nr)).order_by(Qbuff._recid).all():
                    commain = query(commain_data, (lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    comroom = query(comroom_data, (lambda comroom: comroom.room_nm == qbuff.zinr and comroom.room_selected), first=True)
                    if not comroom:
                        continue

                    if qbuff_obj_list.get(qbuff._recid):
                        continue
                    else:
                        qbuff_obj_list[qbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_data.append(tproperty)

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
                    commain = query(commain_data, (lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    if qbuff_obj_list.get(qbuff._recid):
                        continue
                    else:
                        qbuff_obj_list[qbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_data.append(tproperty)

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


    def create_maintain():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, ci_date, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        qbuff = None
        strdatetime:string = ""
        ex_finishstr:string = ""
        cancelstr:string = ""
        Qbuff =  create_buffer("Qbuff",Eg_maintain)
        maintain_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.delete_flag) & (Qbuff.cancel_date == ci_date)).order_by(Qbuff._recid).all():
            cancelstr = to_string(qbuff.cancel_date , "99/99/99") + " " + to_string(qbuff.cancel_time , "HH:MM")

            if qbuff.propertynr != 0:

                tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == qbuff.propertynr), first=True)

                if tproperty:
                    maintain = Maintain()
                    maintain_data.append(maintain)

                    maintain.maintainnr = qbuff.maintainnr
                    maintain.workdate = qbuff.workdate
                    maintain.estworkdate = qbuff.estworkdate
                    maintain.donedate = qbuff.donedate
                    maintain.type = qbuff.type
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
                maintain_data.append(maintain)

                maintain.maintainnr = qbuff.maintainnr
                maintain.workdate = qbuff.workdate
                maintain.estworkdate = qbuff.estworkdate
                maintain.donedate = qbuff.donedate
                maintain.type = qbuff.type
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

    for tcategory in query(tcategory_data):
        tcategory.categ_selected = True


    create_maintask()

    for tlocation in query(tlocation_data):
        tlocation.loc_selected = True


    create_room()
    create_property()
    create_maintain()

    for eg_maintain in db_session.query(Eg_maintain).order_by(Eg_maintain._recid).all():
        t_eg_maintain = T_eg_maintain()
        t_eg_maintain_data.append(t_eg_maintain)

        buffer_copy(eg_maintain, t_eg_maintain)

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        t_zimmer = T_zimmer()
        t_zimmer_data.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)

    return generate_output()