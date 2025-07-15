#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from models import Zimmer, Eg_maintain, Bediener, Htparam, Queasy, Eg_staff, Eg_location, Eg_property

def eg_maincalendardel_gobl(from_date:date, to_date:date, user_init:string, all_room:bool):

    prepare_cache ([Bediener, Htparam, Queasy, Eg_staff, Eg_location, Eg_property])

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
    zimmer = eg_maintain = bediener = htparam = queasy = eg_staff = eg_location = eg_property = None

    t_zimmer = maintain = tproperty = troom = tmaintask = tpic = tstatus = dept_link = tlocation = tcategory = t_eg_maintain = comcategory = comlocat = commain = comroom = None

    t_zimmer_data, T_zimmer = create_model_like(Zimmer)
    maintain_data, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":string, "propertynr":int, "pic":int, "cancel_date":date, "cancel_time":int, "cancel_str":string, "cancel_by":string, "categnr":int})
    tproperty_data, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
    tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tstatus_data, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
    dept_link_data, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":string})
    tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    t_eg_maintain_data, T_eg_maintain = create_model_like(Eg_maintain)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        return {"groupid": groupid, "engid": engid, "p_992": p_992, "maintain": maintain_data, "tproperty": tproperty_data, "troom": troom_data, "tMaintask": tmaintask_data, "tpic": tpic_data, "tStatus": tstatus_data, "dept-link": dept_link_data, "tLocation": tlocation_data, "tcategory": tcategory_data, "t-eg-maintain": t_eg_maintain_data, "t-zimmer": t_zimmer_data}

    def define_group():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def create_related_dept():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
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

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
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

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
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

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data


        tpic_data.clear()
        tpic = Tpic()
        tpic_data.append(tpic)

        tpic.pic_nr = 0
        tpic.pic_nm = ""
        tpic.pic_selected = False

        for eg_staff in db_session.query(Eg_staff).filter(
                 (Eg_staff.usergroup == engid) & (Eg_staff.activeflag)).order_by(Eg_staff.nr).all():
            tpic = Tpic()
            tpic_data.append(tpic)

            tpic.pic_nr = eg_staff.nr
            tpic.pic_nm = eg_staff.name
            tpic.pic_dept = eg_staff.usergroup
            tpic.pic_selected = False


    def create_location():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data


        tlocation_data.clear()
        tlocation = Tlocation()
        tlocation_data.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = False

        for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():

            if eg_location.guestflag :
                tlocation = Tlocation()
                tlocation_data.append(tlocation)

                tlocation.loc_nr = eg_location.nr
                tlocation.loc_nm = eg_location.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = True


            else:
                tlocation = Tlocation()
                tlocation_data.append(tlocation)

                tlocation.loc_nr = eg_location.nr
                tlocation.loc_nm = eg_location.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = False


    def create_maintask():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
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
                tmaintask.main_selected = True


    def create_room():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        i:int = 0
        troom_data.clear()

        tlocation = query(tlocation_data, filters=(lambda tlocation: tlocation.loc_selected  and tlocation.loc_guest), first=True)

        if tlocation:

            for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
                troom = Troom()
                troom_data.append(troom)

                troom.room_nm = zimmer.zinr
                troom.room_selected = False


        else:
            pass


    def create_property():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        ques = None
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

                eg_property_obj_list = {}
                for eg_property in db_session.query(Eg_property).filter(
                         (Eg_property.location == comlocat.loc_nr)).order_by(Eg_property._recid).all():
                    commain = query(commain_data, (lambda commain: commain.main_nr == eg_property.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    comroom = query(comroom_data, (lambda comroom: comroom.room_nm == eg_property.zinr and comroom.room_selected), first=True)
                    if not comroom:
                        continue

                    if eg_property_obj_list.get(eg_property._recid):
                        continue
                    else:
                        eg_property_obj_list[eg_property._recid] = True


                    tproperty = Tproperty()
                    tproperty_data.append(tproperty)

                    tproperty.prop_nr = eg_property.nr
                    tproperty.prop_nm = eg_property.bezeich + "(" + trim (to_string(eg_property.nr , ">>>>>>9")) + ")"
                    tproperty.pzinr = eg_property.zinr
                    tproperty.pmain_nr = eg_property.maintask
                    tproperty.ploc_nr = eg_property.location

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == eg_property.maintask)).first()

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

                    eg_location = get_cache (Eg_location, {"nr": [(eq, eg_property.location)]})

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


            else:

                eg_property_obj_list = {}
                for eg_property in db_session.query(Eg_property).filter(
                         (Eg_property.location == comlocat.loc_nr)).order_by(Eg_property._recid).all():
                    commain = query(commain_data, (lambda commain: commain.main_nr == eg_property.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    if eg_property_obj_list.get(eg_property._recid):
                        continue
                    else:
                        eg_property_obj_list[eg_property._recid] = True


                    tproperty = Tproperty()
                    tproperty_data.append(tproperty)

                    tproperty.prop_nr = eg_property.nr
                    tproperty.prop_nm = eg_property.bezeich + "(" + trim (to_string(eg_property.nr , ">>>>>>9")) + ")"
                    tproperty.pzinr = eg_property.zinr
                    tproperty.pmain_nr = eg_property.maintask
                    tproperty.ploc_nr = eg_property.location

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == eg_property.maintask)).first()

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

                    eg_location = get_cache (Eg_location, {"nr": [(eq, eg_property.location)]})

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


    def create_maintain():

        nonlocal groupid, engid, p_992, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data, t_zimmer_data, zimmer, eg_maintain, bediener, htparam, queasy, eg_staff, eg_location, eg_property
        nonlocal from_date, to_date, user_init, all_room


        nonlocal t_zimmer, maintain, tproperty, troom, tmaintask, tpic, tstatus, dept_link, tlocation, tcategory, t_eg_maintain, comcategory, comlocat, commain, comroom
        nonlocal t_zimmer_data, maintain_data, tproperty_data, troom_data, tmaintask_data, tpic_data, tstatus_data, dept_link_data, tlocation_data, tcategory_data, t_eg_maintain_data

        quesbuff = None
        quesbuff1 = None
        strdatetime:string = ""
        ex_finishstr:string = ""
        cancelstr:string = ""
        Quesbuff =  create_buffer("Quesbuff",Queasy)
        Quesbuff1 =  create_buffer("Quesbuff1",Queasy)
        maintain_data.clear()

        for eg_maintain in db_session.query(Eg_maintain).filter(
                 (Eg_maintain.delete_flag) & (Eg_maintain.cancel_date >= from_date) & (Eg_maintain.cancel_date <= to_date)).order_by(Eg_maintain._recid).all():
            cancelstr = to_string(eg_maintain.cancel_date , "99/99/99") + " " + to_string(eg_maintain.cancel_time , "HH:MM")

            if eg_maintain.propertynr != 0:

                tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == eg_maintain.propertynr), first=True)

                if tproperty:
                    maintain = Maintain()
                    maintain_data.append(maintain)

                    maintain.maintainnr = eg_maintain.maintainnr
                    maintain.workdate = eg_maintain.workdate
                    maintain.estworkdate = eg_maintain.estworkdate
                    maintain.donedate = eg_maintain.donedate
                    maintain.type = eg_maintain.type
                    maintain.maintask = tproperty.pmain_nr
                    maintain.location = tproperty.ploc_nr
                    maintain.propertynr = eg_maintain.propertynr
                    maintain.pic = eg_maintain.pic
                    maintain.cancel_date = eg_maintain.cancel_date
                    maintain.cancel_time = eg_maintain.cancel_time
                    maintain.cancel_str = cancelstr
                    maintain.cancel_by = eg_maintain.cancel_by

                    quesbuff = get_cache (Queasy, {"key": [(eq, 133)],"number1": [(eq, tproperty.pmain_nr)]})

                    if quesbuff:

                        quesbuff1 = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, quesbuff.number2)]})

                        if quesbuff1:
                            maintain.categnr = quesbuff1.number1
                else:
                    pass
            else:
                maintain = Maintain()
                maintain_data.append(maintain)

                maintain.maintainnr = eg_maintain.maintainnr
                maintain.workdate = eg_maintain.workdate
                maintain.estworkdate = eg_maintain.estworkdate
                maintain.donedate = eg_maintain.donedate
                maintain.type = eg_maintain.type
                maintain.maintask = tproperty.pmain_nr
                maintain.location = eg_maintain.location
                maintain.zinr = eg_maintain.zinr
                maintain.propertynr = eg_maintain.propertynr
                maintain.pic = eg_maintain.pic
                maintain.cancel_date = eg_maintain.cancel_date
                maintain.cancel_time = eg_maintain.cancel_time
                maintain.cancel_str = cancelstr
                maintain.cancel_by = eg_maintain.cancel_by

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