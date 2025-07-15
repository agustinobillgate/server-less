#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.eg_repduration_all_locationbl import eg_repduration_all_locationbl
from functions.eg_repduration_open_querybl import eg_repduration_open_querybl
from models import Eg_request

tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
tsubtask_data, Tsubtask = create_model("Tsubtask", {"sub_nr":string, "sub_nm":string, "sub_selected":bool})
tsource_data, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":string, "source_selected":bool})
tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})

def eg_repduration_disp_webbl(all_room:bool, all_property:bool, all_pic:bool, all_subtask:bool, all_source:bool, all_category:bool, all_location:bool, all_maintask:bool, cmb_operand:int, fdate:date, tdate:date, calctime:int, calctime1:int, tpic_data:[Tpic], tsubtask_data:[Tsubtask], tsource_data:[Tsource], tcategory_data:[Tcategory], tlocation_data:[Tlocation], tmaintask_data:[Tmaintask]):
    tproperty_data = []
    troom_data = []
    copyrequest_data = []
    int_str:List[string] = create_empty_list(3,"")
    eg_request = None

    t_eg_request = srequest = copyrequest = tproperty = tpic = tsubtask = tsource = tcategory = tlocation = tmaintask = troom = None

    t_eg_request_data, T_eg_request = create_model_like(Eg_request)
    srequest_data, Srequest = create_model("Srequest", {"reqnr":int, "opendate":date, "status_str":string, "source_str":string, "source_name":string, "process_date":date, "closed_date":date, "urgency":string, "category_str":string, "deptnum":int, "pmaintask":int, "maintask":string, "plocation":int, "location":string, "zinr":string, "property":int, "property_nm":string, "pic_str":string, "sub_str":string, "ex_finishdate":date, "ex_finishtime":string, "ex_finish":string, "done_date":date, "done_time":string, "done":string, "memo":string, "task_def":string, "task_solv":string, "source":int, "category":int, "reqstatus":int, "sub_task":string, "assign_to":int, "reason":string})
    copyrequest_data, Copyrequest = create_model("Copyrequest", {"reqnr":int, "opendate":date, "status_str":string, "source_str":string, "source_name":string, "process_date":date, "closed_date":date, "urgency":string, "category_str":string, "deptnum":int, "pmaintask":int, "maintask":string, "plocation":int, "location":string, "zinr":string, "property":int, "property_nm":string, "pic_str":string, "sub_str":string, "ex_finishdate":date, "ex_finishtime":string, "ex_finish":string, "done_date":date, "done_time":string, "done":string, "memo":string, "task_def":string, "task_solv":string, "source":int, "category":int, "reqstatus":int, "sub_task":string, "assign_to":int, "reason":string, "str":string})
    tproperty_data, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tproperty_data, troom_data, copyrequest_data, int_str, eg_request
        nonlocal all_room, all_property, all_pic, all_subtask, all_source, all_category, all_location, all_maintask, cmb_operand, fdate, tdate, calctime, calctime1


        nonlocal t_eg_request, srequest, copyrequest, tproperty, tpic, tsubtask, tsource, tcategory, tlocation, tmaintask, troom
        nonlocal t_eg_request_data, srequest_data, copyrequest_data, tproperty_data, troom_data

        return {"tpic": tpic_data, "tsubtask": tsubtask_data, "tsource": tsource_data, "tcategory": tcategory_data, "tLocation": tlocation_data, "tMaintask": tmaintask_data, "tproperty": tproperty_data, "troom": troom_data, "copyRequest": copyrequest_data}

    def open_query():

        nonlocal tproperty_data, troom_data, copyrequest_data, int_str, eg_request
        nonlocal all_room, all_property, all_pic, all_subtask, all_source, all_category, all_location, all_maintask, cmb_operand, fdate, tdate, calctime, calctime1


        nonlocal t_eg_request, srequest, copyrequest, tproperty, tpic, tsubtask, tsource, tcategory, tlocation, tmaintask, troom
        nonlocal t_eg_request_data, srequest_data, copyrequest_data, tproperty_data, troom_data

        d:int = 0
        e:int = 0
        calday:int = 0
        full_finish:string = ""
        full_done:string = ""
        troom_data, tproperty_data = get_output(eg_repduration_all_locationbl(all_room, tlocation_data, tmaintask_data))

        if all_property:

            for tproperty in query(tproperty_data):
                tproperty.prop_selected = True


        if all_pic:

            for tpic in query(tpic_data):
                tpic.pic_selected = True


        if all_subtask:

            for tsubtask in query(tsubtask_data):
                tsubtask.sub_selected = True


        if all_source:

            for tsource in query(tsource_data):
                tsource.source_selected = True


        if all_category:

            for tcategory in query(tcategory_data):
                tcategory.categ_selected = True


        if all_location:

            for tlocation in query(tlocation_data):
                tlocation.loc_selected = True


        if all_maintask:

            for tmaintask in query(tmaintask_data):
                tmaintask.main_selected = True

        srequest_data.clear()
        copyrequest_data.clear()
        t_eg_request_data = get_output(eg_repduration_open_querybl(fdate, tdate))

        if cmb_operand == 1:

            for t_eg_request in query(t_eg_request_data):
                full_finish = to_string(t_eg_request.ex_finishdate , "99/99/99") + " " + to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                full_done = to_string(t_eg_request.done_date , "99/99/99") + " " + to_string(t_eg_request.done_time , "HH:MM:SS")

                if t_eg_request.ex_finishdate == t_eg_request.done_date:

                    if (t_eg_request.ex_finishtime - t_eg_request.done_time) >= 0 and (t_eg_request.ex_finishtime - t_eg_request.done_time) < calctime:

                        tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_data.append(srequest)

                            srequest.reqnr = t_eg_request.reqnr
                            srequest.opendate = t_eg_request.opened_date
                            srequest.process_date = t_eg_request.process_date
                            srequest.closed_date = t_eg_request.closed_date
                            srequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            srequest.ex_finish = full_finish
                            srequest.done = full_done
                            srequest.ex_finishdate = t_eg_request.ex_finishdate
                            srequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            srequest.done_date = t_eg_request.done_date
                            srequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            srequest.memo = t_eg_request.memo
                            srequest.task_def = t_eg_request.task_def
                            srequest.task_solv = t_eg_request.task_solv
                            srequest.pmaintask = tproperty.pmain_nr
                            srequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.source = t_eg_request.source
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

                elif t_eg_request.ex_finishdate > t_eg_request.done_date:
                    calday = (t_eg_request.ex_finishdate - t_eg_request.done_date).days
                    d = (calday * 86399) + t_eg_request.done_time
                    e = d - t_eg_request.ex_finishtime

                    if e >= 0 and e < calctime:

                        tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_data.append(srequest)

                            srequest.reqnr = t_eg_request.reqnr
                            srequest.opendate = t_eg_request.opened_date
                            srequest.process_date = t_eg_request.process_date
                            srequest.closed_date = t_eg_request.closed_date
                            srequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            srequest.ex_finish = full_finish
                            srequest.done = full_done
                            srequest.ex_finishdate = t_eg_request.ex_finishdate
                            srequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            srequest.done_date = t_eg_request.done_date
                            srequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            srequest.memo = t_eg_request.memo
                            srequest.task_def = t_eg_request.task_def
                            srequest.task_solv = t_eg_request.task_solv
                            srequest.pmaintask = tproperty.pmain_nr
                            srequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.source = t_eg_request.source
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

        elif cmb_operand == 2:

            for t_eg_request in query(t_eg_request_data):
                full_finish = to_string(t_eg_request.ex_finishdate , "99/99/99") + " " + to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                full_done = to_string(t_eg_request.done_date , "99/99/99") + " " + to_string(t_eg_request.done_time , "HH:MM:SS")

                if t_eg_request.ex_finishdate == t_eg_request.done_date:

                    if (t_eg_request.ex_finishtime - t_eg_request.done_time) >= 0 and (t_eg_request.ex_finishtime - t_eg_request.done_time) <= calctime:

                        tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_data.append(srequest)

                            srequest.reqnr = t_eg_request.reqnr
                            srequest.opendate = t_eg_request.opened_date
                            srequest.process_date = t_eg_request.process_date
                            srequest.closed_date = t_eg_request.closed_date
                            srequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            srequest.ex_finish = full_finish
                            srequest.done = full_done
                            srequest.ex_finishdate = t_eg_request.ex_finishdate
                            srequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            srequest.done_date = t_eg_request.done_date
                            srequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            srequest.memo = t_eg_request.memo
                            srequest.task_def = t_eg_request.task_def
                            srequest.task_solv = t_eg_request.task_solv
                            srequest.pmaintask = tproperty.pmain_nr
                            srequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.source = t_eg_request.source
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

                elif t_eg_request.ex_finishdate > t_eg_request.done_date:
                    calday = (t_eg_request.ex_finishdate - t_eg_request.done_date).days
                    d = (calday * 86399) + t_eg_request.done_time
                    e = d - t_eg_request.ex_finishtime

                    if e >= 0 and e <= calctime:

                        tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_data.append(srequest)

                            srequest.reqnr = t_eg_request.reqnr
                            srequest.opendate = t_eg_request.opened_date
                            srequest.process_date = t_eg_request.process_date
                            srequest.closed_date = t_eg_request.closed_date
                            srequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            srequest.ex_finish = full_finish
                            srequest.done = full_done
                            srequest.ex_finishdate = t_eg_request.ex_finishdate
                            srequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            srequest.done_date = t_eg_request.done_date
                            srequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            srequest.memo = t_eg_request.memo
                            srequest.task_def = t_eg_request.task_def
                            srequest.task_solv = t_eg_request.task_solv
                            srequest.pmaintask = tproperty.pmain_nr
                            srequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.source = t_eg_request.source
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

        elif cmb_operand == 3:

            for t_eg_request in query(t_eg_request_data):
                full_finish = to_string(t_eg_request.ex_finishdate , "99/99/99") + " " + to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                full_done = to_string(t_eg_request.done_date , "99/99/99") + " " + to_string(t_eg_request.done_time , "HH:MM:SS")

                if t_eg_request.ex_finishdate == t_eg_request.done_date:

                    if (t_eg_request.done_time - t_eg_request.ex_finishtime) > calctime:

                        tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_data.append(srequest)

                            srequest.reqnr = t_eg_request.reqnr
                            srequest.opendate = t_eg_request.opened_date
                            srequest.process_date = t_eg_request.process_date
                            srequest.closed_date = t_eg_request.closed_date
                            srequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            srequest.ex_finish = full_finish
                            srequest.done = full_done
                            srequest.ex_finishdate = t_eg_request.ex_finishdate
                            srequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            srequest.done_date = t_eg_request.done_date
                            srequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            srequest.memo = t_eg_request.memo
                            srequest.task_def = t_eg_request.task_def
                            srequest.task_solv = t_eg_request.task_solv
                            srequest.pmaintask = tproperty.pmain_nr
                            srequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.source = t_eg_request.source
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

                elif t_eg_request.ex_finishdate < t_eg_request.done_date:
                    calday = (t_eg_request.done_date - t_eg_request.ex_finishdate).days
                    d = (calday * 86399) + t_eg_request.done_time
                    e = d - t_eg_request.ex_finishtime

                    if e > calctime:

                        tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_data.append(srequest)

                            srequest.reqnr = t_eg_request.reqnr
                            srequest.opendate = t_eg_request.opened_date
                            srequest.process_date = t_eg_request.process_date
                            srequest.closed_date = t_eg_request.closed_date
                            srequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            srequest.ex_finish = full_finish
                            srequest.done = full_done
                            srequest.ex_finishdate = t_eg_request.ex_finishdate
                            srequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            srequest.done_date = t_eg_request.done_date
                            srequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            srequest.memo = t_eg_request.memo
                            srequest.task_def = t_eg_request.task_def
                            srequest.task_solv = t_eg_request.task_solv
                            srequest.pmaintask = tproperty.pmain_nr
                            srequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.source = t_eg_request.source
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

        elif cmb_operand == 4:

            for t_eg_request in query(t_eg_request_data):
                full_finish = to_string(t_eg_request.ex_finishdate , "99/99/99") + " " + to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                full_done = to_string(t_eg_request.done_date , "99/99/99") + " " + to_string(t_eg_request.done_time , "HH:MM:SS")

                if t_eg_request.ex_finishdate == t_eg_request.done_date:

                    if (t_eg_request.done_time - t_eg_request.ex_finishtime) >= calctime:

                        tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_data.append(srequest)

                            srequest.reqnr = t_eg_request.reqnr
                            srequest.opendate = t_eg_request.opened_date
                            srequest.process_date = t_eg_request.process_date
                            srequest.closed_date = t_eg_request.closed_date
                            srequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            srequest.ex_finish = full_finish
                            srequest.done = full_done
                            srequest.ex_finishdate = t_eg_request.ex_finishdate
                            srequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            srequest.done_date = t_eg_request.done_date
                            srequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            srequest.memo = t_eg_request.memo
                            srequest.task_def = t_eg_request.task_def
                            srequest.task_solv = t_eg_request.task_solv
                            srequest.pmaintask = tproperty.pmain_nr
                            srequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.source = t_eg_request.source
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

                elif t_eg_request.ex_finishdate < t_eg_request.done_date:
                    calday = (t_eg_request.done_date - t_eg_request.ex_finishdate).days
                    d = (calday * 86399) + t_eg_request.done_time
                    e = d - t_eg_request.ex_finishtime

                    if e >= calctime:

                        tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_data.append(srequest)

                            srequest.reqnr = t_eg_request.reqnr
                            srequest.opendate = t_eg_request.opened_date
                            srequest.process_date = t_eg_request.process_date
                            srequest.closed_date = t_eg_request.closed_date
                            srequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            srequest.ex_finish = full_finish
                            srequest.done = full_done
                            srequest.ex_finishdate = t_eg_request.ex_finishdate
                            srequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            srequest.done_date = t_eg_request.done_date
                            srequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            srequest.memo = t_eg_request.memo
                            srequest.task_def = t_eg_request.task_def
                            srequest.task_solv = t_eg_request.task_solv
                            srequest.pmaintask = tproperty.pmain_nr
                            srequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.source = t_eg_request.source
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

        elif cmb_operand == 5:

            for t_eg_request in query(t_eg_request_data):
                full_finish = to_string(t_eg_request.ex_finishdate , "99/99/99") + " " + to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                full_done = to_string(t_eg_request.done_date , "99/99/99") + " " + to_string(t_eg_request.done_time , "HH:MM:SS")

                if t_eg_request.ex_finishdate == t_eg_request.done_date:

                    if (t_eg_request.done_time - t_eg_request.ex_finishtime) >= calctime and (t_eg_request.done_time - t_eg_request.ex_finishtime) <= calctime1:

                        tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_data.append(srequest)

                            srequest.reqnr = t_eg_request.reqnr
                            srequest.opendate = t_eg_request.opened_date
                            srequest.process_date = t_eg_request.process_date
                            srequest.closed_date = t_eg_request.closed_date
                            srequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            srequest.ex_finish = full_finish
                            srequest.done = full_done
                            srequest.ex_finishdate = t_eg_request.ex_finishdate
                            srequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            srequest.done_date = t_eg_request.done_date
                            srequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            srequest.memo = t_eg_request.memo
                            srequest.task_def = t_eg_request.task_def
                            srequest.task_solv = t_eg_request.task_solv
                            srequest.pmaintask = tproperty.pmain_nr
                            srequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.source = t_eg_request.source
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

                elif t_eg_request.ex_finishdate < t_eg_request.done_date:
                    calday = (t_eg_request.done_date - t_eg_request.ex_finishdate).days
                    d = (calday * 86399) + t_eg_request.done_time
                    e = d - t_eg_request.ex_finishtime

                    if e >= calctime and e <= calctime1:

                        tproperty = query(tproperty_data, filters=(lambda tproperty: tproperty.prop_nr == t_eg_request.propertynr), first=True)

                        if tproperty:
                            srequest = Srequest()
                            srequest_data.append(srequest)

                            srequest.reqnr = t_eg_request.reqnr
                            srequest.opendate = t_eg_request.opened_date
                            srequest.process_date = t_eg_request.process_date
                            srequest.closed_date = t_eg_request.closed_date
                            srequest.urgency = to_string(t_eg_request.urgency)
                            srequest.source_name = t_eg_request.source_name
                            srequest.ex_finish = full_finish
                            srequest.done = full_done
                            srequest.ex_finishdate = t_eg_request.ex_finishdate
                            srequest.ex_finishtime = to_string(t_eg_request.ex_finishtime , "HH:MM:SS")
                            srequest.done_date = t_eg_request.done_date
                            srequest.done_time = to_string(t_eg_request.done_time, "HH:MM:SS")
                            srequest.memo = t_eg_request.memo
                            srequest.task_def = t_eg_request.task_def
                            srequest.task_solv = t_eg_request.task_solv
                            srequest.pmaintask = tproperty.pmain_nr
                            srequest.plocation = tproperty.ploc_nr
                            srequest.zinr = t_eg_request.zinr
                            srequest.source = t_eg_request.source
                            srequest.category = tproperty.pcateg_nr
                            srequest.reqstatus = t_eg_request.reqstatus
                            srequest.sub_task = t_eg_request.sub_task
                            srequest.assign_to = t_eg_request.assign_to
                            srequest.property = t_eg_request.propertynr
                            srequest.reason = t_eg_request.reasondonetime

        for srequest in query(srequest_data, filters=(lambda srequest: srequest.opendate >= fdate and srequest.opendate <= tdate)):
            tsource = query(tsource_data, (lambda tsource: tsource.source_nr == srequest.source and tsource.source_selected), first=True)
            if not tsource:
                continue

            tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == srequest.category and tcategory.categ_selected), first=True)
            if not tcategory:
                continue

            tsubtask = query(tsubtask_data, (lambda tsubtask: tsubtask.sub_nr == srequest.sub_task and tsubtask.sub_selected), first=True)
            if not tsubtask:
                continue

            tpic = query(tpic_data, (lambda tpic: tpic.pic_nr == srequest.assign_to and tpic.pic_selected), first=True)
            if not tpic:
                continue

            tMaintask = query(tmaintask_data, (lambda tMaintask: tMaintask.main_nr == srequest.pmaintask and tMaintask.main_selected), first=True)
            if not tMaintask:
                continue

            tLocation = query(tlocation_data, (lambda tLocation: tLocation.loc_nr == srequest.plocation and tLocation.loc_selected), first=True)
            if not tLocation:
                continue

            tproperty = query(tproperty_data, (lambda tproperty: tproperty.prop_nr == srequest.property and tproperty.prop_selected), first=True)
            if not tproperty:
                continue

            copyrequest = Copyrequest()
            copyrequest_data.append(copyrequest)

            copyrequest.reqnr = srequest.reqnr
            copyrequest.opendate = srequest.opendate
            copyrequest.source_str = tsource.source_nm
            copyrequest.source_name = srequest.source_name
            copyrequest.process_date = srequest.process_date
            copyrequest.closed_date = srequest.closed_date
            copyrequest.urgency = int_str[int (srequest.urgency) - 1]
            copyrequest.category_str = tcategory.categ_nm
            copyrequest.pmaintask = srequest.pmaintask
            copyrequest.maintask = tMaintask.main_nm
            copyrequest.plocation = srequest.plocation
            copyrequest.location = tLocation.loc_nm
            copyrequest.zinr = srequest.zinr
            copyrequest.property = srequest.property
            copyrequest.property_nm = tproperty.prop_nm
            copyrequest.pic_str = tpic.pic_nm
            copyrequest.sub_str = tsubtask.sub_nm
            copyrequest.ex_finish = srequest.ex_finish
            copyrequest.done = srequest.done
            copyrequest.ex_finishdate = srequest.ex_finishdate
            copyrequest.ex_finishtime = to_string(srequest.ex_finishtime , "HH:MM:SS")
            copyrequest.done_date = srequest.done_date
            copyrequest.done_time = to_string(srequest.done_time , "HH:MM:SS")
            copyrequest.memo = srequest.memo
            copyrequest.task_def = srequest.task_def
            copyrequest.task_solv = srequest.task_solv
            copyrequest.source = srequest.source
            copyrequest.category = srequest.category
            copyrequest.reqstatus = srequest.reqstatus
            copyrequest.sub_task = srequest.sub_task
            copyrequest.assign_to = srequest.assign_to
            copyrequest.reason = srequest.reason

    int_str[0] = "Low"
    int_str[1] = "Medium"
    int_str[2] = "High"
    open_query()

    return generate_output()