from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Eg_request, Queasy, Eg_property, Eg_location, Zimmer, Eg_subtask

def eg_reglist1_btn_cancelbl(location:int, rmno:str, main_nr:int, reqstatus:int, sguestflag:bool, copyrequest_reqnr:int, user_init:str, st_cancel:str):
    flag = False
    copyrequest_list = []
    eg_request = queasy = eg_property = eg_location = zimmer = eg_subtask = None

    tpic = copyrequest = tcategory = tsource = tsubtask = tmaintask = tlocation = troom = tstatus = ques = qbuff = qbuff1 = None

    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool, "pic_dept":int})
    copyrequest_list, Copyrequest = create_model("Copyrequest", {"reqnr":int, "openby":str, "opendate":date, "opentime":int, "openstr":str, "status_str":str, "source_str":str, "source_name":str, "process_date":date, "closed_date":date, "urgency_nr":int, "urgency":str, "category_str":str, "deptnum":int, "dept_nm":str, "pmaintask":int, "maintask":str, "plocation":int, "location":str, "zinr":str, "property":int, "property_nm":str, "pic_str":str, "sub_str":str, "ex_finishdate":date, "ex_finishtime":int, "ex_finishstr":str, "memo":str, "task_def":str, "task_solv":str, "source":int, "category":int, "reqstatus":int, "sub_task":str, "subtask_bezeich":str, "assign_to":int, "delete_flag":bool, "str":str, "rec":str})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})
    tsource_list, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":str, "source_selected":bool})
    tsubtask_list, Tsubtask = create_model("Tsubtask", {"sub_nr":str, "sub_nm":str, "sub_selected":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":str, "stat_selected":bool})

    Ques = Queasy
    Qbuff = Queasy
    Qbuff1 = Tlocation
    qbuff1_list = tlocation_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal ques, qbuff, qbuff1


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, ques, qbuff, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list
        return {"flag": flag, "copyRequest": copyrequest_list}

    def create_request1():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal ques, qbuff, qbuff1


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, ques, qbuff, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list

        strdatetime:str = ""
        ex_finishstr:str = ""
        Ques = Queasy

        for eg_request in db_session.query(Eg_request).filter(
                (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
            strdatetime = to_string(eg_request.opened_date , "99/99/99") + " " + to_string(eg_request.opened_time , "HH:MM")

            if eg_request.ex_finishdate == None:
                ex_finishstr = ""
            else:
                ex_finishstr = to_string(eg_request.ex_finishdate , "99/99/99") + " " + to_string(eg_request.Ex_finishtime , "HH:MM")

            if eg_request.propertynr == 0:
                eg_request.char2 = strdatetime
                eg_request.char3 = ex_finishstr


            else:

                eg_property = db_session.query(Eg_property).filter(
                        (Eg_property.nr == eg_request.propertynr)).first()

                if eg_property:
                    eg_request.char2 = strdatetime
                    eg_request.char3 = ex_finishstr
                    eg_request.maintask = eg_property.maintask

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.KEY == 133) &  (Queasy.number1 == eg_property.maintask)).first()

                    if queasy:

                        ques = db_session.query(Ques).filter(
                                (Ques.key == 132) &  (Ques.number1 == queasy.number2)).first()

                        if ques:
                            eg_request.category = queasy.number2

    def open_query1():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal ques, qbuff, qbuff1


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, ques, qbuff, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list


        copyrequest_list.clear()

        if sguestflag :

            eg_location = db_session.query(Eg_location).filter(
                    (Eg_location.guestflag)).first()

            if eg_location:
                location = eg_location.nr

            if rmno != "" and main_nr != 0:

                if reqstatus == 0:

                    eg_request_obj_list = []
                    for eg_request, tstatus, tsource, tcategory, tsubtask, tMaintask, tpic, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, TMaintask, Tpic, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                            (func.lower(Eg_request.zinr) == (rmno).lower()) &  (Eg_request.maintask == main_nr) &  (Eg_request.deptnum >= 0) &  (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                        if eg_request._recid in eg_request_obj_list:
                            continue
                        else:
                            eg_request_obj_list.append(eg_request._recid)


                        create_copy1()
                else:

                    eg_request_obj_list = []
                    for eg_request, tstatus, tsource, tcategory, tsubtask, tMaintask, tpic, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, TMaintask, Tpic, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                            (func.lower(Eg_request.zinr) == (rmno).lower()) &  (Eg_request.maintask == main_nr) &  (Eg_request.deptnum >= 0) &  (Eg_request.reqstatus == reqstatus) &  (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                        if eg_request._recid in eg_request_obj_list:
                            continue
                        else:
                            eg_request_obj_list.append(eg_request._recid)


                        create_copy1()

            elif rmno != "" and main_nr == 0:

                if reqstatus == 0:

                    eg_request_obj_list = []
                    for eg_request, tstatus, tsource, tcategory, tsubtask, tMaintask, tpic, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, TMaintask, Tpic, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                            (func.lower(Eg_request.zinr) == (rmno).lower()) &  (Eg_request.deptnum >= 0) &  (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                        if eg_request._recid in eg_request_obj_list:
                            continue
                        else:
                            eg_request_obj_list.append(eg_request._recid)


                        create_copy1()
                else:

                    eg_request_obj_list = []
                    for eg_request, tstatus, tsource, tcategory, tsubtask, tMaintask, tpic, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, TMaintask, Tpic, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                            (func.lower(Eg_request.zinr) == (rmno).lower()) &  (Eg_request.delete_flag == False) &  (Eg_request.deptnum >= 0) &  (Eg_request.reqstatus == reqstatus) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                        if eg_request._recid in eg_request_obj_list:
                            continue
                        else:
                            eg_request_obj_list.append(eg_request._recid)


                        create_copy1()

            elif rmno == "" and main_nr != 0:

                if reqstatus == 0:

                    eg_request_obj_list = []
                    for eg_request, tstatus, tsource, tcategory, tsubtask, tMaintask, tpic, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, TMaintask, Tpic, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                            (Eg_request.reserve_int == location) &  (Eg_request.maintask == main_nr) &  (Eg_request.deptnum >= 0) &  (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                        if eg_request._recid in eg_request_obj_list:
                            continue
                        else:
                            eg_request_obj_list.append(eg_request._recid)


                        create_copy1()
                else:

                    eg_request_obj_list = []
                    for eg_request, tstatus, tsource, tcategory, tsubtask, tMaintask, tpic, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, TMaintask, Tpic, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                            (Eg_request.reserve_int == location) &  (Eg_request.maintask == main_nr) &  (Eg_request.deptnum >= 0) &  (Eg_request.reqstatus == reqstatus) &  (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                        if eg_request._recid in eg_request_obj_list:
                            continue
                        else:
                            eg_request_obj_list.append(eg_request._recid)


                        create_copy1()
            else:

                if reqstatus == 0:

                    eg_request_obj_list = []
                    for eg_request, tstatus, tsource, tcategory, tsubtask, tMaintask, tpic, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, TMaintask, Tpic, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                            (Eg_request.reserve_int == location) &  (Eg_request.delete_flag == False) &  (Eg_request.deptnum >= 0) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                        if eg_request._recid in eg_request_obj_list:
                            continue
                        else:
                            eg_request_obj_list.append(eg_request._recid)


                        create_copy1()
                else:

                    eg_request_obj_list = []
                    for eg_request, tstatus, tsource, tcategory, tsubtask, tpic, tMaintask, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, Tpic, TMaintask, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                            (Eg_request.reserve_int == location) &  (Eg_request.deptnum >= 0) &  (Eg_request.reqstatus == reqstatus) &  (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                        if eg_request._recid in eg_request_obj_list:
                            continue
                        else:
                            eg_request_obj_list.append(eg_request._recid)


                        create_copy1()
        else:

            if location == 0:

                if main_nr != 0:

                    if reqstatus == 0:

                        eg_request_obj_list = []
                        for eg_request, tstatus, tsource, tcategory, tsubtask, tpic, tMaintask, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, Tpic, TMaintask, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                (Eg_request.maintask == main_nr) &  (Eg_request.deptnum >= 0) &  (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                            if eg_request._recid in eg_request_obj_list:
                                continue
                            else:
                                eg_request_obj_list.append(eg_request._recid)


                            create_copy1()
                    else:

                        eg_request_obj_list = []
                        for eg_request, tstatus, tsource, tcategory, tsubtask, tpic, tMaintask, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, Tpic, TMaintask, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                (Eg_request.maintask == main_nr) &  (Eg_request.deptnum >= 0) &  (Eg_request.reqstatus == reqstatus) &  (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                            if eg_request._recid in eg_request_obj_list:
                                continue
                            else:
                                eg_request_obj_list.append(eg_request._recid)


                            create_copy1()

                elif main_nr == 0:

                    if reqstatus == 0:

                        eg_request_obj_list = []
                        for eg_request, tstatus, tsource, tcategory, tsubtask, tMaintask, tpic, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, TMaintask, Tpic, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                (Eg_request.deptnum >= 0) &  (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                            if eg_request._recid in eg_request_obj_list:
                                continue
                            else:
                                eg_request_obj_list.append(eg_request._recid)


                            create_copy1()
                    else:

                        eg_request_obj_list = []
                        for eg_request, tstatus, tsource, tcategory, tsubtask, tpic, tMaintask, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, Tpic, TMaintask, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                (Eg_request.deptnum >= 0) &  (Eg_request.reqstatus == reqstatus) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                            if eg_request._recid in eg_request_obj_list:
                                continue
                            else:
                                eg_request_obj_list.append(eg_request._recid)


                            create_copy1()
            else:

                if main_nr != 0:

                    if reqstatus == 0:

                        eg_request_obj_list = []
                        for eg_request, tstatus, tsource, tcategory, tsubtask, tpic, tMaintask, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, Tpic, TMaintask, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                (Eg_request.reserve_int == location) &  (Eg_request.maintask == main_nr) &  (Eg_request.deptnum >= 0) &  (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                            if eg_request._recid in eg_request_obj_list:
                                continue
                            else:
                                eg_request_obj_list.append(eg_request._recid)


                            create_copy1()
                    else:

                        eg_request_obj_list = []
                        for eg_request, tstatus, tsource, tcategory, tsubtask, tpic, tMaintask, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, Tpic, TMaintask, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                (Eg_request.reserve_int == location) &  (Eg_request.maintask == main_nr) &  (Eg_request.deptnum >= 0) &  (Eg_request.reqstatus == reqstatus) &  (Eg_request.delete_flag == False) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                            if eg_request._recid in eg_request_obj_list:
                                continue
                            else:
                                eg_request_obj_list.append(eg_request._recid)


                            create_copy1()

                elif main_nr == 0:

                    if reqstatus == 0:

                        eg_request_obj_list = []
                        for eg_request, tstatus, tsource, tcategory, tsubtask, tpic, tMaintask, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, Tpic, TMaintask, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                (Eg_request.reserve_int == location) &  (Eg_request.delete_flag == False) &  (Eg_request.deptnum >= 0) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                            if eg_request._recid in eg_request_obj_list:
                                continue
                            else:
                                eg_request_obj_list.append(eg_request._recid)


                            create_copy1()
                    else:

                        eg_request_obj_list = []
                        for eg_request, tstatus, tsource, tcategory, tsubtask, tpic, tMaintask, eg_location, eg_property in db_session.query(Eg_request, Tstatus, Tsource, Tcategory, Tsubtask, Tpic, TMaintask, Eg_location, Eg_property).join(Tstatus,(Tstatus.stat_nr == Eg_request.reqstatus)).join(Tsource,(Tsource.source_nr == Eg_request.SOURCE)).join(Tcategory,(Tcategory.categ_nr == Eg_request.category)).join(Tsubtask,(Tsubtask.sub_nr == Eg_request.sub_task)).join(Tpic,(Tpic.pic_nr == Eg_request.assign_to)).join(TMaintask,(tmaintask.main_nr == Eg_request.maintask)).join(Eg_location,(Eg_location.nr == Eg_request.reserve_int)).join(Eg_property,(Eg_property.nr == Eg_request.property)).filter(
                                (Eg_request.reserve_int == location) &  (Eg_request.deptnum >= 0) &  (Eg_request.delete_flag == False) &  (Eg_request.reqstatus == reqstatus) &  (Eg_request.opened_date >= from_date) &  (Eg_request.opened_date <= to_date)).all():
                            if eg_request._recid in eg_request_obj_list:
                                continue
                            else:
                                eg_request_obj_list.append(eg_request._recid)


                            create_copy1()

    def create_status():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal ques, qbuff, qbuff1


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, ques, qbuff, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list


        tStatus_list.clear()
        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 1
        tStatus.stat_nm = "New"
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


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 4
        tStatus.stat_nm = "Postponed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 5
        tStatus.stat_nm = "Closed"
        tstatus.stat_selected = False

    def create_room():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal ques, qbuff, qbuff1


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, ques, qbuff, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list

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

    def create_maintask():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal ques, qbuff, qbuff1


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, ques, qbuff, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list


        Qbuff = Queasy
        tMaintask_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 133)).all():
            tmaintask = Tmaintask()
            tmaintask_list.append(tmaintask)

            tMaintask.main_nr = qbuff.number1
            tMaintask.Main_nm = qbuff.char1
            tmaintask.main_selected = False

    def create_subtask():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal ques, qbuff, qbuff1


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, ques, qbuff, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list


        Qbuff = Eg_subtask
        tsubtask_list.clear()

        for qbuff in db_session.query(Qbuff).all():
            tsubtask = Tsubtask()
            tsubtask_list.append(tsubtask)

            tsubtask.sub_nr = qbuff.sub_code
            tsubtask.sub_nm = qbuff.bezeich
            tsubtask.sub_selected = False

    def create_source():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal ques, qbuff, qbuff1


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, ques, qbuff, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list


        Qbuff = Queasy
        tsource_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.KEY == 130)).all():
            tsource = Tsource()
            tsource_list.append(tsource)

            tsource.source_nr = qbuff.number1
            tsource.source_nm = qbuff.char1
            tsource.source_selected = False

    def create_category():

        nonlocal flag, copyrequest_list, eg_request, queasy, eg_property, eg_location, zimmer, eg_subtask
        nonlocal ques, qbuff, qbuff1


        nonlocal tpic, copyrequest, tcategory, tsource, tsubtask, tmaintask, tlocation, troom, tstatus, ques, qbuff, qbuff1
        nonlocal tpic_list, copyrequest_list, tcategory_list, tsource_list, tsubtask_list, tmaintask_list, tlocation_list, troom_list, tstatus_list


        Qbuff = Queasy
        tcategory_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 132)).all():
            tcategory = Tcategory()
            tcategory_list.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.char1
            tcategory.categ_selected = False

    eg_request = db_session.query(Eg_request).filter(
            (Eg_request.reqnr == copyrequest_reqnr)).first()

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