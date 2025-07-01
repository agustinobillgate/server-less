#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_request, Queasy, Eg_property, Eg_location, Zimmer, Eg_subtask

def eg_reglist1_btn_cancelbl(location:int, rmno:string, main_nr:int, reqstatus:int, sguestflag:bool, copyrequest_reqnr:int, user_init:string, st_cancel:string):

    prepare_cache ([Eg_request, Queasy, Eg_property, Eg_location])

    flag = False
    copyrequest_list = []
    eg_request = queasy = eg_property = eg_location = zimmer = eg_subtask = None

    tpic = copyrequest = tcategory = tsource = tsubtask = tmaintask = tlocation = troom = tstatus = qbuff1 = None

    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    copyrequest_list, Copyrequest = create_model("Copyrequest", {"reqnr":int, "openby":string, "opendate":date, "opentime":int, "openstr":string, "status_str":string, "source_str":string, "source_name":string, "process_date":date, "closed_date":date, "urgency_nr":int, "urgency":string, "category_str":string, "deptnum":int, "dept_nm":string, "pmaintask":int, "maintask":string, "plocation":int, "location":string, "zinr":string, "property":int, "property_nm":string, "pic_str":string, "sub_str":string, "ex_finishdate":date, "ex_finishtime":int, "ex_finishstr":string, "memo":string, "task_def":string, "task_solv":string, "source":int, "category":int, "reqstatus":int, "sub_task":string, "subtask_bezeich":string, "assign_to":int, "delete_flag":bool, "str":string, "rec":string})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    tsource_list, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":string, "source_selected":bool})
    tsubtask_list, Tsubtask = create_model("Tsubtask", {"sub_nr":string, "sub_nm":string, "sub_selected":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    troom_list, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, copyrequest_reqnr, user_init, st_cancel


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list

        return {"location": location, "rmno": rmno, "main_nr": main_nr, "reqstatus": reqstatus, "flag": flag, "copyRequest": copyrequest_list}

    def create_request1():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, copyrequest_reqnr, user_init, st_cancel


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list

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
                ex_finishstr = to_string(eg_request.ex_finishdate , "99/99/99") + " " + to_string(eg_request.Ex_finishtime , "HH:MM")

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


    def open_query1():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, copyrequest_reqnr, user_init, st_cancel


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list


        copyrequest_list.clear()

        if sguestflag :

            eg_location = get_cache (Eg_location, {"guestflag": [(eq, True)]})

            if eg_location:
                location = eg_location.nr

            if rmno != "" and main_nr != 0:

                if reqstatus == 0:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                             (Eg_request.zinr == (rmno).lower()) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                        if not tsubtask:
                            continue

                        tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                        if not tpic:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()
                else:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                             (Eg_request.zinr == (rmno).lower()) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                        if not tsubtask:
                            continue

                        tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                        if not tpic:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()

            elif rmno != "" and main_nr == 0:

                if reqstatus == 0:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                             (Eg_request.zinr == (rmno).lower()) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                        if not tsubtask:
                            continue

                        tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                        if not tpic:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()
                else:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                             (Eg_request.zinr == (rmno).lower()) & (Eg_request.delete_flag == False) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                        if not tsubtask:
                            continue

                        tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                        if not tpic:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()

            elif rmno == "" and main_nr != 0:

                if reqstatus == 0:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                             (Eg_request.reserve_int == location) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                        if not tsubtask:
                            continue

                        tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                        if not tpic:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()
                else:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                             (Eg_request.reserve_int == location) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                        if not tsubtask:
                            continue

                        tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                        if not tpic:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()
            else:

                if reqstatus == 0:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                             (Eg_request.reserve_int == location) & (Eg_request.delete_flag == False) & (Eg_request.deptnum >= 0) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                        if not tsubtask:
                            continue

                        tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                        if not tmaintask:
                            continue

                        tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                        if not tpic:
                            continue

                        if eg_request_obj_list.get(eg_request._recid):
                            continue
                        else:
                            eg_request_obj_list[eg_request._recid] = True


                        create_copy1()
                else:

                    eg_request_obj_list = {}
                    for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                             (Eg_request.reserve_int == location) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                        tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                        if not tstatus:
                            continue

                        tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                        if not tsource:
                            continue

                        tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                        if not tcategory:
                            continue

                        tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                        if not tsubtask:
                            continue

                        tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                        if not tpic:
                            continue

                        tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
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
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                 (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                            if not tsubtask:
                                continue

                            tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                            if not tpic:
                                continue

                            tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()
                    else:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                 (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                            if not tsubtask:
                                continue

                            tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                            if not tpic:
                                continue

                            tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
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
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                 (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                            if not tsubtask:
                                continue

                            tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                            if not tpic:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()
                    else:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                 (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.reqnr).all():
                            tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                            if not tsubtask:
                                continue

                            tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                            if not tpic:
                                continue

                            tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
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
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                 (Eg_request.reserve_int == location) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                            if not tsubtask:
                                continue

                            tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                            if not tpic:
                                continue

                            tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()
                    else:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                 (Eg_request.reserve_int == location) & (Eg_request.maintask == main_nr) & (Eg_request.deptnum >= 0) & (Eg_request.reqstatus == reqstatus) & (Eg_request.delete_flag == False) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                            if not tsubtask:
                                continue

                            tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                            if not tpic:
                                continue

                            tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
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
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                 (Eg_request.reserve_int == location) & (Eg_request.delete_flag == False) & (Eg_request.deptnum >= 0) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                            if not tsubtask:
                                continue

                            tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                            if not tpic:
                                continue

                            tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()
                    else:

                        eg_request_obj_list = {}
                        for eg_request, eg_location, eg_property in db_session.query(Eg_request, Eg_location, Eg_property).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                 (Eg_request.reserve_int == location) & (Eg_request.deptnum >= 0) & (Eg_request.delete_flag == False) & (Eg_request.reqstatus == reqstatus) & (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date)).order_by(Eg_request.opened_date).all():
                            tstatus = query(tstatus_list, (lambda tstatus: tstatus.stat_nr == eg_request.reqstatus), first=True)
                            if not tstatus:
                                continue

                            tsource = query(tsource_list, (lambda tsource: tsource.source_nr == eg_request.source), first=True)
                            if not tsource:
                                continue

                            tcategory = query(tcategory_list, (lambda tcategory: tcategory.categ_nr == eg_request.category), first=True)
                            if not tcategory:
                                continue

                            tsubtask = query(tsubtask_list, (lambda tsubtask: tsubtask.sub_nr == eg_request.sub_task), first=True)
                            if not tsubtask:
                                continue

                            tpic = query(tpic_list, (lambda tpic: tpic.pic_nr == eg_request.assign_to), first=True)
                            if not tpic:
                                continue

                            tmaintask = query(tmaintask_list, (lambda tmaintask: tmaintask.main_nr == eg_request.maintask), first=True)
                            if not tmaintask:
                                continue

                            if eg_request_obj_list.get(eg_request._recid):
                                continue
                            else:
                                eg_request_obj_list[eg_request._recid] = True


                            create_copy1()


    def create_status():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, copyrequest_reqnr, user_init, st_cancel


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list


        tstatus_list.clear()
        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 1
        tstatus.stat_nm = "New"
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


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 4
        tstatus.stat_nm = "Postponed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 5
        tstatus.stat_nm = "Closed"
        tstatus.stat_selected = False


    def create_room():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, copyrequest_reqnr, user_init, st_cancel


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list

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


    def create_maintask():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, copyrequest_reqnr, user_init, st_cancel


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        tmaintask_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 133)).order_by(Qbuff._recid).all():
            tmaintask = Tmaintask()
            tmaintask_list.append(tmaintask)

            tmaintask.main_nr = qbuff.number1
            tmaintask.main_nm = qbuff.char1
            tmaintask.main_selected = False


    def create_subtask():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, copyrequest_reqnr, user_init, st_cancel


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_subtask)
        tsubtask_list.clear()

        for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
            tsubtask = Tsubtask()
            tsubtask_list.append(tsubtask)

            tsubtask.sub_nr = qbuff.sub_code
            tsubtask.sub_nm = qbuff.bezeich
            tsubtask.sub_selected = False


    def create_source():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, copyrequest_reqnr, user_init, st_cancel


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        tsource_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 130)).order_by(Qbuff._recid).all():
            tsource = Tsource()
            tsource_list.append(tsource)

            tsource.source_nr = qbuff.number1
            tsource.source_nm = qbuff.char1
            tsource.source_selected = False


    def create_category():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal location, rmno, main_nr, reqstatus, sguestflag, copyrequest_reqnr, user_init, st_cancel


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list

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


    eg_request = get_cache (Eg_request, {"reqnr": [(eq, copyrequest_reqnr)]})

    if eg_request:
        eg_request.delete_flag = True
        eg_request.cancel_date = get_current_date()
        eg_request.cancel_time = get_current_time_in_seconds()
        eg_request.cancel_by = user_init
        eg_request.char1 = st_cancel


        create_request1()
        flag = True
        create_status()
        create_room()
        create_maintask()
        create_subtask()
        create_source()
        create_category()
        open_query1()

    return generate_output()