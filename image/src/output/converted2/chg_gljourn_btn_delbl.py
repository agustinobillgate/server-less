#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_journal, Gl_jouhdr

def chg_gljourn_btn_delbl(jnr:int, rec_id:int):

    prepare_cache ([Gl_jouhdr])

    debits = to_decimal("0.0")
    credits = to_decimal("0.0")
    remains = to_decimal("0.0")
    gl_journal = gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, remains, gl_journal, gl_jouhdr
        nonlocal jnr, rec_id

        return {"debits": debits, "credits": credits, "remains": remains}


    gl_journal = get_cache (Gl_journal, {"_recid": [(eq, rec_id)]})

    gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, jnr)]})
    gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) - to_decimal(gl_journal.debit)
    gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) - to_decimal(gl_journal.credit)
    gl_jouhdr.remain =  to_decimal(gl_jouhdr.debit) - to_decimal(gl_jouhdr.credit)
    pass
    debits =  to_decimal(gl_jouhdr.debit)
    credits =  to_decimal(gl_jouhdr.credit)
    remains =  to_decimal(gl_jouhdr.remain)
    pass
    db_session.delete(gl_journal)

    return generate_output()