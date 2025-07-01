#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Htparam

def transfer_journalsbl(from_date:date, to_date:date, depttype:int):

    prepare_cache ([Gl_jouhdr, Htparam])

    gl_jouhdr = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr, htparam
        nonlocal from_date, to_date, depttype

        return {}

    def transfer_journals():

        nonlocal gl_jouhdr, htparam
        nonlocal from_date, to_date, depttype

        gl_jouhdr1 = None
        gl_jouhdr2 = None
        bjouhdr = None
        date1:date = None
        date2:date = None
        Gl_jouhdr1 =  create_buffer("Gl_jouhdr1",Gl_jouhdr)
        Gl_jouhdr2 =  create_buffer("Gl_jouhdr2",Gl_jouhdr)
        Bjouhdr =  create_buffer("Bjouhdr",Gl_jouhdr)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
        date1 = htparam.fdate + timedelta(days=1)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
        date2 = htparam.fdate

        if from_date > date1:
            date1 = from_date

        if to_date < date2:
            date2 = to_date

        for gl_jouhdr1 in db_session.query(Gl_jouhdr1).filter(
                 (Gl_jouhdr1.activeflag == 0) & (Gl_jouhdr1.datum >= date1) & (Gl_jouhdr1.datum <= date2) & (Gl_jouhdr1.jtype == depttype) & (Gl_jouhdr1.batch)).order_by(Gl_jouhdr1._recid).all():

            bjouhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, gl_jouhdr1._recid)]})
            bjouhdr.batch = False
            pass
            pass

        for gl_jouhdr2 in db_session.query(Gl_jouhdr2).filter(
                 (Gl_jouhdr2.activeflag == 0) & (Gl_jouhdr2.datum >= date1) & (Gl_jouhdr2.datum <= date2) & (Gl_jouhdr2.jtype == 0) & (Gl_jouhdr2.batch)).order_by(Gl_jouhdr2._recid).all():

            bjouhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, gl_jouhdr2._recid)]})
            bjouhdr.batch = False
            pass
            pass


    def checked_journals():

        nonlocal gl_jouhdr, htparam
        nonlocal from_date, to_date, depttype

        gl_jouhdr3 = None
        gl_jouhdr4 = None
        bjouhdr = None
        date3:date = None
        date4:date = None
        Gl_jouhdr3 =  create_buffer("Gl_jouhdr3",Gl_jouhdr)
        Gl_jouhdr4 =  create_buffer("Gl_jouhdr4",Gl_jouhdr)
        Bjouhdr =  create_buffer("Bjouhdr",Gl_jouhdr)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
        date3 = htparam.fdate + timedelta(days=1)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
        date4 = htparam.fdate

        if from_date > date3:
            date3 = from_date

        if to_date < date4:
            date4 = to_date

        for gl_jouhdr3 in db_session.query(Gl_jouhdr3).filter(
                 (Gl_jouhdr3.activeflag == 0) & (Gl_jouhdr3.datum >= date3) & (Gl_jouhdr3.datum <= date4) & (Gl_jouhdr3.jtype == depttype) & (Gl_jouhdr3.batch)).order_by(Gl_jouhdr3._recid).all():

            bjouhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, gl_jouhdr3._recid)]})
            bjouhdr.batch = False
            pass
            pass

        for gl_jouhdr4 in db_session.query(Gl_jouhdr4).filter(
                 (Gl_jouhdr4.activeflag == 0) & (Gl_jouhdr4.datum >= date3) & (Gl_jouhdr4.datum <= date4) & (Gl_jouhdr4.jtype == 0) & (Gl_jouhdr4.batch)).order_by(Gl_jouhdr4._recid).all():

            bjouhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, gl_jouhdr4._recid)]})
            bjouhdr.batch = False
            pass
            pass


    transfer_journals()
    checked_journals()

    return generate_output()