#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Bediener, Eg_location, Zimmer, Eg_property, Eg_staff, Eg_subtask

def prepare_eg_repdurationbl(all_maintask:bool, all_room:bool, user_init:string):

    prepare_cache ([Queasy, Htparam, Bediener, Eg_location, Eg_subtask])

    engid = 0
    groupid = 0
    ci_date = None
    tlocation_list = []
    tcategory_list = []
    troom_list = []
    tmaintask_list = []
    tproperty_list = []
    tpic_list = []
    tsubtask_list = []
    tsource_list = []
    queasy = htparam = bediener = eg_location = zimmer = eg_property = eg_staff = eg_subtask = None

    tsource = tsubtask = tpic = tproperty = tmaintask = troom = tlocation = tcategory = qbuff = tbuff = comlocat = commain = comroom = comcategory = None

    tsource_list, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":string, "source_selected":bool})
    tsubtask_list, Tsubtask = create_model("Tsubtask", {"sub_nr":string, "sub_nm":string, "sub_selected":bool})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
    troom_list, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})

    Qbuff = create_buffer("Qbuff",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, ci_date, tlocation_list, tcategory_list, troom_list, tmaintask_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, queasy, htparam, bediener, eg_location, zimmer, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init
        nonlocal qbuff


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tlocation, tcategory, qbuff, tbuff, comlocat, commain, comroom, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tlocation_list, tcategory_list

        return {"engid": engid, "groupid": groupid, "ci_date": ci_date, "tLocation": tlocation_list, "tcategory": tcategory_list, "troom": troom_list, "tMaintask": tmaintask_list, "tproperty": tproperty_list, "tpic": tpic_list, "tsubtask": tsubtask_list, "tsource": tsource_list}

    def define_engineering():

        nonlocal engid, groupid, ci_date, tlocation_list, tcategory_list, troom_list, tmaintask_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, queasy, htparam, bediener, eg_location, zimmer, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init
        nonlocal qbuff


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tlocation, tcategory, qbuff, tbuff, comlocat, commain, comroom, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tlocation_list, tcategory_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal engid, groupid, ci_date, tlocation_list, tcategory_list, troom_list, tmaintask_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, queasy, htparam, bediener, eg_location, zimmer, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init
        nonlocal qbuff


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tlocation, tcategory, qbuff, tbuff, comlocat, commain, comroom, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tlocation_list, tcategory_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def create_location():

        nonlocal engid, groupid, ci_date, tlocation_list, tcategory_list, troom_list, tmaintask_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, queasy, htparam, bediener, eg_location, zimmer, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init
        nonlocal qbuff


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tlocation, tcategory, qbuff, tbuff, comlocat, commain, comroom, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tlocation_list, tcategory_list

        egbuff = None
        Egbuff =  create_buffer("Egbuff",Eg_location)
        tlocation_list.clear()
        tlocation = Tlocation()
        tlocation_list.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = False

        for egbuff in db_session.query(Egbuff).order_by(Egbuff._recid).all():

            if egbuff.guestflag :
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tlocation.loc_nr = egbuff.nr
                tlocation.loc_nm = egbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = True


            else:
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tlocation.loc_nr = egbuff.nr
                tlocation.loc_nm = egbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = False


    def create_room():

        nonlocal engid, groupid, ci_date, tlocation_list, tcategory_list, troom_list, tmaintask_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, queasy, htparam, bediener, eg_location, zimmer, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init
        nonlocal qbuff


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tlocation, tcategory, qbuff, tbuff, comlocat, commain, comroom, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tlocation_list, tcategory_list

        i:int = 0
        zbuff = None
        Zbuff =  create_buffer("Zbuff",Zimmer)
        Tbuff = Tlocation
        tbuff_list = tlocation_list
        troom_list.clear()

        tbuff = query(tbuff_list, filters=(lambda tbuff: tbuff.loc_selected  and tbuff.loc_guest), first=True)

        if tbuff:

            for zbuff in db_session.query(Zbuff).order_by(Zbuff._recid).all():
                troom = Troom()
                troom_list.append(troom)

                troom.room_nm = zbuff.zinr
                troom.room_selected = False


        else:
            pass


    def create_property():

        nonlocal engid, groupid, ci_date, tlocation_list, tcategory_list, troom_list, tmaintask_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, queasy, htparam, bediener, eg_location, zimmer, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init
        nonlocal qbuff


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tlocation, tcategory, qbuff, tbuff, comlocat, commain, comroom, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tlocation_list, tcategory_list

        pbuff = None
        ques = None
        Pbuff =  create_buffer("Pbuff",Eg_property)
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

                pbuff_obj_list = {}
                for pbuff in db_session.query(Pbuff).filter(
                         (Pbuff.location == comlocat.loc_nr)).order_by(Pbuff._recid).all():
                    commain = query(commain_list, (lambda commain: commain.main_nr == pbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    comroom = query(comroom_list, (lambda comroom: comroom.room_nm == pbuff.zinr and comroom.room_selected), first=True)
                    if not comroom:
                        continue

                    if pbuff_obj_list.get(pbuff._recid):
                        continue
                    else:
                        pbuff_obj_list[pbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = pbuff.nr
                    tproperty.prop_nm = pbuff.bezeich + "(" + trim (to_string(pbuff.nr , ">>>>>>9")) + ")"
                    tproperty.pzinr = pbuff.zinr
                    tproperty.pmain_nr = pbuff.maintask
                    tproperty.ploc_nr = pbuff.location

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == pbuff.maintask)).first()

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

                    eg_location = get_cache (Eg_location, {"nr": [(eq, pbuff.location)]})

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


            else:

                pbuff_obj_list = {}
                for pbuff in db_session.query(Pbuff).filter(
                         (Pbuff.location == comlocat.loc_nr)).order_by(Pbuff._recid).all():
                    commain = query(commain_list, (lambda commain: commain.main_nr == pbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    if pbuff_obj_list.get(pbuff._recid):
                        continue
                    else:
                        pbuff_obj_list[pbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = pbuff.nr
                    tproperty.prop_nm = pbuff.bezeich + "(" + trim (to_string(pbuff.nr , ">>>>>>9")) + ")"
                    tproperty.pzinr = pbuff.zinr
                    tproperty.pmain_nr = pbuff.maintask
                    tproperty.ploc_nr = pbuff.location

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == pbuff.maintask)).first()

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

                    eg_location = get_cache (Eg_location, {"nr": [(eq, pbuff.location)]})

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


    def create_pic():

        nonlocal engid, groupid, ci_date, tlocation_list, tcategory_list, troom_list, tmaintask_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, queasy, htparam, bediener, eg_location, zimmer, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init
        nonlocal qbuff


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tlocation, tcategory, qbuff, tbuff, comlocat, commain, comroom, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tlocation_list, tcategory_list

        sbuff = None
        Sbuff =  create_buffer("Sbuff",Eg_staff)
        tpic_list.clear()
        tpic = Tpic()
        tpic_list.append(tpic)

        tpic.pic_nr = 0
        tpic.pic_nm = ""
        tpic.pic_selected = False

        for sbuff in db_session.query(Sbuff).filter(
                 (Sbuff.usergroup == engid) & (Sbuff.activeflag)).order_by(Sbuff.nr).all():
            tpic = Tpic()
            tpic_list.append(tpic)

            tpic.pic_nr = sbuff.nr
            tpic.pic_nm = sbuff.name
            tpic.pic_dept = sbuff.usergroup
            tpic.pic_selected = False


    def create_subtask():

        nonlocal engid, groupid, ci_date, tlocation_list, tcategory_list, troom_list, tmaintask_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, queasy, htparam, bediener, eg_location, zimmer, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init
        nonlocal qbuff


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tlocation, tcategory, qbuff, tbuff, comlocat, commain, comroom, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tlocation_list, tcategory_list


        tsubtask_list.clear()
        tsubtask = Tsubtask()
        tsubtask_list.append(tsubtask)

        tsubtask.sub_nr = "0"
        tsubtask.sub_nm = ""
        tsubtask.sub_selected = False

        if all_maintask:

            for eg_subtask in db_session.query(Eg_subtask).order_by(Eg_subtask._recid).all():
                tsubtask = Tsubtask()
                tsubtask_list.append(tsubtask)

                tsubtask.sub_nr = eg_subtask.sub_code
                tsubtask.sub_nm = eg_subtask.bezeich
                tsubtask.sub_selected = False


        else:

            for tmaintask in query(tmaintask_list, filters=(lambda tmaintask: tmaintask.main_selected)):

                for eg_subtask in db_session.query(Eg_subtask).filter(
                         (Eg_subtask.main_nr == tmaintask.main_nr)).order_by(Eg_subtask._recid).all():
                    tsubtask = Tsubtask()
                    tsubtask_list.append(tsubtask)

                    tsubtask.sub_nr = eg_subtask.sub_code
                    tsubtask.sub_nm = eg_subtask.bezeich
                    tsubtask.sub_selected = False


    def create_source():

        nonlocal engid, groupid, ci_date, tlocation_list, tcategory_list, troom_list, tmaintask_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, queasy, htparam, bediener, eg_location, zimmer, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init
        nonlocal qbuff


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tlocation, tcategory, qbuff, tbuff, comlocat, commain, comroom, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tlocation_list, tcategory_list


        tsource_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 130)).order_by(Qbuff._recid).all():
            tsource = Tsource()
            tsource_list.append(tsource)

            tsource.source_nr = qbuff.number1
            tsource.source_nm = qbuff.char1
            tsource.source_selected = False


    def create_category():

        nonlocal engid, groupid, ci_date, tlocation_list, tcategory_list, troom_list, tmaintask_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, queasy, htparam, bediener, eg_location, zimmer, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init
        nonlocal qbuff


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tlocation, tcategory, qbuff, tbuff, comlocat, commain, comroom, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tlocation_list, tcategory_list


        tcategory_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 132)).order_by(Qbuff._recid).all():
            tcategory = Tcategory()
            tcategory_list.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.char1
            tcategory.categ_selected = False


    def create_maintask():

        nonlocal engid, groupid, ci_date, tlocation_list, tcategory_list, troom_list, tmaintask_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, queasy, htparam, bediener, eg_location, zimmer, eg_property, eg_staff, eg_subtask
        nonlocal all_maintask, all_room, user_init
        nonlocal qbuff


        nonlocal tsource, tsubtask, tpic, tproperty, tmaintask, troom, tlocation, tcategory, qbuff, tbuff, comlocat, commain, comroom, comcategory
        nonlocal tsource_list, tsubtask_list, tpic_list, tproperty_list, tmaintask_list, troom_list, tlocation_list, tcategory_list


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


    define_group()
    define_engineering()
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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    return generate_output()