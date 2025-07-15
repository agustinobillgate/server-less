#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener, Eg_location, Zimmer, Queasy, Eg_property, Eg_staff, Eg_subtask

def prepare_eg_reprequestcancel_webbl(all_maintask:bool, all_room:bool, user_init:string):

    prepare_cache ([Htparam, Bediener, Eg_location, Zimmer, Queasy, Eg_property, Eg_staff, Eg_subtask])

    engid = 0
    groupid = 0
    ci_date = None
    tsource_data = []
    tsubtask_data = []
    tpic_data = []
    tproperty_data = []
    tmaintask_data = []
    troom_data = []
    tstatus_data = []
    tlocation_data = []
    tcategory_data = []
    htparam = bediener = eg_location = zimmer = queasy = eg_property = eg_staff = eg_subtask = None

    tsource = tsubtask = tpic = tproperty = tmaintask = troom = tstatus = tlocation = tcategory = comlocat = commain = comroom = comcategory = None

    tsource_data, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":string, "source_selected":bool})
    tsubtask_data, Tsubtask = create_model("Tsubtask", {"sub_nr":string, "sub_nm":string, "sub_selected":bool})
    tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tproperty_data, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pmain_nr":int, "pmain":string, "pcateg_nr":int, "pcateg":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool, "categ_nr":int, "categ_nm":string})
    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tstatus_data, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
    tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool}, {"loc_selected": True})
    tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data

        return {"engid": engid, "groupid": groupid, "ci_date": ci_date, "tsource": tsource_data, "tsubtask": tsubtask_data, "tpic": tpic_data, "tproperty": tproperty_data, "tMaintask": tmaintask_data, "troom": troom_data, "tStatus": tstatus_data, "tLocation": tlocation_data, "tcategory": tcategory_data}

    def define_engineering():

        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def create_status():

        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data


        tstatus_data.clear()
        tstatus = Tstatus()
        tstatus_data.append(tstatus)

        tstatus.stat_nr = 1
        tstatus.stat_nm = "New"
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


        tstatus = Tstatus()
        tstatus_data.append(tstatus)

        tstatus.stat_nr = 4
        tstatus.stat_nm = "Postponed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_data.append(tstatus)

        tstatus.stat_nr = 5
        tstatus.stat_nm = "Closed"
        tstatus.stat_selected = False


    def create_location():

        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data


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


    def create_room():

        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data

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

        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data

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

                for eg_property in db_session.query(Eg_property).filter(
                         (Eg_property.location == comlocat.loc_nr)).order_by(Eg_property._recid).all():
                    tproperty = Tproperty()
                    tproperty_data.append(tproperty)

                    tproperty.prop_nr = eg_property.nr
                    tproperty.prop_nm = eg_property.bezeich + "(" + to_string(eg_property.nr) + ")"
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

                for eg_property in db_session.query(Eg_property).filter(
                         (Eg_property.location == comlocat.loc_nr)).order_by(Eg_property._recid).all():
                    tproperty = Tproperty()
                    tproperty_data.append(tproperty)

                    tproperty.prop_nr = eg_property.nr
                    tproperty.prop_nm = eg_property.bezeich + "(" + to_string(eg_property.nr) + ")"
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


    def create_pic():

        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data


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


    def create_subtask():

        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data


        tsubtask_data.clear()
        tsubtask = Tsubtask()
        tsubtask_data.append(tsubtask)

        tsubtask.sub_nr = "0"
        tsubtask.sub_nm = ""
        tsubtask.sub_selected = False

        if all_maintask:

            for eg_subtask in db_session.query(Eg_subtask).order_by(Eg_subtask._recid).all():
                tsubtask = Tsubtask()
                tsubtask_data.append(tsubtask)

                tsubtask.sub_nr = eg_subtask.sub_code
                tsubtask.sub_nm = eg_subtask.bezeich
                tsubtask.sub_selected = False


        else:

            for tmaintask in query(tmaintask_data, filters=(lambda tmaintask: tmaintask.main_selected)):

                for eg_subtask in db_session.query(Eg_subtask).filter(
                         (Eg_subtask.main_nr == tmaintask.main_nr)).order_by(Eg_subtask._recid).all():
                    tsubtask = Tsubtask()
                    tsubtask_data.append(tsubtask)

                    tsubtask.sub_nr = eg_subtask.sub_code
                    tsubtask.sub_nm = eg_subtask.bezeich
                    tsubtask.sub_selected = False


    def create_source():

        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        tsource_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 130)).order_by(Qbuff._recid).all():
            tsource = Tsource()
            tsource_data.append(tsource)

            tsource.source_nr = qbuff.number1
            tsource.source_nm = qbuff.char1
            tsource.source_selected = False


    def create_category():

        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data

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


    def create_maintask():

        nonlocal engid, groupid, ci_date, tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data, htparam, bediener, eg_location, zimmer, queasy, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tstatus, tlocation, tcategory, comlocat, commain, comroom, comcategory
        nonlocal tsource_data, tsubtask_data, tpic_data, tproperty_data, tmaintask_data, troom_data, tstatus_data, tlocation_data, tcategory_data

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


                tmaintask.categ_nr = comcategory.categ_nr
                tmaintask.categ_nm = comcategory.categ_nm

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

    for tcategory in query(tcategory_data):
        tcategory.categ_selected = True


    create_maintask()

    for tlocation in query(tlocation_data):
        tlocation.loc_selected = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    return generate_output()