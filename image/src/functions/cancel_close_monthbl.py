from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_jouhdr, Gl_journal, Htparam

def cancel_close_monthbl(from_date:date, to_date:date):
    gl_jouhdr = gl_journal = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr, gl_journal, htparam


        return {}

    def close_month():

        nonlocal gl_jouhdr, gl_journal, htparam

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                    (Gl_jouhdr.datum >= from_date) &  (Gl_jouhdr.datum <= to_date)).first()
        while None != gl_jouhdr :

            gl_jouhdr = db_session.query(Gl_jouhdr).first()
            gl_jouhdr.activeflag = 0 gl_jouhdr.BATCH == True

            if gl_jouhdr.jtype == 0:
                gl_jouhdr.BATCH = False

            gl_jouhdr = db_session.query(Gl_jouhdr).first()

            gl_journal = db_session.query(Gl_journal).filter(
                        (Gl_journal.jnr == gl_jouhdr.jnr)).first()
            while None != gl_journal:

                gl_journal = db_session.query(Gl_journal).first()
                gl_journal.activeflag = 0

                gl_journal = db_session.query(Gl_journal).first()

                gl_journal = db_session.query(Gl_journal).filter(
                            (Gl_journal.jnr == gl_jouhdr.jnr)).first()

            gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                        (Gl_jouhdr.datum >= from_date) &  (Gl_jouhdr.datum <= to_date)).first()

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 597)).first()
        htparam.fdate = to_date

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 558)).first()
        htparam.fdate = from_date - 1


    close_month()

    return generate_output()