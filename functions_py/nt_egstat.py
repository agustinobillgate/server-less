#using conversion tools version: 1.0.0.117

# ============================================
# Rulita, 23-10-2025 
# Issue : 
# - New compile program

# Rulita, 28-10-2025
# - Fixing issue where closed_date eq today -1 
# ============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_request, Htparam, Eg_reqstat

def nt_egstat():

    prepare_cache ([Eg_request, Htparam, Eg_reqstat])

    ci_date:date = None
    eg_request = htparam = eg_reqstat = None

    req = None

    Req = create_buffer("Req",Eg_request)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, eg_request, htparam, eg_reqstat
        nonlocal req


        nonlocal req

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    # Rulita, 28-10-2025
    # - Fixing issue where closed_date eq today -1 
    for req in db_session.query(Req).filter(
             (Req.closed_date == (get_current_date() - timedelta(days=1)))).order_by(Req._recid).all():

        eg_reqstat = get_cache (Eg_reqstat, {"reqfrom": [(eq, req.source)],"deptnum": [(eq, req.deptnum)],"location": [(eq, req.reserve_int)],"zinr": [(eq, req.zinr)],"category": [(eq, req.category)],"object": [(eq, req.maintask)],"objectitem": [(eq, req.propertynr)],"objecttask": [(eq, req.sub_task)],"pic": [(eq, req.assign_to)],"reqstat": [(eq, req.reqnr)],"estfinishdate": [(eq, req.ex_finishdate)],"estfinishtime": [(eq, req.ex_finishtime)],"urgency": [(eq, req.urgency)],"opendate": [(eq, req.opened_date)],"opentime": [(eq, req.opened_time)],"processdate": [(eq, req.process_date)],"processtime": [(eq, req.process_time)],"donedate": [(eq, req.done_date)],"donetime": [(eq, req.done_time)],"closedate": [(eq, req.closed_date)],"closetime": [(eq, req.closed_time)]})

        if not eg_reqstat:
            eg_reqstat = Eg_reqstat()
            db_session.add(eg_reqstat)

            eg_reqstat.reqfrom = req.source
            eg_reqstat.deptnum = req.deptnum
            eg_reqstat.location = req.reserve_int
            eg_reqstat.zinr = req.zinr
            eg_reqstat.category = req.category
            eg_reqstat.object = req.maintask
            eg_reqstat.objectitem = req.propertynr
            eg_reqstat.objecttask = req.sub_task
            eg_reqstat.pic = req.assign_to
            eg_reqstat.reqstat = req.reqnr
            eg_reqstat.estfinishdate = req.ex_finishdate
            eg_reqstat.estfinishtime = req.ex_finishtime
            eg_reqstat.urgency = req.urgency
            eg_reqstat.opendate = req.opened_date
            eg_reqstat.opentime = req.opened_time
            eg_reqstat.processdate = req.process_date
            eg_reqstat.processtime = req.process_time
            eg_reqstat.donedate = req.done_date
            eg_reqstat.donetime = req.done_time
            eg_reqstat.closedate = req.closed_date
            eg_reqstat.closetime = req.closed_time


        pass

    return generate_output()