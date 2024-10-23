from functions.additional_functions import *
import decimal
from models import Gl_journal, Gl_jouhdr

def chg_gljourn_btn_delbl(jnr:int, rec_id:int):
    debits = to_decimal("0.0")
    credits = to_decimal("0.0")
    remains = to_decimal("0.0")
    gl_journal = gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, remains, gl_journal, gl_jouhdr
        nonlocal jnr, rec_id


        return {"debits": debits, "credits": credits, "remains": remains}


    gl_journal = db_session.query(Gl_journal).filter(
             (Gl_journal._recid == rec_id)).first()

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.jnr == jnr)).first()
    gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) - to_decimal(gl_journal.debit)
    gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) - to_decimal(gl_journal.credit)
    gl_jouhdr.remain =  to_decimal(gl_jouhdr.debit) - to_decimal(gl_jouhdr.credit)
    debits =  to_decimal(gl_jouhdr.debit)
    credits =  to_decimal(gl_jouhdr.credit)
    remains =  to_decimal(gl_jouhdr.remain)
    db_session.delete(gl_journal)

    return generate_output()