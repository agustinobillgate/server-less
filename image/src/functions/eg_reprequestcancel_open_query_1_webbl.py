from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_request

def eg_reprequestcancel_open_query_1_webbl(fdate:date, tdate:date, tsource:[Tsource], tsubtask:[Tsubtask], tpic:[Tpic], tproperty:[Tproperty], tmaintask:[Tmaintask], troom:[Troom], tstatus:[Tstatus], tlocation:[Tlocation], tcategory:[Tcategory]):
    copyrequest_list = []
    int_str:[str] = ["", "", "", ""]
    eg_request = None

    t_eg_request = tstatus = tlocation = tmaintask = troom = tproperty = tpic = tsubtask = tsource = tcategory = srequest = copyrequest = comproperty = comstatus = compic = comsource = comsubtask = comcategory = commaintask = comlocation = comroom = None

    t_eg_request_list, T_eg_request = create_model_like(Eg_request)
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":str, "stat_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool}, {"loc_selected": True})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool, "categ_nr":int, "categ_nm":str})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pmain_nr":int, "pmain":str, "pcateg_nr":int, "pcateg":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool, "pic_dept":int})
    tsubtask_list, Tsubtask = create_model("Tsubtask", {"sub_nr":str, "sub_nm":str, "sub_selected":bool})
    tsource_list, Tsource = create_model("Tsource", {"source_nr":int, "source_nm":str, "source_selected":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})
    srequest_list, Srequest = create_model("Srequest", {"reqnr":int, "opendate":date, "canceldate":date, "cancelby":str, "reason":str, "status_str":str, "source_str":str, "source_name":str, "process_date":date, "closed_date":date, "urgency":str, "category_str":str, "deptnum":int, "pmaintask":int, "maintask":str, "plocation":int, "location":str, "zinr":str, "property":int, "property_nm":str, "pic_str":str, "sub_str":str, "ex_finishdate":date, "memo":str, "task_def":str, "task_solv":str, "source":int, "category":int, "reqstatus":int, "sub_task":str, "assign_to":int})
    copyrequest_list, Copyrequest = create_model("Copyrequest", {"reqnr":int, "opendate":date, "canceldate":date, "cancelby":str, "reason":str, "status_str":str, "source_str":str, "source_name":str, "process_date":date, "closed_date":date, "urgency":str, "category_str":str, "deptnum":int, "pmaintask":int, "maintask":str, "plocation":int, "location":str, "zinr":str, "property":int, "property_nm":str, "pic_str":str, "sub_str":str, "ex_finishdate":date, "memo":str, "task_def":str, "task_solv":str, "source":int, "category":int, "reqstatus":int, "sub_task":str, "assign_to":int, "str":str})

    Comproperty = Tproperty
    comproperty_list = tproperty_list

    Comstatus = Tstatus
    comstatus_list = tstatus_list

    Compic = Tpic
    compic_list = tpic_list

    Comsource = Tsource
    comsource_list = tsource_list

    Comsubtask = Tsubtask
    comsubtask_list = tsubtask_list

    Comcategory = Tcategory
    comcategory_list = tcategory_list

    Commaintask = Tmaintask
    commaintask_list = tmaintask_list

    Comlocation = Tlocation
    comlocation_list = tlocation_list

    Comroom = Troom
    comroom_list = troom_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal copyrequest_list, int_str, eg_request
        nonlocal comproperty, comstatus, compic, comsource, comsubtask, comcategory, commaintask, comlocation, comroom


        nonlocal t_eg_request, tstatus, tlocation, tmaintask, troom, tproperty, tpic, tsubtask, tsource, tcategory, srequest, copyrequest, comproperty, comstatus, compic, comsource, comsubtask, comcategory, commaintask, comlocation, comroom
        nonlocal t_eg_request_list, tstatus_list, tlocation_list, tmaintask_list, troom_list, tproperty_list, tpic_list, tsubtask_list, tsource_list, tcategory_list, srequest_list, copyrequest_list
        return {"copyRequest": copyrequest_list}


    for eg_request in db_session.query(Eg_request).filter(
            (Eg_request.cancel_date >= fdate) &  (Eg_request.cancel_date <= tdate) &  (Eg_request.delete_flag)).all():
        t_eg_request = T_eg_request()
        t_eg_request_list.append(t_eg_request)

        buffer_copy(eg_request, t_eg_request)

    for t_eg_request in query(t_eg_request_list):

        if t_eg_request.propertynr == 0:
            srequest = Srequest()
            srequest_list.append(srequest)

            sRequest.reqnr = t_eg_request.reqnr
            sRequest.opendate = t_eg_request.opened_date
            sRequest.process_date = t_eg_request.process_date
            sRequest.closed_date = t_eg_request.closed_date
            sRequest.urgency = to_string(t_eg_request.urgency)
            srequest.source_name = t_eg_request.source_name
            sRequest.ex_finishdate = t_eg_request.ex_finishdate
            sRequest.memo = t_eg_request.memo
            sRequest.task_def = t_eg_request.task_def
            sRequest.task_solv = t_eg_request.task_solv
            sRequest.pmaintask = t_eg_request.maintask
            sRequest.plocation = t_eg_request.reserve_int
            srequest.zinr = t_eg_request.zinr
            srequest.SOURCE = t_eg_request.SOURCE
            srequest.category = t_eg_request.category
            srequest.reqstatus = t_eg_request.reqstatus
            srequest.sub_task = t_eg_request.sub_task
            srequest.assign_to = t_eg_request.assign_to
            srequest.property = t_eg_request.propertynr
            srequest.canceldate = t_eg_request.cancel_date
            srequest.cancelby = t_eg_request.cancel_by
            srequest.reason = t_eg_request.char1


        else:

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
                sRequest.ex_finishdate = t_eg_request.ex_finishdate
                sRequest.memo = t_eg_request.memo
                sRequest.task_def = t_eg_request.task_def
                sRequest.task_solv = t_eg_request.task_solv
                sRequest.pmaintask = tproperty.pmain_nr
                sRequest.plocation = t_eg_request.reserve_int
                srequest.zinr = t_eg_request.zinr
                srequest.SOURCE = t_eg_request.SOURCE
                srequest.category = tproperty.pcateg_nr
                srequest.reqstatus = t_eg_request.reqstatus
                srequest.sub_task = t_eg_request.sub_task
                srequest.assign_to = t_eg_request.assign_to
                srequest.property = t_eg_request.propertynr
                srequest.canceldate = t_eg_request.cancel_date
                srequest.cancelby = t_eg_request.cancel_by
                srequest.reason = t_eg_request.char1

    for srequest in query(srequest_list):
        tStatus = db_session.query(TStatus).filter((TStatus.stat_nr == srequest.reqstatus) &  (TStatus.stat_selected)).first()
        if not tStatus:
            continue

        tsource = db_session.query(Tsource).filter((Tsource.source_nr == srequest.SOURCE) &  (Tsource.source_selected)).first()
        if not tsource:
            continue

        tcategory = db_session.query(Tcategory).filter((Tcategory.categ_nr == srequest.category) &  (Tcategory.categ_selected)).first()
        if not tcategory:
            continue

        tSubtask = db_session.query(TSubtask).filter((TSubtask.sub_nr == srequest.sub_task) &  (TSubtask.sub_selected)).first()
        if not tSubtask:
            continue

        tpic = db_session.query(Tpic).filter((Tpic.pic_nr == srequest.assign_to) &  (Tpic.pic_selected)).first()
        if not tpic:
            continue

        tmaintask = db_session.query(Tmaintask).filter((Tmaintask.main_nr == srequest.pmaintask) &  (Tmaintask.main_selected)).first()
        if not tmaintask:
            continue

        tlocation = db_session.query(Tlocation).filter((Tlocation.loc_nr == srequest.plocation) &  (Tlocation.loc_selected)).first()
        if not tlocation:
            continue

        tproperty = db_session.query(Tproperty).filter((Tproperty.prop_nr == srequest.property) &  (Tproperty.prop_selected)).first()
        if not tproperty:
            continue

        copyrequest = Copyrequest()
        copyrequest_list.append(copyrequest)

        copyRequest.reqnr = srequest.reqnr
        copyRequest.opendate = srequest.opendate
        copyRequest.status_str = tStatus.stat_nm
        copyRequest.Source_str = tsource.source_nm
        copyRequest.process_date = srequest.process_date
        copyRequest.closed_date = srequest.closed_date
        copyRequest.urgency = int_str[int (srequest.urgency) - 1]
        copyRequest.category_str = tcategory.categ_nm
        copyRequest.pmaintask = srequest.pmaintask
        copyRequest.maintask = tmaintask.main_nm
        copyRequest.plocation = srequest.plocation
        copyRequest.location = tlocation.loc_nm
        copyRequest.zinr = srequest.zinr
        copyRequest.property = srequest.property
        copyRequest.property_nm = tproperty.prop_nm
        copyRequest.pic_str = tpic.pic_nm
        copyRequest.sub_str = tSubtask.sub_nm
        copyRequest.ex_finishdate = srequest.ex_finishdate
        copyRequest.memo = srequest.memo
        copyRequest.task_def = srequest.task_def
        copyRequest.task_solv = srequest.task_solv
        copyRequest.SOURCE = srequest.source
        copyRequest.category = srequest.category
        copyRequest.reqstatus = srequest.reqstatus
        copyRequest.sub_task = srequest.sub_task
        copyRequest.assign_to = srequest.assign_to
        copyrequest.canceldate = srequest.canceldate
        copyrequest.cancelby = srequest.cancelby
        copyrequest.reason = srequest.reason
        copyrequest.source_name = srequest.source_name

    return generate_output()