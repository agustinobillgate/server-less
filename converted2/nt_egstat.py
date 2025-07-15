from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_request, Htparam, Eg_reqstat

def nt_egstat():
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


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    for req in db_session.query(Req).filter(
             (Req.closed_date == (get_current_date() - 1))).order_by(Req._recid).all():

        eg_reqstat = db_session.query(Eg_reqstat).filter(
                 (Eg_reqstat.reqfrom == req.source) & (Eg_reqstat.Deptnum == req.deptnum) & (Eg_reqstat.Location == req.reserve_int) & (Eg_reqstat.zinr == req.zinr) & (Eg_reqstat.Category == req.category) & (Eg_reqstat.Object == req.maintask) & (Eg_reqstat.ObjectItem == req.propertynr) & (Eg_reqstat.ObjectTask == req.sub_task) & (Eg_reqstat.PIC == req.assign_to) & (Eg_reqstat.reqStat == req.reqnr) & (Eg_reqstat.estFinishDate == req.ex_finishdate) & (Eg_reqstat.estfinishtime == req.ex_finishtime) & (Eg_reqstat.urgency == req.urgency) & (Eg_reqstat.opendate == req.opened_date) & (Eg_reqstat.opentime == req.opened_time) & (Eg_reqstat.processdate == req.process_date) & (Eg_reqstat.processtime == req.process_time) & (Eg_reqstat.donedate == req.done_date) & (Eg_reqstat.donetime == req.done_time) & (Eg_reqstat.closedate == req.closed_date) & (Eg_reqstat.closetime == req.closed_time)).first()

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

    return generate_output()