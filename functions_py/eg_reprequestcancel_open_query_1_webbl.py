#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 29/8/2025
# data kosong
# gitlab: 1032
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_request

tsource_data, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":string, "source_selected":bool})
tsubtask_data, Tsubtask = create_model("Tsubtask", {"sub_nr":string, "sub_nm":string, "sub_selected":bool})
tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
tproperty_data, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pmain_nr":int, "pmain":string, "pcateg_nr":int, "pcateg":string, "ploc_nr":int, "ploc":string, "pzinr":string})
tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool, "categ_nr":int, "categ_nm":string})
troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
tstatus_data, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool}, {"loc_selected": True})
tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})

def eg_reprequestcancel_open_query_1_webbl(fdate:date, tdate:date, 
                                            tsource_data:[Tsource], 
                                            tsubtask_data:[Tsubtask], 
                                            tpic_data:[Tpic], 
                                            tproperty_data:[Tproperty], 
                                            tmaintask_data:[Tmaintask], 
                                            troom_data:[Troom], 
                                            tstatus_data:[Tstatus], 
                                            tlocation_data:[Tlocation], 
                                            tcategory_data:[Tcategory]):
    copyrequest_data = []
    int_str:List[string] = ["Low", "Medium", "High"]
    eg_request = None

    t_eg_request = tstatus = tlocation = tmaintask = troom = tproperty = tpic = tsubtask = tsource = tcategory = srequest = copyrequest = comproperty = comstatus = compic = comsource = comsubtask = comcategory = commaintask = comlocation = comroom = None

    t_eg_request_data, T_eg_request = create_model_like(Eg_request)
    srequest_data, Srequest = create_model("Srequest", {"reqnr":int, "opendate":date, "canceldate":date, "cancelby":string, "reason":string, "status_str":string, "source_str":string, "source_name":string, "process_date":date, "closed_date":date, "urgency":string, "category_str":string, "deptnum":int, "pmaintask":int, "maintask":string, "plocation":int, "location":string, "zinr":string, "property":int, "property_nm":string, "pic_str":string, "sub_str":string, "ex_finishdate":date, "memo":string, "task_def":string, "task_solv":string, "source":int, "category":int, "reqstatus":int, "sub_task":string, "assign_to":int})
    copyrequest_data, Copyrequest = create_model("Copyrequest", {"reqnr":int, "opendate":date, "canceldate":date, "cancelby":string, "reason":string, "status_str":string, "source_str":string, "source_name":string, "process_date":date, "closed_date":date, "urgency":string, "category_str":string, "deptnum":int, "pmaintask":int, "maintask":string, "plocation":int, "location":string, "zinr":string, "property":int, "property_nm":string, "pic_str":string, "sub_str":string, "ex_finishdate":date, "memo":string, "task_def":string, "task_solv":string, "source":int, "category":int, "reqstatus":int, "sub_task":string, "assign_to":int, "str":string})

    Comproperty = Tproperty
    comproperty_data = tproperty_data

    Comstatus = Tstatus
    comstatus_data = tstatus_data

    Compic = Tpic
    compic_data = tpic_data

    Comsource = Tsource
    comsource_data = tsource_data

    Comsubtask = Tsubtask
    comsubtask_data = tsubtask_data

    Comcategory = Tcategory
    comcategory_data = tcategory_data

    Commaintask = Tmaintask
    commaintask_data = tmaintask_data

    Comlocation = Tlocation
    comlocation_data = tlocation_data

    Comroom = Troom
    comroom_data = troom_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal copyrequest_data, int_str, eg_request
        nonlocal fdate, tdate
        nonlocal comproperty, comstatus, compic, comsource, comsubtask, comcategory, commaintask, comlocation, comroom


        nonlocal t_eg_request, tstatus, tlocation, tmaintask, troom, tproperty, tpic, tsubtask, tsource, tcategory, srequest, copyrequest, comproperty, comstatus, compic, comsource, comsubtask, comcategory, commaintask, comlocation, comroom
        nonlocal t_eg_request_data, srequest_data, copyrequest_data

        return {"copyRequest": copyrequest_data, "status": tstatus_data}

    print("ST:", fdate, tstatus_data)

    for eg_request in db_session.query(Eg_request).filter(
             (Eg_request.cancel_date >= fdate) & (Eg_request.cancel_date <= tdate) & (Eg_request.delete_flag)).order_by(Eg_request._recid).all():
        t_eg_request = T_eg_request()
        t_eg_request_data.append(t_eg_request)
        buffer_copy(eg_request, t_eg_request)
        # print(t_eg_request)

    # for t_eg_request in query(t_eg_request_data):
    for t_eg_request in t_eg_request_data:
        # print(t_eg_request.propertynr)
        if t_eg_request.propertynr == 0:
            srequest = Srequest()
            srequest_data.append(srequest)

            srequest.reqnr = t_eg_request.reqnr
            srequest.opendate = t_eg_request.opened_date
            srequest.process_date = t_eg_request.process_date
            srequest.closed_date = t_eg_request.closed_date
            srequest.urgency = to_string(t_eg_request.urgency)
            srequest.source_name = t_eg_request.source_name
            srequest.ex_finishdate = t_eg_request.ex_finishdate
            srequest.memo = t_eg_request.memo
            srequest.task_def = t_eg_request.task_def
            srequest.task_solv = t_eg_request.task_solv
            srequest.pmaintask = t_eg_request.maintask
            srequest.plocation = t_eg_request.reserve_int
            srequest.zinr = t_eg_request.zinr
            srequest.source = t_eg_request.source
            srequest.category = t_eg_request.category
            srequest.reqstatus = t_eg_request.reqstatus
            srequest.sub_task = t_eg_request.sub_task
            srequest.assign_to = t_eg_request.assign_to
            srequest.property = t_eg_request.propertynr
            srequest.canceldate = t_eg_request.cancel_date
            srequest.cancelby = t_eg_request.cancel_by
            srequest.reason = t_eg_request.char1


        else:

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
                srequest.ex_finishdate = t_eg_request.ex_finishdate
                srequest.memo = t_eg_request.memo
                srequest.task_def = t_eg_request.task_def
                srequest.task_solv = t_eg_request.task_solv
                srequest.pmaintask = tproperty.pmain_nr
                srequest.plocation = t_eg_request.reserve_int
                srequest.zinr = t_eg_request.zinr
                srequest.source = t_eg_request.source
                srequest.category = tproperty.pcateg_nr
                srequest.reqstatus = t_eg_request.reqstatus
                srequest.sub_task = t_eg_request.sub_task
                srequest.assign_to = t_eg_request.assign_to
                srequest.property = t_eg_request.propertynr
                srequest.canceldate = t_eg_request.cancel_date
                srequest.cancelby = t_eg_request.cancel_by
                srequest.reason = t_eg_request.char1

    for srequest in query(srequest_data):
        print("SR:", srequest.reqstatus)
        tstatus = query(tstatus_data, (lambda tstatus: tstatus.stat_nr == srequest.reqstatus and tstatus.stat_selected), first=True)
        if not tstatus:
            continue

        tsource = query(tsource_data, (lambda tsource: tsource.source_nr == srequest.source and tsource.source_selected), first=True)
        if not tsource:
            continue

        tcategory = query(tcategory_data, (lambda tcategory: tcategory.categ_nr == srequest.category and tcategory.categ_selected), first=True)
        if not tcategory:
            continue

        # Rd 29/8/2025
        # tSubtask = query(tSubtask_data, (lambda tSubtask: tSubtask.sub_nr == srequest.sub_task and tSubtask.sub_selected), first=True)
        tSubtask = query(tsubtask_data, (lambda tSubtask: tSubtask.sub_nr == srequest.sub_task and tSubtask.sub_selected), first=True)
        if not tSubtask:
            continue

        tpic = query(tpic_data, (lambda tpic: tpic.pic_nr == srequest.assign_to and tpic.pic_selected), first=True)
        if not tpic:
            continue

        tmaintask = query(tmaintask_data, (lambda tmaintask: tmaintask.main_nr == srequest.pmaintask and tmaintask.main_selected), first=True)
        if not tmaintask:
            continue

        tlocation = query(tlocation_data, (lambda tlocation: tlocation.loc_nr == srequest.plocation and tlocation.loc_selected), first=True)
        if not tlocation:
            continue

        tproperty = query(tproperty_data, (lambda tproperty: tproperty.prop_nr == srequest.property and tproperty.prop_selected), first=True)
        if not tproperty:
            continue

        copyrequest = Copyrequest()
        copyrequest_data.append(copyrequest)

        copyrequest.reqnr = srequest.reqnr
        copyrequest.opendate = srequest.opendate
        copyrequest.status_str = tstatus.stat_nm
        copyrequest.source_str = tsource.source_nm
        copyrequest.process_date = srequest.process_date
        copyrequest.closed_date = srequest.closed_date
        copyrequest.urgency = int_str[int (srequest.urgency) - 1]
        copyrequest.category_str = tcategory.categ_nm
        copyrequest.pmaintask = srequest.pmaintask
        copyrequest.maintask = tmaintask.main_nm
        copyrequest.plocation = srequest.plocation
        copyrequest.location = tlocation.loc_nm
        copyrequest.zinr = srequest.zinr
        copyrequest.property = srequest.property
        copyrequest.property_nm = tproperty.prop_nm
        copyrequest.pic_str = tpic.pic_nm
        copyrequest.sub_str = tSubtask.sub_nm
        copyrequest.ex_finishdate = srequest.ex_finishdate
        copyrequest.memo = srequest.memo
        copyrequest.task_def = srequest.task_def
        copyrequest.task_solv = srequest.task_solv
        copyrequest.source = srequest.source
        copyrequest.category = srequest.category
        copyrequest.reqstatus = srequest.reqstatus
        copyrequest.sub_task = srequest.sub_task
        copyrequest.assign_to = srequest.assign_to
        copyrequest.canceldate = srequest.canceldate
        copyrequest.cancelby = srequest.cancelby
        copyrequest.reason = srequest.reason
        copyrequest.source_name = srequest.source_name

    return generate_output()