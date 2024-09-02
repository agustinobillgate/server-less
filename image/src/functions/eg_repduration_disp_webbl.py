from functions.additional_functions import *
import decimal
from datetime import date
from functions.eg_repduration_all_locationbl import eg_repduration_all_locationbl
from functions.eg_repduration_open_querybl import eg_repduration_open_querybl
from models import Eg_request

def eg_repduration_disp_webbl(all_room:bool, all_property:bool, all_pic:bool, all_subtask:bool, all_source:bool, all_category:bool, all_location:bool, all_maintask:bool, cmb_operand:int, fdate:date, tdate:date, calctime:int, calctime1:int, tpic:[Tpic], tsubtask:[Tsubtask], tsource:[Tsource], tcategory:[Tcategory], tlocation:[Tlocation], tmaintask:[Tmaintask]):
    tproperty_list = []
    troom_list = []
    copyrequest_list = []
    int_str:[str] = ["", "", "", ""]
    eg_request = None

    t_eg_request = srequest = copyrequest = tproperty = tpic = tsubtask = tsource = tcategory = tlocation = tmaintask = troom = None

    t_eg_request_list, T_eg_request = create_model_like(Eg_request)
    srequest_list, Srequest = create_model("Srequest", {"reqnr":int, "opendate":date, "status_str":str, "source_str":str, "source_name":str, "process_date":date, "closed_date":date, "urgency":str, "category_str":str, "deptnum":int, "pmaintask":int, "maintask":str, "plocation":int, "location":str, "zinr":str, "property":int, "property_nm":str, "pic_str":str, "sub_str":str, "ex_finishdate":date, "ex_finishtime":str, "ex_finish":str, "done_date":date, "done_time":str, "done":str, "memo":str, "task_def":str, "task_solv":str, "source":int, "category":int, "reqstatus":int, "sub_task":str, "assign_to":int, "reason":str})
    copyrequest_list, Copyrequest = create_model("Copyrequest", {"reqnr":int, "opendate":date, "status_str":str, "source_str":str, "source_name":str, "process_date":date, "closed_date":date, "urgency":str, "category_str":str, "deptnum":int, "pmaintask":int, "maintask":str, "plocation":int, "location":str, "zinr":str, "property":int, "property_nm":str, "pic_str":str, "sub_str":str, "ex_finishdate":date, "ex_finishtime":str, "ex_finish":str, "done_date":date, "done_time":str, "done":str, "memo":str, "task_def":str, "task_solv":str, "source":int, "category":int, "reqstatus":int, "sub_task":str, "assign_to":int, "reason":str, "str":str})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pcateg_nr":int, "pcateg":str, "pmain_nr":int, "pmain":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool, "pic_dept":int})
    tsubtask_list, Tsubtask = create_model("Tsubtask", {"sub_nr":str, "sub_nm":str, "sub_selected":bool})
    tsource_list, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":str, "source_selected":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tproperty_list, troom_list, copyrequest_list, int_str, eg_request


        nonlocal t_eg_request, srequest, copyrequest, tproperty, tpic, tsubtask, tsource, tcategory, tlocation, tmaintask, troom
        nonlocal t_eg_request_list, srequest_list, copyrequest_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, tcategory_list, tlocation_list, tmaintask_list, troom_list
        return {"tproperty": tproperty_list, "troom": troom_list, "copyRequest": copyrequest_list}

    def open_query():

        nonlocal tproperty_list, troom_list, copyrequest_list, int_str, eg_request


        nonlocal t_eg_request, srequest, copyrequest, tproperty, tpic, tsubtask, tsource, tcategory, tlocation, tmaintask, troom
        nonlocal t_eg_request_list, srequest_list, copyrequest_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, tcategory_list, tlocation_list, tmaintask_list, troom_list

        d:int = 0
        e:int = 0
        calday:int = 0
        full_finish:str = ""
        full_done:str = ""
        troom_list, tproperty_list = get_output(eg_repduration_all_locationbl(all_room, tLocation, tmaintask))

        if all_property:

            for tproperty in query(tproperty_list):
                tproperty.prop_selected = True


        if all_pic:

            for tpic in query(tpic_list):
                tpic.pic_selected = True


        if all_subtask:

            for tsubtask in query(tsubtask_list):
                tsubtask.sub_selected = True


        if all_source:

            for tsource in query(tsource_list):
                tsource.source_selected = True


        if all_category:

            for tcategory in query(tcategory_list):
                tcategory.categ_selected = True


        if all_location:

            for tlocation in query(tlocation_list):
                tLocation.loc_selected = True


        if all_maintask:

            for tmaintask in query(tmaintask_list):
                tMaintask.main_selected = True

        srequest_list.clear()
        copyrequest_list.clear()
        t_eg_request_list = get_output(eg_repduration_open_querybl(fdate, tdate))

        if cmb_operand == 1:

            for t_eg_request in query(t_eg_request_list):
                full_finish = to_string(t_eg_request.ex_finishdate , "99/99/99") + " " + to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                full_done = to_string(t_eg_request.done_date , "99/99/99") + " " + to_string(t_eg_request.done_time , "HH:MM:SS")

                if t_eg_request.ex_finishdate == t_eg_request.done_date:

                    if (t_eg_request.ex_finishtime - t_eg_request.done_time) >= 0 and (t_eg_request.ex_finishtime - t_eg_request.done_time) < calctime:

                        tproperty = query(tproperty_list, filters=(lambda tproperty :tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_list.append(srequest)

                            sRequest.reqnr = t_eg_request.reqnr
                            sRequest.opendate = t_eg_request.opened_date
                            sRequest.process_date = t_eg_request.process_date
                            sRequest.closed_date = t_eg_request.closed_date
                            sRequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            sRequest.ex_finish = full_finish
                            sRequest.done = full_done
                            sRequest.ex_finishdate = t_eg_request.ex_finishdate
                            sRequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            sRequest.done_date = t_eg_request.done_date
                            sRequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            sRequest.memo = t_eg_request.memo
                            sRequest.task_def = t_eg_request.task_def
                            sRequest.task_solv = t_eg_request.task_solv
                            sRequest.pmaintask = tproperty.pmain_nr
                            sRequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.SOURCE = t_eg_request.SOURCE
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

                elif t_eg_request.ex_finishdate > t_eg_request.done_date:
                    calday = t_eg_request.ex_finishdate - t_eg_request.done_date
                    d = (calday * 86399) + t_eg_request.done_time
                    e = d - t_eg_request.ex_finishtime

                    if e >= 0 and e < calctime:

                        tproperty = query(tproperty_list, filters=(lambda tproperty :tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_list.append(srequest)

                            sRequest.reqnr = t_eg_request.reqnr
                            sRequest.opendate = t_eg_request.opened_date
                            sRequest.process_date = t_eg_request.process_date
                            sRequest.closed_date = t_eg_request.closed_date
                            sRequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            sRequest.ex_finish = full_finish
                            sRequest.done = full_done
                            sRequest.ex_finishdate = t_eg_request.ex_finishdate
                            sRequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            sRequest.done_date = t_eg_request.done_date
                            sRequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            sRequest.memo = t_eg_request.memo
                            sRequest.task_def = t_eg_request.task_def
                            sRequest.task_solv = t_eg_request.task_solv
                            sRequest.pmaintask = tproperty.pmain_nr
                            sRequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.SOURCE = t_eg_request.SOURCE
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

        elif cmb_operand == 2:

            for t_eg_request in query(t_eg_request_list):
                full_finish = to_string(t_eg_request.ex_finishdate , "99/99/99") + " " + to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                full_done = to_string(t_eg_request.done_date , "99/99/99") + " " + to_string(t_eg_request.done_time , "HH:MM:SS")

                if t_eg_request.ex_finishdate == t_eg_request.done_date:

                    if (t_eg_request.ex_finishtime - t_eg_request.done_time) >= 0 and (t_eg_request.ex_finishtime - t_eg_request.done_time) <= calctime:

                        tproperty = query(tproperty_list, filters=(lambda tproperty :tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_list.append(srequest)

                            sRequest.reqnr = t_eg_request.reqnr
                            sRequest.opendate = t_eg_request.opened_date
                            sRequest.process_date = t_eg_request.process_date
                            sRequest.closed_date = t_eg_request.closed_date
                            sRequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            sRequest.ex_finish = full_finish
                            sRequest.done = full_done
                            sRequest.ex_finishdate = t_eg_request.ex_finishdate
                            sRequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            sRequest.done_date = t_eg_request.done_date
                            sRequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            sRequest.memo = t_eg_request.memo
                            sRequest.task_def = t_eg_request.task_def
                            sRequest.task_solv = t_eg_request.task_solv
                            sRequest.pmaintask = tproperty.pmain_nr
                            sRequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.SOURCE = t_eg_request.SOURCE
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

                elif t_eg_request.ex_finishdate > t_eg_request.done_date:
                    calday = t_eg_request.ex_finishdate - t_eg_request.done_date
                    d = (calday * 86399) + t_eg_request.done_time
                    e = d - t_eg_request.ex_finishtime

                    if e >= 0 and e <= calctime:

                        tproperty = query(tproperty_list, filters=(lambda tproperty :tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_list.append(srequest)

                            sRequest.reqnr = t_eg_request.reqnr
                            sRequest.opendate = t_eg_request.opened_date
                            sRequest.process_date = t_eg_request.process_date
                            sRequest.closed_date = t_eg_request.closed_date
                            sRequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            sRequest.ex_finish = full_finish
                            sRequest.done = full_done
                            sRequest.ex_finishdate = t_eg_request.ex_finishdate
                            sRequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            sRequest.done_date = t_eg_request.done_date
                            sRequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            sRequest.memo = t_eg_request.memo
                            sRequest.task_def = t_eg_request.task_def
                            sRequest.task_solv = t_eg_request.task_solv
                            sRequest.pmaintask = tproperty.pmain_nr
                            sRequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.SOURCE = t_eg_request.SOURCE
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

        elif cmb_operand == 3:

            for t_eg_request in query(t_eg_request_list):
                full_finish = to_string(t_eg_request.ex_finishdate , "99/99/99") + " " + to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                full_done = to_string(t_eg_request.done_date , "99/99/99") + " " + to_string(t_eg_request.done_time , "HH:MM:SS")

                if t_eg_request.ex_finishdate == t_eg_request.done_date:

                    if (t_eg_request.done_time - t_eg_request.ex_finishtime) > calctime:

                        tproperty = query(tproperty_list, filters=(lambda tproperty :tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_list.append(srequest)

                            sRequest.reqnr = t_eg_request.reqnr
                            sRequest.opendate = t_eg_request.opened_date
                            sRequest.process_date = t_eg_request.process_date
                            sRequest.closed_date = t_eg_request.closed_date
                            sRequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            sRequest.ex_finish = full_finish
                            sRequest.done = full_done
                            sRequest.ex_finishdate = t_eg_request.ex_finishdate
                            sRequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            sRequest.done_date = t_eg_request.done_date
                            sRequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            sRequest.memo = t_eg_request.memo
                            sRequest.task_def = t_eg_request.task_def
                            sRequest.task_solv = t_eg_request.task_solv
                            sRequest.pmaintask = tproperty.pmain_nr
                            sRequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.SOURCE = t_eg_request.SOURCE
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

                elif t_eg_request.ex_finishdate < t_eg_request.done_date:
                    calday = t_eg_request.done_date - t_eg_request.ex_finishdate
                    d = (calday * 86399) + t_eg_request.done_time
                    e = d - t_eg_request.ex_finishtime

                    if e > calctime:

                        tproperty = query(tproperty_list, filters=(lambda tproperty :tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_list.append(srequest)

                            sRequest.reqnr = t_eg_request.reqnr
                            sRequest.opendate = t_eg_request.opened_date
                            sRequest.process_date = t_eg_request.process_date
                            sRequest.closed_date = t_eg_request.closed_date
                            sRequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            sRequest.ex_finish = full_finish
                            sRequest.done = full_done
                            sRequest.ex_finishdate = t_eg_request.ex_finishdate
                            sRequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            sRequest.done_date = t_eg_request.done_date
                            sRequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            sRequest.memo = t_eg_request.memo
                            sRequest.task_def = t_eg_request.task_def
                            sRequest.task_solv = t_eg_request.task_solv
                            sRequest.pmaintask = tproperty.pmain_nr
                            sRequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.SOURCE = t_eg_request.SOURCE
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

        elif cmb_operand == 4:

            for t_eg_request in query(t_eg_request_list):
                full_finish = to_string(t_eg_request.ex_finishdate , "99/99/99") + " " + to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                full_done = to_string(t_eg_request.done_date , "99/99/99") + " " + to_string(t_eg_request.done_time , "HH:MM:SS")

                if t_eg_request.ex_finishdate == t_eg_request.done_date:

                    if (t_eg_request.done_time - t_eg_request.ex_finishtime) >= calctime:

                        tproperty = query(tproperty_list, filters=(lambda tproperty :tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_list.append(srequest)

                            sRequest.reqnr = t_eg_request.reqnr
                            sRequest.opendate = t_eg_request.opened_date
                            sRequest.process_date = t_eg_request.process_date
                            sRequest.closed_date = t_eg_request.closed_date
                            sRequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            sRequest.ex_finish = full_finish
                            sRequest.done = full_done
                            sRequest.ex_finishdate = t_eg_request.ex_finishdate
                            sRequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            sRequest.done_date = t_eg_request.done_date
                            sRequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            sRequest.memo = t_eg_request.memo
                            sRequest.task_def = t_eg_request.task_def
                            sRequest.task_solv = t_eg_request.task_solv
                            sRequest.pmaintask = tproperty.pmain_nr
                            sRequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.SOURCE = t_eg_request.SOURCE
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

                elif t_eg_request.ex_finishdate < t_eg_request.done_date:
                    calday = t_eg_request.done_date - t_eg_request.ex_finishdate
                    d = (calday * 86399) + t_eg_request.done_time
                    e = d - t_eg_request.ex_finishtime

                    if e >= calctime:

                        tproperty = query(tproperty_list, filters=(lambda tproperty :tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_list.append(srequest)

                            sRequest.reqnr = t_eg_request.reqnr
                            sRequest.opendate = t_eg_request.opened_date
                            sRequest.process_date = t_eg_request.process_date
                            sRequest.closed_date = t_eg_request.closed_date
                            sRequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            sRequest.ex_finish = full_finish
                            sRequest.done = full_done
                            sRequest.ex_finishdate = t_eg_request.ex_finishdate
                            sRequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            sRequest.done_date = t_eg_request.done_date
                            sRequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            sRequest.memo = t_eg_request.memo
                            sRequest.task_def = t_eg_request.task_def
                            sRequest.task_solv = t_eg_request.task_solv
                            sRequest.pmaintask = tproperty.pmain_nr
                            sRequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.SOURCE = t_eg_request.SOURCE
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

        elif cmb_operand == 5:

            for t_eg_request in query(t_eg_request_list):
                full_finish = to_string(t_eg_request.ex_finishdate , "99/99/99") + " " + to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                full_done = to_string(t_eg_request.done_date , "99/99/99") + " " + to_string(t_eg_request.done_time , "HH:MM:SS")

                if t_eg_request.ex_finishdate == t_eg_request.done_date:

                    if (t_eg_request.done_time - t_eg_request.ex_finishtime) >= calctime and (t_eg_request.done_time - t_eg_request.ex_finishtime) <= calctime1:

                        tproperty = query(tproperty_list, filters=(lambda tproperty :tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_list.append(srequest)

                            sRequest.reqnr = t_eg_request.reqnr
                            sRequest.opendate = t_eg_request.opened_date
                            sRequest.process_date = t_eg_request.process_date
                            sRequest.closed_date = t_eg_request.closed_date
                            sRequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            sRequest.ex_finish = full_finish
                            sRequest.done = full_done
                            sRequest.ex_finishdate = t_eg_request.ex_finishdate
                            sRequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            sRequest.done_date = t_eg_request.done_date
                            sRequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            sRequest.memo = t_eg_request.memo
                            sRequest.task_def = t_eg_request.task_def
                            sRequest.task_solv = t_eg_request.task_solv
                            sRequest.pmaintask = tproperty.pmain_nr
                            sRequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.SOURCE = t_eg_request.SOURCE
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

                elif t_eg_request.ex_finishdate < t_eg_request.done_date:
                    calday = t_eg_request.done_date - t_eg_request.ex_finishdate
                    d = (calday * 86399) + t_eg_request.done_time
                    e = d - t_eg_request.ex_finishtime

                    if e >= calctime and e <= calctime1:

                        tproperty = query(tproperty_list, filters=(lambda tproperty :tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_list.append(srequest)

                            sRequest.reqnr = t_eg_request.reqnr
                            sRequest.opendate = t_eg_request.opened_date
                            sRequest.process_date = t_eg_request.process_date
                            sRequest.closed_date = t_eg_request.closed_date
                            sRequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            sRequest.ex_finish = full_finish
                            sRequest.done = full_done
                            sRequest.ex_finishdate = t_eg_request.ex_finishdate
                            sRequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            sRequest.done_date = t_eg_request.done_date
                            sRequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            sRequest.memo = t_eg_request.memo
                            sRequest.task_def = t_eg_request.task_def
                            sRequest.task_solv = t_eg_request.task_solv
                            sRequest.pmaintask = tproperty.pmain_nr
                            sRequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.SOURCE = t_eg_request.SOURCE
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

        for srequest in query(srequest_list, filters=(lambda srequest :srequest.opendate >= fdate and srequest.opendate <= tdate)):
            tsource = db_session.query(Tsource).filter((Tsource.source_nr == srequest.SOURCE) &  (Tsource.source_selected)).first()
            if not tsource:
                continue

            tcategory = db_session.query(Tcategory).filter((Tcategory.categ_nr == srequest.category) &  (Tcategory.categ_selected)).first()
            if not tcategory:
                continue

            tsubtask = db_session.query(Tsubtask).filter((Tsubtask.sub_nr == srequest.sub_task) &  (Tsubtask.sub_selected)).first()
            if not tsubtask:
                continue

            tpic = db_session.query(Tpic).filter((Tpic.pic_nr == srequest.assign_to) &  (Tpic.pic_selected)).first()
            if not tpic:
                continue

            tMaintask = db_session.query(TMaintask).filter((TMaintask.main_nr == srequest.pmaintask) &  (TMaintask.main_selected)).first()
            if not tMaintask:
                continue

            tLocation = db_session.query(TLocation).filter((TLocation.loc_nr == srequest.plocation) &  (TLocation.loc_selected)).first()
            if not tLocation:
                continue

            tproperty = db_session.query(Tproperty).filter((Tproperty.prop_nr == srequest.property) &  (Tproperty.prop_selected)).first()
            if not tproperty:
                continue

            copyrequest = Copyrequest()
            copyrequest_list.append(copyrequest)

            copyRequest.reqnr = srequest.reqnr
            copyRequest.opendate = srequest.opendate
            copyRequest.Source_str = tsource.source_nm
            copyrequest.source_name = srequest.source_name
            copyRequest.process_date = srequest.process_date
            copyRequest.closed_date = srequest.closed_date
            copyRequest.urgency = int_str[int (srequest.urgency) - 1]
            copyRequest.category_str = tcategory.categ_nm
            copyRequest.pmaintask = srequest.pmaintask
            copyRequest.maintask = tMaintask.main_nm
            copyRequest.plocation = srequest.plocation
            copyRequest.location = tLocation.loc_nm
            copyRequest.zinr = srequest.zinr
            copyRequest.property = srequest.property
            copyRequest.property_nm = tproperty.prop_nm
            copyRequest.pic_str = tpic.pic_nm
            copyRequest.sub_str = tsubtask.sub_nm
            copyRequest.ex_finish = srequest.ex_finish
            copyRequest.done = srequest.done
            copyRequest.ex_finishdate = srequest.ex_finishdate
            copyRequest.ex_finishtime = to_string(srequest.ex_finishtime , "HH:MM:SS")
            copyRequest.done_date = srequest.done_date
            copyRequest.done_time = to_string(srequest.done_time , "HH:MM:SS")
            copyRequest.memo = srequest.memo
            copyRequest.task_def = srequest.task_def
            copyRequest.task_solv = srequest.task_solv
            copyRequest.SOURCE = srequest.source
            copyRequest.category = srequest.category
            copyRequest.reqstatus = srequest.reqstatus
            copyRequest.sub_task = srequest.sub_task
            copyRequest.assign_to = srequest.assign_to
            copyRequest.reason = srequest.reason


        OPEN QUERY q1 FOR EACH copyrequest


    int_str[0] = "Low"
    int_str[1] = "Medium"
    int_str[2] = "High"
    open_query()

    return generate_output()