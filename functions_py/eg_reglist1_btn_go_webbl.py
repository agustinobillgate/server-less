#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 18/7/25
# gitlab: 676
# Ex_finishtime -> ex_finishtime
# CHAR3 -> char3
# vat_art_list -> ex_finishtime
# property -> propertynr
# OthersFlag -> othersFlag
# output table tidak sama
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.eg_repmaintain_open_querybl import eg_repmaintain_open_querybl
from models import Eg_action, Eg_maintain, Eg_location, Eg_property, Eg_staff, Eg_mdetail, Queasy, Zimmer, Eg_subtask, Eg_request, Guestbook

tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})

def eg_reglist1_btn_go_webbl(location:int, rmno:string, main_nr:int, reqstatus:int, sguestflag:bool, from_date:date, to_date:date, pvilanguage:int, tpic_data:[Tpic]):

    prepare_cache ([Eg_action, Eg_location, Eg_property, Eg_staff, Queasy, Eg_request])

    copyrequest_data = []
    smaintain_data = []
    action_data = []
    lvcarea:string = "eg-reglist1"
    int_str:List[string] = create_empty_list(3,"")
    type_str:List[string] = ["Weekly", "Monthly", "Quarter", "Half Yearly", "Year"]
    eg_action = eg_maintain = eg_location = eg_property = eg_staff = eg_mdetail = queasy = zimmer = eg_subtask = eg_request = guestbook = None

    action = tpic = copyrequest = tcategory = tsource = tsubtask = tmaintask = tlocation = troom = tstatus = t_eg_maintain = smaintain = qbuff1 = None

    action_data, Action = create_model_like(Eg_action, {"maintainnr":int})
    copyrequest_data, Copyrequest = create_model("Copyrequest", {"reqnr":int, "openby":string, "opendate":date, "opentime":int, "openstr":string, "status_str":string, "source_str":string, "source_name":string, "process_date":date, "closed_date":date, "urgency_nr":int, "urgency":string, "category_str":string, "deptnum":int, "dept_nm":string, "pmaintask":int, "maintask":string, "plocation":int, "location":string, "zinr":string, "property":int, "property_nm":string, "pic_str":string, "sub_str":string, "ex_finishdate":date, "ex_finishtime":int, "ex_finishstr":string, "memo":string, "task_def":string, "task_solv":string, "source":int, "category":int, "reqstatus":int, "sub_task":string, "subtask_bezeich":string, "assign_to":int, "delete_flag":bool, "str":string, "rec":string, "avail_image":bool})
    tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    tsource_data, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":string, "source_selected":bool})
    tsubtask_data, Tsubtask = create_model("Tsubtask", {"sub_nr":string, "sub_nm":string, "sub_selected":bool})
    tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
    tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tstatus_data, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
    t_eg_maintain_data, T_eg_maintain = create_model_like(Eg_maintain)
    smaintain_data, Smaintain = create_model("Smaintain", {"maintainnr":int, "estworkdate":date, "workdate":date, "donedate":date, "stat_nr":int, "stat_nm":string, "freq":string, "category_str":string, "maintask":string, "location":string, "zinr":string, "property":string, "comments":string, "pic":string, "str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal copyrequest_data, smaintain_data, action_data, lvcarea, int_str, type_str, eg_action, eg_maintain, eg_location, eg_property, eg_staff, eg_mdetail, queasy, zimmer, eg_subtask, eg_request, guestbook
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, from_date, to_date, pvilanguage


        nonlocal action, tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, t_eg_maintain, smaintain, qbuff1
        nonlocal action_data, copyrequest_data, tcategory_data, tsource_data, tsubtask_data, tmaintask_data, tlocation_data, troom_data, tstatus_data, t_eg_maintain_data, smaintain_data

        return {"location": location, "rmno": rmno, "main_nr": main_nr, "reqstatus": reqstatus, "copyRequest": copyrequest_data, "smaintain": smaintain_data, "action": action_data}

    def create_temp():

        nonlocal copyrequest_data, smaintain_data, action_data, lvcarea, int_str, type_str, eg_action, eg_maintain, eg_location, eg_property, eg_staff, eg_mdetail, queasy, zimmer, eg_subtask, eg_request, guestbook
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, from_date, to_date, pvilanguage


        nonlocal action, tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, t_eg_maintain, smaintain, qbuff1
        nonlocal action_data, copyrequest_data, tcategory_data, tsource_data, tsubtask_data, tmaintask_data, tlocation_data, troom_data, tstatus_data, t_eg_maintain_data, smaintain_data

        ques = None
        Ques =  create_buffer("Ques",Queasy)
        smaintain = Smaintain()
        smaintain_data.append(smaintain)


        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 133) & (Queasy.number1 == eg_property.maintask)).first()

        if queasy:
            smaintain.maintask = queasy.char1

            ques = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, queasy.number2)]})

            if ques:
                smaintain.category = ques.char1


        smaintain.maintainnr = t_eg_maintain.maintainnr
        smaintain.estworkdate = t_eg_maintain.estWorkDate
        smaintain.workdate = t_eg_maintain.workdate
        smaintain.donedate = t_eg_maintain.donedate
        smaintain.stat_nr = t_eg_maintain.type
        smaintain.freq = type_str[t_eg_maintain.typework - 1]
        smaintain.location = eg_location.bezeich
        smaintain.zinr = t_eg_maintain.zinr
        smaintain.property = eg_property.bezeich + "(" + trim (to_string(eg_property.nr , ">>>>>>9")) + ")"
        smaintain.comments = t_eg_maintain.comments
        smaintain.pic = eg_staff.name


    def create_status():

        nonlocal copyrequest_data, smaintain_data, action_data, lvcarea, int_str, type_str, eg_action, eg_maintain, eg_location, eg_property, eg_staff, eg_mdetail, queasy, zimmer, eg_subtask, eg_request, guestbook
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, from_date, to_date, pvilanguage


        nonlocal action, tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, t_eg_maintain, smaintain, qbuff1
        nonlocal action_data, copyrequest_data, tcategory_data, tsource_data, tsubtask_data, tmaintask_data, tlocation_data, troom_data, tstatus_data, t_eg_maintain_data, smaintain_data


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


    def create_room():

        nonlocal copyrequest_data, smaintain_data, action_data, lvcarea, int_str, type_str, eg_action, eg_maintain, eg_location, eg_property, eg_staff, eg_mdetail, queasy, zimmer, eg_subtask, eg_request, guestbook
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, from_date, to_date, pvilanguage


        nonlocal action, tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, t_eg_maintain, smaintain, qbuff1
        nonlocal action_data, copyrequest_data, tcategory_data, tsource_data, tsubtask_data, tmaintask_data, tlocation_data, troom_data, tstatus_data, t_eg_maintain_data, smaintain_data

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


    def create_maintask():

        nonlocal copyrequest_data, smaintain_data, action_data, lvcarea, int_str, type_str, eg_action, eg_maintain, eg_location, eg_property, eg_staff, eg_mdetail, queasy, zimmer, eg_subtask, eg_request, guestbook
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, from_date, to_date, pvilanguage


        nonlocal action, tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, t_eg_maintain, smaintain, qbuff1
        nonlocal action_data, copyrequest_data, tcategory_data, tsource_data, tsubtask_data, tmaintask_data, tlocation_data, troom_data, tstatus_data, t_eg_maintain_data, smaintain_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        tmaintask_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 133)).order_by(Qbuff._recid).all():
            tmaintask = Tmaintask()
            tmaintask_data.append(tmaintask)

            tmaintask.main_nr = qbuff.number1
            tmaintask.main_nm = qbuff.char1
            tmaintask.main_selected = False


    def create_subtask():

        nonlocal copyrequest_data, smaintain_data, action_data, lvcarea, int_str, type_str, eg_action, eg_maintain, eg_location, eg_property, eg_staff, eg_mdetail, queasy, zimmer, eg_subtask, eg_request, guestbook
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, from_date, to_date, pvilanguage


        nonlocal action, tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, t_eg_maintain, smaintain, qbuff1
        nonlocal action_data, copyrequest_data, tcategory_data, tsource_data, tsubtask_data, tmaintask_data, tlocation_data, troom_data, tstatus_data, t_eg_maintain_data, smaintain_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_subtask)
        tsubtask_data.clear()

        for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
            tsubtask = Tsubtask()
            tsubtask_data.append(tsubtask)

            tsubtask.sub_nr = qbuff.sub_code
            tsubtask.sub_nm = qbuff.bezeich
            tsubtask.sub_selected = False


    def create_source():

        nonlocal copyrequest_data, smaintain_data, action_data, lvcarea, int_str, type_str, eg_action, eg_maintain, eg_location, eg_property, eg_staff, eg_mdetail, queasy, zimmer, eg_subtask, eg_request, guestbook
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, from_date, to_date, pvilanguage


        nonlocal action, tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, t_eg_maintain, smaintain, qbuff1
        nonlocal action_data, copyrequest_data, tcategory_data, tsource_data, tsubtask_data, tmaintask_data, tlocation_data, troom_data, tstatus_data, t_eg_maintain_data, smaintain_data

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

        nonlocal copyrequest_data, smaintain_data, action_data, lvcarea, int_str, type_str, eg_action, eg_maintain, eg_location, eg_property, eg_staff, eg_mdetail, queasy, zimmer, eg_subtask, eg_request, guestbook
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, from_date, to_date, pvilanguage


        nonlocal action, tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, t_eg_maintain, smaintain, qbuff1
        nonlocal action_data, copyrequest_data, tcategory_data, tsource_data, tsubtask_data, tmaintask_data, tlocation_data, troom_data, tstatus_data, t_eg_maintain_data, smaintain_data

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


    def open_query1():

        nonlocal copyrequest_data, smaintain_data, action_data, lvcarea, int_str, type_str, eg_action, eg_maintain, eg_location, eg_property, eg_staff, eg_mdetail, queasy, zimmer, eg_subtask, eg_request, guestbook
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, from_date, to_date, pvilanguage


        nonlocal action, tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, t_eg_maintain, smaintain, qbuff1
        nonlocal action_data, copyrequest_data, tcategory_data, tsource_data, tsubtask_data, tmaintask_data, tlocation_data, troom_data, tstatus_data, t_eg_maintain_data, smaintain_data


        copyrequest_data.clear()

        if sguestflag :

            if rmno != "" and main_nr != 0:

                if reqstatus == 0:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                             (Eg_request.zinr == (rmno).lower()) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()
                else:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                             (Eg_request.zinr == (rmno).lower()) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()

            elif rmno != "" and main_nr == 0:

                if reqstatus == 0:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                             (Eg_request.zinr == (rmno).lower()) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()
                else:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                             (Eg_request.zinr == (rmno).lower()) & (Eg_request.delete_flag == False) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()

            elif rmno == "" and main_nr != 0:

                if reqstatus == 0:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                             (Eg_request.reserve_int == location) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()
                else:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                             (Eg_request.reserve_int == location) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()
            else:

                if reqstatus == 0:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                             (Eg_request.reserve_int == location) & (Eg_request.delete_flag == False) & (Eg_request.deptnum >= 0) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()
                else:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                             (Eg_request.reserve_int == location) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()
        else:

            if location == 0:

                if main_nr != 0:

                    if reqstatus == 0:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                                 (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()
                    else:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                                 (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()

                elif main_nr == 0:

                    if reqstatus == 0:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                                 (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()
                    else:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                                 (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.reqstatus == reqstatus) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.reqnr).all():
                            tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()
            else:

                if main_nr != 0:

                    if reqstatus == 0:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                                 (Eg_request.reserve_int == location) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()
                    else:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                                 (Eg_request.reserve_int == location) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()

                elif main_nr == 0:

                    if reqstatus == 0:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                                 (Eg_request.reserve_int == location) & (Eg_request.delete_flag == False) & (Eg_request.deptnum >= 0) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()
                    else:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.propertynr)).filter(
                                 (Eg_request.reserve_int == location) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.reqstatus == reqstatus) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_data, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()


    def create_copy1():

        nonlocal copyrequest_data, smaintain_data, action_data, lvcarea, int_str, type_str, eg_action, eg_maintain, eg_location, eg_property, eg_staff, eg_mdetail, queasy, zimmer, eg_subtask, eg_request, guestbook
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, from_date, to_date, pvilanguage


        nonlocal action, tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, t_eg_maintain, smaintain, qbuff1
        nonlocal action_data, copyrequest_data, tcategory_data, tsource_data, tsubtask_data, tmaintask_data, tlocation_data, troom_data, tstatus_data, t_eg_maintain_data, smaintain_data

        strdept:string = ""
        cat_nm:string = ""
        pic_number:int = 0

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, eg_request.deptnum)]})

        if queasy:
            strdept = queasy.char3
        else:
            strdept = ""
        copyrequest = Copyrequest()
        copyrequest_data.append(copyrequest)

        copyrequest.reqnr = eg_request.reqnr
        copyrequest.openby = eg_request.opened_by
        copyrequest.opendate = eg_request.opened_date
        copyrequest.opentime = eg_request.opened_time
        copyrequest.openstr = eg_request.char2
        copyrequest.status_str = tstatus.stat_nm
        copyrequest.source_str = tsource.source_nm
        copyrequest.source_name = eg_request.source_name
        copyrequest.process_date = eg_request.process_date
        copyrequest.closed_date = eg_request.closed_date
        copyrequest.urgency_nr = eg_request.urgency
        copyrequest.urgency = int_str[int (eg_request.urgency) - 1]
        copyrequest.category_str = tcategory.categ_nm
        copyrequest.deptnum = eg_request.deptnum
        copyrequest.dept_nm = strdept
        copyrequest.pmaintask = eg_request.number3
        copyrequest.maintask = tmaintask.main_nm
        copyrequest.plocation = eg_request.reserve_int
        copyrequest.location = eg_location.bezeich
        copyrequest.zinr = eg_request.zinr
        copyrequest.property = eg_request.propertynr
        copyrequest.ex_finishdate = eg_request.ex_finishdate
        copyrequest.ex_finishtime = eg_request.ex_finishtime
        copyrequest.ex_finishstr = eg_request.char3
        copyrequest.memo = eg_request.memo
        copyrequest.task_def = eg_request.task_def
        copyrequest.task_solv = eg_request.task_solv
        copyrequest.source = eg_request.source
        copyrequest.category = eg_request.category
        copyrequest.reqstatus = eg_request.reqstatus
        copyrequest.sub_task = eg_request.sub_task
        copyrequest.assign_to = eg_request.assign_to


        pic_number = to_int("-8" + to_string(eg_request.reqnr))

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, pic_number)],"reserve_int[0]": [(eq, eg_request.reqnr)]})

        if guestbook:
            copyrequest.avail_image = True

        eg_property = get_cache (Eg_property, {"nr": [(eq, eg_request.propertynr)]})

        if eg_property:
            copyrequest.property_nm = eg_property.bezeich + "(" + trim (to_string(eg_request.propertynr , ">>>>>>9")) + ")"


        else:
            copyrequest.property_nm = eg_property.bezeich

        tpic = query(tpic_data, filters=(lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)

        if tpic:
            copyrequest.pic_str = tpic.pic_nm

        tsubtask = query(tsubtask_data, filters=(lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)

        if tsubtask:

            eg_subtask = get_cache (Eg_subtask, {"sub_code": [(eq, eg_request.sub_task)]})

            if eg_subtask:

                # Rd 3/8/2025
                # othersFlag -> othersflag
                if eg_subtask.othersflag:

                    if eg_request.subtask_bezeich != "":
                        copyrequest.sub_str = tsubtask.sub_nm + "(" + eg_request.subtask_bezeich + ")"


                    else:
                        copyrequest.sub_str = tsubtask.sub_nm


                else:
                    copyrequest.sub_str = tsubtask.sub_nm


            else:
                copyrequest.sub_str = tsubtask.sub_nm


    def create_request1():

        nonlocal copyrequest_data, smaintain_data, action_data, lvcarea, int_str, type_str, eg_action, eg_maintain, eg_location, eg_property, eg_staff, eg_mdetail, queasy, zimmer, eg_subtask, eg_request, guestbook
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, from_date, to_date, pvilanguage


        nonlocal action, tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, t_eg_maintain, smaintain, qbuff1
        nonlocal action_data, copyrequest_data, tcategory_data, tsource_data, tsubtask_data, tmaintask_data, tlocation_data, troom_data, tstatus_data, t_eg_maintain_data, smaintain_data

        strdatetime:string = ""
        ex_finishstr:string = ""
        ques = None
        Ques =  create_buffer("Ques",Queasy)

        for eg_request in db_session.query(Eg_request).filter(
                 (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request._recid).all():
            strdatetime = to_string(eg_request.opened_date , "99/99/99") + " " + to_string(eg_request.opened_time , "HH:MM")

            if eg_request.ex_finishdate == None:
                ex_finishstr = ""
            else:
                ex_finishstr = to_string(eg_request.ex_finishdate , "99/99/99") + " " + to_string(eg_request.ex_finishtime , "HH:MM")

            if eg_request.propertynr == 0:
                eg_request.char2 = strdatetime
                eg_request.char3 = ex_finishstr


            else:

                eg_property = get_cache (Eg_property, {"nr": [(eq, eg_request.propertynr)]})

                if eg_property:
                    eg_request.char2 = strdatetime
                    eg_request.char3 = ex_finishstr
                    eg_request.maintask = eg_property.maintask

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == eg_property.maintask)).first()

                    if queasy:

                        ques = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, queasy.number2)]})

                        if ques:
                            eg_request.category = queasy.number2


    int_str[0] = translateExtended ("Low", lvcarea , "")
    int_str[1] = translateExtended ("Medium" , lvcarea , "")
    int_str[2] = translateExtended ("High", lvcarea , "")
    create_status()
    create_room()
    create_maintask()
    create_subtask()
    create_source()
    create_category()
    create_request1()
    open_query1()
    t_eg_maintain_data = get_output(eg_repmaintain_open_querybl(get_current_date(), get_current_date()))
    
    # Rd, 1/8/2025
    if t_eg_maintain_data:        
        eg_location_obj_list = {}
        for eg_location, eg_property, eg_staff in db_session.query(Eg_location, Eg_property, Eg_staff).join(Eg_property,(Eg_property.nr == t_eg_maintain.propertynr)).join(Eg_staff,(Eg_staff.nr == t_eg_maintain.pic)).filter(
                ((Eg_location.nr.in_(list(set([t_eg_maintain.location for t_eg_maintain in t_eg_maintain_data])))))).order_by(Eg_location._recid).all():
            if eg_location_obj_list.get(eg_location._recid):
                continue
            else:
                eg_location_obj_list[eg_location._recid] = True


            create_temp()

    for smaintain in query(smaintain_data):

        eg_mdetail_obj_list = {}
        for eg_mdetail, eg_action in db_session.query(Eg_mdetail, Eg_action).join(Eg_action,(Eg_action.actionnr == Eg_mdetail.nr)).filter(
                 (Eg_mdetail.key == 1) & (Eg_mdetail.maintainnr == smaintain.maintainnr)).order_by(Eg_mdetail._recid).all():
            if eg_mdetail_obj_list.get(eg_mdetail._recid):
                continue
            else:
                eg_mdetail_obj_list[eg_mdetail._recid] = True


            action = Action()
            action_data.append(action)

            action.actionnr = eg_action.actionnr
            action.bezeich = eg_action.bezeich
            action.maintask = eg_action.maintask
            action.maintainnr = smaintain.maintainnr

    return generate_output()