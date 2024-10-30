from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_jouhdr, Gl_journal, Htparam

def cancel_close_monthbl(from_date:date, to_date:date):
    gl_jouhdr = gl_journal = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr, gl_journal, htparam
        nonlocal from_date, to_date

        return {}

    def close_month():

        nonlocal gl_jouhdr, gl_journal, htparam
        nonlocal from_date, to_date

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).first()
        while None != gl_jouhdr :
            gl_jouhdr.activeflag = 0
            gl_jouhdr.batch = True

            if gl_jouhdr.jtype == 0:
                
                gl_jouhdr.batch = False

            gl_journal = db_session.query(Gl_journal).filter(
                         (Gl_journal.jnr == gl_jouhdr.jnr)).first()
            while None != gl_journal:
                gl_journal.activeflag = 0

                curr_recid = gl_journal._recid
                gl_journal = db_session.query(Gl_journal).filter(
                             (Gl_journal.jnr == gl_jouhdr.jnr)).filter(Gl_journal._recid > curr_recid).first()

            curr_recid = gl_jouhdr._recid
            gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).filter(Gl_jouhdr._recid > curr_recid).first()

        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 597)).first()
        htparam.fdate = to_date

        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 558)).first()
        htparam.fdate = from_date - timedelta(days=1)

    close_month()

    return generate_output()