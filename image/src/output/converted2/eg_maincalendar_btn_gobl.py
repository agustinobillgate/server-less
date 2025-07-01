#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Htparam, Queasy, Eg_staff, Eg_location, Zimmer, Eg_property

def eg_maincalendar_btn_gobl(user_init:string, all_room:bool):

    prepare_cache ([Bediener, Htparam, Queasy, Eg_location, Eg_property])

    groupid = 0
    engid = 0
    troom_list = []
    tproperty_list = []
    bediener = htparam = queasy = eg_staff = eg_location = zimmer = eg_property = None

    tmaintask = tpic = tstatus = dept_link = tproperty = troom = tlocation = tcategory = comcategory = qbuff1 = comlocat = commain = comroom = None

    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
    dept_link_list, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":string})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    troom_list, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal user_init, all_room


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

        return {"groupid": groupid, "engid": engid, "troom": troom_list, "tproperty": tproperty_list}

    def define_group():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal user_init, all_room


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal user_init, all_room


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def create_related_dept():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal user_init, all_room


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

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

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal user_init, all_room


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list


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

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal user_init, all_room


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

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


    def create_pic():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal user_init, all_room


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

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


    def create_location():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal user_init, all_room


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

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


    def create_maintask():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal user_init, all_room


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

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


    def create_room():

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal user_init, all_room


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

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

        nonlocal groupid, engid, troom_list, tproperty_list, bediener, htparam, queasy, eg_staff, eg_location, zimmer, eg_property
        nonlocal user_init, all_room


        nonlocal tmaintask, tpic, tstatus, dept_link, tproperty, troom, tlocation, tcategory, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal tmaintask_list, tpic_list, tstatus_list, dept_link_list, tproperty_list, troom_list, tlocation_list, tcategory_list

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

        qbuff_obj_list = {}
        for qbuff in db_session.query(Qbuff).filter(
                 ((Qbuff.location.in_(list(set([comlocat.loc_nr for comlocat in comlocat_list if comlocat.loc_selected])))))).order_by(Qbuff._recid).all():
            if qbuff_obj_list.get(qbuff._recid):
                continue
            else:
                qbuff_obj_list[qbuff._recid] = True

            comlocat = query(comlocat_list, (lambda comlocat: (qbuff.location == comlocat.loc_nr)), first=True)

            if comlocat.loc_guest :

                commain = query(commain_list, filters=(lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)

                if commain:

                    comroom = query(comroom_list, filters=(lambda comroom: comroom.room_nm == qbuff.zinr and comroom.room_selected), first=True)

                    if comroom:
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

                commain = query(commain_list, filters=(lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)

                if commain:
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