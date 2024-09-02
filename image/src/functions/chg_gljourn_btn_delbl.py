from functions.additional_functions import *
import decimal
from models import Gl_journal, Gl_jouhdr

def chg_gljourn_btn_delbl(jnr:int, rec_id:int):
    debits = 0
    credits = 0
    remains = 0
    gl_journal = gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, remains, gl_journal, gl_jouhdr


        return {"debits": debits, "credits": credits, "remains": remains}


    gl_journal = db_session.query(Gl_journal).filter(
            (Gl_journal._recid == rec_id)).first()

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.jnr == jnr)).first()
    gl_jouhdr.debit = gl_jouhdr.debit - gl_journal.debit
    gl_jouhdr.credit = gl_jouhdr.credit - gl_journal.credit
    gl_jouhdr.remain = gl_jouhdr.debit - gl_jouhdr.credit

    gl_jouhdr = db_session.query(Gl_jouhdr).first()
    debits = gl_jouhdr.debit
    credits = gl_jouhdr.credit
    remains = gl_jouhdr.remain

    gl_journal = db_session.query(Gl_journal).first()
    db_session.delete(gl_journal)

    return generate_output()