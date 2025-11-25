#using conversion tools version: 1.0.0.117
#---------------------------------------------------
# Rd, 24/11/2025 , Update last counter dengan next_counter_for_update
#---------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Gl_journal, Htparam

def cancel_close_monthbl(from_date:date, to_date:date):

    prepare_cache ([Htparam])

    gl_jouhdr = gl_journal = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr, gl_journal, htparam
        nonlocal from_date, to_date

        return {}

    def close_month():

        nonlocal gl_jouhdr, gl_journal, htparam
        nonlocal from_date, to_date

        # gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(ge, from_date),(le, to_date)]})
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).with_for_update().first()
        while None != gl_jouhdr :
            pass
            gl_jouhdr.activeflag = 0 
            gl_jouhdr.batch = True

            if gl_jouhdr.jtype == 0:
                gl_jouhdr.batch = False

            pass

            # gl_journal = get_cache (Gl_journal, {"jnr": [(eq, gl_jouhdr.jnr)]})
            gl_journal = db_session.query(Gl_journal).filter(
                         (Gl_journal.jnr == gl_jouhdr.jnr)).with_for_update().first()
            while None != gl_journal:
                pass
                gl_journal.activeflag = 0
                pass

                curr_recid = gl_journal._recid
                gl_journal = db_session.query(Gl_journal).filter(
                             (Gl_journal.jnr == gl_jouhdr.jnr) & (Gl_journal._recid > curr_recid)).with_for_update().first()

            curr_recid = gl_jouhdr._recid
            gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date) & (Gl_jouhdr._recid > curr_recid)).with_for_update().first()
            
        # htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 597)).with_for_update().first()
        htparam.fdate = to_date

        # htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 558)).with_for_update().first()
        htparam.fdate = from_date - timedelta(days=1)


    close_month()

    return generate_output()