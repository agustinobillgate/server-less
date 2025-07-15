#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_journal, Gl_jouhdr, Bediener, Res_history

def chg_gljourn_btn_del_1bl(jnr:int, rec_id:int, user_init:string, fibukonto:string):

    prepare_cache ([Gl_jouhdr, Bediener, Res_history])

    debits = to_decimal("0.0")
    credits = to_decimal("0.0")
    remains = to_decimal("0.0")
    str:string = ""
    datum:date = None
    refno:string = ""
    debit:Decimal = to_decimal("0.0")
    credit:Decimal = to_decimal("0.0")
    gl_journal = gl_jouhdr = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, remains, str, datum, refno, debit, credit, gl_journal, gl_jouhdr, bediener, res_history
        nonlocal jnr, rec_id, user_init, fibukonto

        return {"debits": debits, "credits": credits, "remains": remains}


    gl_journal = get_cache (Gl_journal, {"_recid": [(eq, rec_id)]})

    gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, jnr)]})
    datum = gl_jouhdr.datum
    refno = gl_jouhdr.refno
    debit =  to_decimal(gl_journal.debit)
    credit =  to_decimal(gl_journal.credit)
    gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) - to_decimal(gl_journal.debit)
    gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) - to_decimal(gl_journal.credit)
    gl_jouhdr.remain =  to_decimal(gl_jouhdr.debit) - to_decimal(gl_jouhdr.credit)
    pass
    debits =  to_decimal(gl_jouhdr.debit)
    credits =  to_decimal(gl_jouhdr.credit)
    remains =  to_decimal(gl_jouhdr.remain)
    pass
    db_session.delete(gl_journal)
    str = "Delete Journal, Date: " + to_string(datum) + ", AcctNo: " + fibukonto + ", refno: " + refno

    if debit != 0:
        str = str + ", debit: " + to_string(debit)
    else:
        str = str + ", credit: " + to_string(credit)

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = str
        res_history.action = "G/L"


        pass
        pass

    return generate_output()