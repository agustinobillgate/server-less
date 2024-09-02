from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_jouhdr, Htparam

def transfer_journalsbl(from_date:date, to_date:date, depttype:int):
    gl_jouhdr = htparam = None

    gl_jouhdr1 = None

    Gl_jouhdr1 = Gl_jouhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr, htparam
        nonlocal gl_jouhdr1


        nonlocal gl_jouhdr1
        return {}

    def transfer_journals():

        nonlocal gl_jouhdr, htparam
        nonlocal gl_jouhdr1


        nonlocal gl_jouhdr1

        date1:date = None
        date2:date = None
        Gl_jouhdr1 = Gl_jouhdr

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 558)).first()
        date1 = htparam.fdate + timedelta(days=1)

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 597)).first()
        date2 = htparam.fdate

        if from_date > date1:
            date1 = from_date

        if to_date < date2:
            date2 = to_date

        for gl_jouhdr1 in db_session.query(Gl_jouhdr1).filter(
                (Gl_jouhdr1.activeflag == 0) &  (Gl_jouhdr1.datum >= date1) &  (Gl_jouhdr1.datum <= date2) &  (Gl_jouhdr1.jtype == depttype) &  (Gl_jouhdr1.batch)).all():
            gl_jouhdr1.batch = False

    transfer_journals()

    return generate_output()